#!/usr/bin/env python3
"""Verifica que TODOS os .SCP traduzidos recompilam (pack LZSS + roundtrip),
simulando exatamente o build (pula strings que excedem chars, como o pipeline)."""
import os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('SLUS_ELF', 'work/original/SLUS_216.41')
from scp_pipeline import parse_translated_txt, encode_utf16_padded
from scp_codec import pack_scp, unpack_scp

tr_dir = 'work/scp_translated'
decomp_dir = 'work/scp_decompressed'
ok = fail = skipped_files = 0
total_skipped_strings = 0
failures = []
for txt in sorted(glob.glob(os.path.join(tr_dir, '*.txt'))):
    name = os.path.basename(txt)[:-4]  # strip .txt -> NOME.SCP
    decomp = os.path.join(decomp_dir, name + '.decomp')
    if not os.path.exists(decomp):
        continue
    plain = bytearray(open(decomp, 'rb').read())
    blocks = parse_translated_txt(txt)
    n = skip = 0
    for idx, off, chars, text in blocks:
        try:
            nb = encode_utf16_padded(text, chars)
        except Exception:
            skip += 1
            continue
        if bytes(plain[off:off+chars*2]) != nb:
            plain[off:off+chars*2] = nb
            n += 1
    total_skipped_strings += skip
    if n == 0:
        continue
    try:
        scp = pack_scp(bytes(plain))
        rt = unpack_scp(scp)
        if rt != bytes(plain):
            fail += 1; failures.append((name, 'roundtrip != plain'))
        else:
            ok += 1
    except Exception as e:
        fail += 1; failures.append((name, str(e)))
        continue

print(f"Arquivos recompilados OK: {ok} | FALHAS: {fail}")
print(f"Strings puladas (oversize, ficam EN no jogo - esperado p/ Yes/No): {total_skipped_strings}")
for name, err in failures:
    print(f"  FALHA {name}: {err}")
sys.exit(1 if fail else 0)
