#!/usr/bin/env python3
"""
scp_codec.py - Decoder + Encoder LZSS Marvelous via Unicorn Engine.

Encoder: vaddr 0x180180  signature: encode(a0=src, a1=src_size, a2=dst, a3=out_size_ptr)
Decoder: vaddr 0x1807c8  signature: decode(a0=src, a1=ignored, a2=dst, a3=out_size_ptr)
"""

import struct
import os
import sys
from unicorn import *
from unicorn.mips_const import *

# Localizar SLUS executável:
# 1. env SLUS_ELF tem prioridade
# 2. work/original/SLUS_216.41 (extraído pelo ilhm_extract)
# 3. ./SLUS_216.41 (cwd)
# 4. /tmp/work/SLUS_216.41 (sandbox legacy)
def _find_slus():
    candidates = [
        os.environ.get('SLUS_ELF'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work', 'original', 'SLUS_216.41'),
        os.path.join(os.getcwd(), 'work', 'original', 'SLUS_216.41'),
        os.path.join(os.getcwd(), 'SLUS_216.41'),
        '/tmp/work/SLUS_216.41',
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return os.path.abspath(p)
    return None

ELF_PATH = _find_slus()

MAIN_VA   = 0x100000;  MAIN_SIZE  = 0x200000
# (merged)
# (merged)

SCRATCH_VA  = 0x10000000
SCRATCH_SIZE = 0x800000
SRC_BUF   = SCRATCH_VA + 0x000000
DST_BUF   = SCRATCH_VA + 0x200000
OUT_PTR   = SCRATCH_VA + 0x400000
HASH_BUF  = SCRATCH_VA + 0x500000
STACK_BASE = SCRATCH_VA + 0x700000
STACK_TOP  = STACK_BASE + 0x080000

GP_VAL    = 0x1bb100 + 0x8000

ENCODER_VA = 0x180180
DECODER_VA = 0x1807c8
ALLOC_VA   = 0x169d68
FREE_VA    = 0x16a190
RETURN_MAGIC = 0xDEADBEEF


def _load_elf_segments(mu):
    if ELF_PATH is None:
        raise FileNotFoundError(
            "SLUS_216.41 nao encontrado. Roda o 1_extrair.bat primeiro (ele extrai SLUS_216.41 pra work/original/),\n"
            "ou define a variavel SLUS_ELF apontando pro arquivo SLUS_216.41 da ISO."
        )
    with open(ELF_PATH, 'rb') as f:
        elf = f.read()
    mu.mem_write(0x100000, elf[0x1000:0x1000 + 0xbb098])
    mu.mem_write(0x1bb100, elf[0xbc100:0xbc100 + 0x82c75])
    mu.mem_write(0x294900, elf[0x13f900:0x13f900 + 0x67b8])


def _make_unicorn():
    mu = Uc(UC_ARCH_MIPS, UC_MODE_MIPS64 + UC_MODE_LITTLE_ENDIAN)
    mu.mem_map(MAIN_VA,    MAIN_SIZE, UC_PROT_ALL)
    mu.mem_map(SCRATCH_VA, SCRATCH_SIZE, UC_PROT_ALL)
    _load_elf_segments(mu)
    mu.reg_write(UC_MIPS_REG_GP, GP_VAL)
    mu.reg_write(UC_MIPS_REG_SP, STACK_TOP - 0x100)
    return mu


def _install_stubs(mu, hash_buf_va):
    EE_MULT_PCS = {0x1801e4, 0x180210, 0x180240, 0x180270, 0x18028c}
    REG_MAP = {
        0: UC_MIPS_REG_ZERO, 1: UC_MIPS_REG_AT, 2: UC_MIPS_REG_V0, 3: UC_MIPS_REG_V1,
        4: UC_MIPS_REG_A0, 5: UC_MIPS_REG_A1, 6: UC_MIPS_REG_A2, 7: UC_MIPS_REG_A3,
        8: UC_MIPS_REG_T0, 9: UC_MIPS_REG_T1, 10: UC_MIPS_REG_T2, 11: UC_MIPS_REG_T3,
        12: UC_MIPS_REG_T4, 13: UC_MIPS_REG_T5, 14: UC_MIPS_REG_T6, 15: UC_MIPS_REG_T7,
        16: UC_MIPS_REG_S0, 17: UC_MIPS_REG_S1, 18: UC_MIPS_REG_S2, 19: UC_MIPS_REG_S3,
        20: UC_MIPS_REG_S4, 21: UC_MIPS_REG_S5, 22: UC_MIPS_REG_S6, 23: UC_MIPS_REG_S7,
        24: UC_MIPS_REG_T8, 25: UC_MIPS_REG_T9, 26: UC_MIPS_REG_K0, 27: UC_MIPS_REG_K1,
        28: UC_MIPS_REG_GP, 29: UC_MIPS_REG_SP, 30: UC_MIPS_REG_FP, 31: UC_MIPS_REG_RA,
    }
    def hook_code(uc, address, size, user_data):
        if address == ALLOC_VA:
            uc.mem_write(hash_buf_va, b"\x00" * 0x10000)
            uc.reg_write(UC_MIPS_REG_V0, hash_buf_va)
            uc.reg_write(UC_MIPS_REG_PC, uc.reg_read(UC_MIPS_REG_RA))
            return
        if address == FREE_VA:
            uc.reg_write(UC_MIPS_REG_PC, uc.reg_read(UC_MIPS_REG_RA))
            return
        if address in EE_MULT_PCS:
            word = struct.unpack("<I", uc.mem_read(address, 4))[0]
            funct = word & 0x3f
            rd = (word >> 11) & 0x1f
            rs = (word >> 21) & 0x1f
            rt = (word >> 16) & 0x1f
            a = uc.reg_read(REG_MAP[rs]) & 0xFFFFFFFF
            b = uc.reg_read(REG_MAP[rt]) & 0xFFFFFFFF
            if funct == 0x18:
                aa = a if a < 0x80000000 else a - 0x100000000
                bb = b if b < 0x80000000 else b - 0x100000000
                prod = (aa * bb) & 0xFFFFFFFFFFFFFFFF
            else:
                prod = (a * b) & 0xFFFFFFFFFFFFFFFF
            lo = prod & 0xFFFFFFFF
            hi = (prod >> 32) & 0xFFFFFFFF
            uc.reg_write(UC_MIPS_REG_LO, lo)
            uc.reg_write(UC_MIPS_REG_HI, hi)
            if rd != 0:
                v = lo if lo < 0x80000000 else lo | 0xFFFFFFFF00000000
                uc.reg_write(REG_MAP[rd], v)
            uc.reg_write(UC_MIPS_REG_PC, address + 4)
    mu.hook_add(UC_HOOK_CODE, hook_code, begin=ALLOC_VA, end=ALLOC_VA + 3)
    mu.hook_add(UC_HOOK_CODE, hook_code, begin=FREE_VA,  end=FREE_VA  + 3)
    for pc in EE_MULT_PCS:
        mu.hook_add(UC_HOOK_CODE, hook_code, begin=pc, end=pc + 3)

def encode_lzss(plain: bytes, debug=False) -> bytes:
    mu = _make_unicorn()
    _install_stubs(mu, HASH_BUF)
    pad = max(0x40, len(plain) * 2 + 0x40)
    mu.mem_write(SRC_BUF, b'\x00' * (len(plain) + 64))
    mu.mem_write(SRC_BUF, plain)
    mu.mem_write(DST_BUF, b'\x00' * pad)
    mu.mem_write(OUT_PTR, b'\x00' * 4)
    mu.reg_write(UC_MIPS_REG_A0, SRC_BUF)
    mu.reg_write(UC_MIPS_REG_A1, len(plain))
    mu.reg_write(UC_MIPS_REG_A2, DST_BUF)
    mu.reg_write(UC_MIPS_REG_A3, OUT_PTR)
    mu.reg_write(UC_MIPS_REG_RA, RETURN_MAGIC)
    try:
        mu.emu_start(ENCODER_VA, RETURN_MAGIC, timeout=0, count=0)
    except UcError as e:
        if debug: print(f'[encode] {e} pc={mu.reg_read(UC_MIPS_REG_PC):x}', file=sys.stderr)
    out_size = struct.unpack('<I', mu.mem_read(OUT_PTR, 4))[0]
    return bytes(mu.mem_read(DST_BUF, out_size))


def decode_lzss(payload: bytes, debug=False) -> bytes:
    src_size = len(payload)
    mu = _make_unicorn()
    _install_stubs(mu, HASH_BUF)
    mu.mem_write(SRC_BUF, payload)
    dst_size = max(0x40000, len(payload) * 16)
    mu.mem_write(DST_BUF, b'\x00' * dst_size)
    mu.mem_write(OUT_PTR, b'\x00' * 4)
    mu.reg_write(UC_MIPS_REG_A0, SRC_BUF)
    mu.reg_write(UC_MIPS_REG_A1, src_size)
    mu.reg_write(UC_MIPS_REG_A2, DST_BUF)
    mu.reg_write(UC_MIPS_REG_A3, OUT_PTR)
    mu.reg_write(UC_MIPS_REG_RA, RETURN_MAGIC)
    try:
        mu.emu_start(DECODER_VA, RETURN_MAGIC, timeout=0, count=0)
    except UcError as e:
        if debug: print(f'[decode] {e} pc={mu.reg_read(UC_MIPS_REG_PC):x}', file=sys.stderr)
    out_size = struct.unpack('<I', mu.mem_read(OUT_PTR, 4))[0]
    return bytes(mu.mem_read(DST_BUF, out_size))


def unpack_scp(scp: bytes) -> bytes:
    assert scp[:4] == b'SL01'
    decompressed_size = struct.unpack('<I', scp[4:8])[0]
    compressed_size   = struct.unpack('<I', scp[8:12])[0]
    payload = scp[12:12 + compressed_size]
    out = decode_lzss(payload)
    return out


def pack_scp(plain: bytes) -> bytes:
    # End-of-stream sentinel required by the decoder
    payload = encode_lzss(plain) + b"\x11\x00\x00"
    return b'SL01' + struct.pack('<II', len(plain), len(payload)) + payload


if __name__ == '__main__':
    import glob
    raw_dir = '/sessions/wonderful-inspiring-pascal/mnt/harvestmoon/ilhm/work/scp_raw'
    test_files = sorted(glob.glob(os.path.join(raw_dir, '*.SCP')))[:3]
    for tf in test_files:
        name = os.path.basename(tf)
        with open(tf, 'rb') as f:
            raw = f.read()
        try:
            plain = unpack_scp(raw)
        except Exception as e:
            print(f'{name}: decode failed: {e}')
            continue
        print(f'{name}: orig_compressed={len(raw)} decompressed={len(plain)}')
        repk = pack_scp(plain)
        print(f'  recompressed={len(repk)} (delta {len(repk)-len(raw):+d})')
        re_plain = unpack_scp(repk)
        ok = (re_plain == plain)
        print(f'  roundtrip equal: {ok}')
        if not ok:
            for i, (a, b) in enumerate(zip(re_plain, plain)):
                if a != b:
                    print(f'    diff at {i}: re={a:02x} orig={b:02x}'); break
