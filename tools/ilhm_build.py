#!/usr/bin/env python3
"""
ilhm_build.py - Pipeline completo: translated/*.txt -> ISO patcheada in-place.

Le todos os .txt de translated/, re-encoda as strings UTF-16 e injeta na ISO
nos offsets corretos (calculados a partir do LBA original do arquivo).

Estrategia: in-place sem mexer em tamanhos de arquivos.
  - SYSTEM.MSG: slot fixo, padding com null.
  - SI_*.DAT:   in-place mantendo CHARS exato; PT menor preenche com espaco.

Strings que excedem chars original: erro reportado (precisa encurtar).

Uso:
  # IMPORTANTE: copia a ISO original primeiro (Ctrl+C / Ctrl+V no Windows).
  # Esse script edita IN-PLACE.
  python ilhm_build.py --iso InnocentLife_PT.iso --work work/

Args opcionais:
  --dry-run     so reporta o que faria, nao escreve nada
  --only NOME   processa apenas o arquivo NOME (ex: --only SYSTEM.MSG)
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilhm_codec import (
    parse_sysmsg, scan_mn01,
    encode_sysmsg_payload, encode_utf16_string,
    txt_line_to_text,
)

SECTOR = 2048

# Mapeamento .txt slug -> nome binario (igual ilhm_extract)
TARGETS = [
    ("SYSTEM.MSG",   "system_msg"),
    ("SI_LT00.DAT",  "si_lt00"),
    ("SI_LT0~1.DAT", "si_lt01"),
    ("SI_MN00.DAT",  "si_mn00"),
    ("SI_MN0~1.DAT", "si_mn01"),
    ("SI_MN0~2.DAT", "si_mn02"),
    ("SI_DB00.DAT",  "si_db00"),
]


def load_lba_map(work_dir):
    """Le work/lba_map.txt gerado pelo extract."""
    path = os.path.join(work_dir, "lba_map.txt")
    lba_map = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            fname, lba = parts[0], int(parts[1])
            lba_map[fname] = lba
    return lba_map


def parse_txt_blocks(txt_path):
    """Le .txt e retorna lista de (header_dict, text_str)."""
    with open(txt_path, encoding="utf-8") as f:
        content = f.read()
    blocks = []
    # split em headers [N|...]
    pattern = re.compile(r'^\[(\d+)\|([^\]]+)\]\n((?:(?!^\[\d+\|).)*)', re.MULTILINE | re.DOTALL)
    for m in pattern.finditer(content):
        idx = int(m.group(1))
        meta_str = m.group(2)
        text_raw = m.group(3).rstrip('\n')
        meta = {'index': idx}
        for kv in meta_str.split('|'):
            if '=' in kv:
                k, v = kv.split('=', 1)
                meta[k] = v
        blocks.append((meta, text_raw))
    return blocks


def build_sysmsg(work_dir):
    """Le translated/system_msg.txt e gera SYSTEM.MSG patcheado.
    Retorna (bytes_patcheados, lista_de_erros)."""
    orig_path = os.path.join(work_dir, "original", "SYSTEM.MSG")
    txt_path = os.path.join(work_dir, "translated", "system_msg.txt")
    with open(orig_path, "rb") as f:
        orig = bytearray(f.read())
    entries = parse_sysmsg(bytes(orig))
    blocks = parse_txt_blocks(txt_path)
    if len(blocks) != len(entries):
        return None, [f"count mismatch: txt {len(blocks)} vs SYSTEM.MSG {len(entries)}"]

    errors = []
    changed = 0
    for (meta, text), entry in zip(blocks, entries):
        slot = int(meta['slot'])
        if slot != entry.slot_size:
            errors.append(f"  [{entry.index}] slot diff: txt={slot} vs sysmsg={entry.slot_size}")
            continue
        # so re-encoda se texto mudou
        if text == entry.text:
            continue
        text_unescaped = txt_line_to_text(text)
        try:
            new_bytes = encode_sysmsg_payload(text_unescaped, entry.slot_size)
        except Exception as e:
            errors.append(f"  [{entry.index}] encode: {e}")
            continue
        orig[entry.file_off:entry.file_off + entry.slot_size] = new_bytes
        changed += 1
    return bytes(orig), errors, changed


def build_mn01(work_dir, fname, slug):
    """Le translated/<slug>.txt e gera bytes patcheados do MN01 file."""
    orig_path = os.path.join(work_dir, "original", fname)
    txt_path = os.path.join(work_dir, "translated", f"{slug}.txt")
    with open(orig_path, "rb") as f:
        orig = bytearray(f.read())
    strings = scan_mn01(bytes(orig))
    blocks = parse_txt_blocks(txt_path)
    if len(blocks) != len(strings):
        return None, [f"count mismatch: txt {len(blocks)} vs {fname} {len(strings)}"], 0

    errors = []
    changed = 0
    for (meta, text), s in zip(blocks, strings):
        chars = int(meta['chars'])
        if chars != s.chars:
            errors.append(f"  [{s.hdr_off:x}] chars diff: txt={chars} vs file={s.chars}")
            continue
        if text == s.text:
            continue
        text_unescaped = txt_line_to_text(text)
        try:
            new_bytes = encode_utf16_string(text_unescaped, s.chars)
        except Exception as e:
            errors.append(f"  [{s.hdr_off:x}] encode: {e}")
            continue
        orig[s.str_off:s.str_off + s.chars*2] = new_bytes
        changed += 1
    return bytes(orig), errors, changed


def patch_iso(iso_path, lba, new_bytes, dry_run):
    """Sobrescreve setor LBA da ISO com new_bytes."""
    abs_off = lba * SECTOR
    if not dry_run:
        with open(iso_path, "r+b") as f:
            f.seek(abs_off)
            f.write(new_bytes)
    return abs_off


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--iso", required=True, help="ISO PT (sera modificada in-place)")
    p.add_argument("--work", required=True, help="diretorio com translated/ e original/")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--only", help="processa apenas este arquivo (ex: SYSTEM.MSG)")
    args = p.parse_args()

    if not os.path.exists(args.iso):
        sys.exit(f"ISO nao existe: {args.iso}")

    lba_map = load_lba_map(args.work)

    print(f"=== Build ISO PT: {args.iso} ===")
    if args.dry_run:
        print("(dry-run: nao vai escrever na ISO)\n")

    total_changed = 0
    total_errors = []

    for fname, slug in TARGETS:
        if args.only and fname != args.only:
            continue
        print(f"\n--- {fname} ---")
        try:
            if fname == "SYSTEM.MSG":
                result = build_sysmsg(args.work)
            else:
                result = build_mn01(args.work, fname, slug)
            new_bytes, errors, changed = result
        except Exception as e:
            print(f"  ERRO: {e}")
            continue

        if errors:
            print(f"  {len(errors)} erros:")
            for err in errors[:10]:
                print(f"    {err}")
            if len(errors) > 10:
                print(f"    ... e mais {len(errors) - 10}")
            total_errors.extend(errors)

        if new_bytes is None:
            continue

        if changed == 0:
            print(f"  nenhuma mudanca")
            continue

        # confere que o size nao mudou
        orig_size = os.path.getsize(os.path.join(args.work, "original", fname))
        if len(new_bytes) != orig_size:
            print(f"  ERRO FATAL: size novo ({len(new_bytes)}) != original ({orig_size})")
            continue

        lba = lba_map[fname]
        abs_off = patch_iso(args.iso, lba, new_bytes, args.dry_run)
        print(f"  {changed} strings alteradas, patcheadas em 0x{abs_off:x}")
        total_changed += changed

    print(f"\n=== Total: {total_changed} strings alteradas, {len(total_errors)} erros ===")
    if total_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
