#!/usr/bin/env python3
"""
ilhm_extract.py - Extrai SYSTEM.MSG e SI_*.DAT da ISO do Innocent Life e
decodifica pra .txt legivel/editavel.

Layout gerado:
  work/
    original/         binarios extraidos da ISO (read-only, fonte)
      SYSTEM.MSG
      SI_LT00.DAT
      ...
    decoded/          .txt com texto em ingles (NAO editar - referencia)
      system_msg.txt
      si_lt00.txt
      ...
    translated/       .txt com placeholder pra editar (vai virar PT)
      system_msg.txt
      ...

Uso:
  python ilhm_extract.py --iso "Innocent Life...iso" --work work/

Formato dos .txt:
  Header com metadados, depois blocos:
    [N|slot=SS|id=0xMID]      <- SYSTEM.MSG
    texto da mensagem...
    (linha em branco separa)

    [N|kind=item|chars=CC|id=0xID]    <- MN01 containers
    [N|kind=cont|chars=CC]
    [N|kind=flex|chars=CC]
    texto da string...
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ilhm_codec import parse_sysmsg, scan_mn01, text_to_txt_line

try:
    import pycdlib
except ImportError:
    sys.exit("pip install pycdlib")


# Lista de arquivos que tem texto traduzivel
TARGETS = [
    ("/DATAIMG/FONT/SYSTEM.MSG;1",          "SYSTEM.MSG",   "system_msg"),
    ("/DATAIMG/MENU/FORM/SI_LT00.DAT;1",    "SI_LT00.DAT",  "si_lt00"),
    ("/DATAIMG/MENU/FORM/SI_LT0~1.DAT;1",   "SI_LT0~1.DAT", "si_lt01"),
    ("/DATAIMG/MENU/FORM/SI_MN00.DAT;1",    "SI_MN00.DAT",  "si_mn00"),
    ("/DATAIMG/MENU/FORM/SI_MN0~1.DAT;1",   "SI_MN0~1.DAT", "si_mn01"),
    ("/DATAIMG/MENU/FORM/SI_MN0~2.DAT;1",   "SI_MN0~2.DAT", "si_mn02"),
    ("/DATAIMG/MENU/FORM/SI_DB00.DAT;1",    "SI_DB00.DAT",  "si_db00"),
    # SLUS executavel — necessario pelo scp_codec.py (decoder/encoder LZSS)
    ("/SLUS_216.41;1",                       "SLUS_216.41",  "_slus"),
]


def extract_from_iso(iso_path: str, out_dir: str) -> dict:
    """Extrai os arquivos da TARGETS. Retorna dict {fname: lba}."""
    os.makedirs(out_dir, exist_ok=True)
    iso = pycdlib.PyCdlib()
    iso.open(iso_path)
    lba_map = {}
    for iso_path_in, fname, _slug in TARGETS:
        rec = iso.get_record(iso_path=iso_path_in)
        lba_map[fname] = rec.extent_location()
        out = os.path.join(out_dir, fname)
        with open(out, "wb") as f:
            iso.get_file_from_iso_fp(f, iso_path=iso_path_in)
        print(f"  extraido: {fname:18s} ({os.path.getsize(out):>8,} bytes, LBA {rec.extent_location()})")
    iso.close()
    return lba_map


def decode_sysmsg_to_txt(bin_path: str, txt_path: str):
    with open(bin_path, "rb") as f:
        data = f.read()
    entries = parse_sysmsg(data)
    lines = [
        f"# {os.path.basename(bin_path)} - {len(entries)} mensagens",
        f"# Formato: [N|slot=SS|id=0xMID] linha de header.",
        f"# Texto nas linhas seguintes ate proximo bloco.",
        f"# Tokens <XX> = byte de controle, <HHLL> = 2 bytes brutos.",
        f"# Quebra de linha vira \\n literal. NAO mude o header [N|...].",
        "",
    ]
    for e in entries:
        lines.append(f"[{e.index}|slot={e.slot_size}|id=0x{e.msg_id:x}]")
        lines.append(text_to_txt_line(e.text))
        lines.append("")
    with open(txt_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def decode_mn01_to_txt(bin_path: str, txt_path: str):
    with open(bin_path, "rb") as f:
        data = f.read()
    strings = scan_mn01(data)
    name = os.path.basename(bin_path)
    lines = [
        f"# {name} - {len(strings)} strings UTF-16",
        f"# Formato: [N|kind=K|chars=CC|id=0xID|hdr=0xHHHH|str=0xSSSS] linha de header.",
        f"# kind: item (chunk com ID), cont (continuacao), flex (header simples).",
        f"# Texto nas linhas seguintes ate proximo bloco. ESCAPE <HHLL> = 2 bytes brutos.",
        f"# NAO mude o header. Mantenha chars EXATO (PT mesma quantidade de chars).",
        "",
    ]
    for i, s in enumerate(strings):
        id_part = f"|id=0x{s.item_id:x}" if s.item_id is not None else ""
        lines.append(f"[{i}|kind={s.kind}|chars={s.chars}{id_part}|hdr=0x{s.hdr_off:x}|str=0x{s.str_off:x}]")
        lines.append(text_to_txt_line(s.text))
        lines.append("")
    with open(txt_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--iso", required=True, help="ISO do Innocent Life USA")
    p.add_argument("--work", required=True, help="diretorio de trabalho")
    args = p.parse_args()

    orig_dir = os.path.join(args.work, "original")
    decoded_dir = os.path.join(args.work, "decoded")
    translated_dir = os.path.join(args.work, "translated")
    os.makedirs(decoded_dir, exist_ok=True)
    os.makedirs(translated_dir, exist_ok=True)

    print(f"=== [1/3] Extraindo arquivos da ISO ===")
    lba_map = extract_from_iso(args.iso, orig_dir)

    # Salvar mapeamento LBA pra build depois
    with open(os.path.join(args.work, "lba_map.txt"), "w") as f:
        f.write("# fname\tLBA\toffset_absoluto\n")
        for fname, lba in lba_map.items():
            f.write(f"{fname}\t{lba}\t0x{lba*2048:x}\n")

    print(f"\n=== [2/3] Decodificando pra .txt (decoded/) ===")
    for iso_path, fname, slug in TARGETS:
        if slug.startswith('_'):
            # arquivos com slug que comeca com '_' (ex: _slus) sao so binarios extras, nao tem .txt
            continue
        bin_path = os.path.join(orig_dir, fname)
        txt_path = os.path.join(decoded_dir, f"{slug}.txt")
        if fname == "SYSTEM.MSG":
            decode_sysmsg_to_txt(bin_path, txt_path)
        else:
            decode_mn01_to_txt(bin_path, txt_path)
        print(f"  decoded: {os.path.basename(txt_path)}")

    print(f"\n=== [3/3] Copiando decoded/ -> translated/ como ponto de partida ===")
    import shutil
    for iso_path, fname, slug in TARGETS:
        if slug.startswith('_'):
            continue
        src = os.path.join(decoded_dir, f"{slug}.txt")
        dst = os.path.join(translated_dir, f"{slug}.txt")
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"  criado: {os.path.basename(dst)}")
        else:
            print(f"  ja existe: {os.path.basename(dst)} (mantido)")

    print(f"\nPronto! Edite arquivos em {translated_dir}/ depois rode ilhm_build.py")


if __name__ == "__main__":
    main()
