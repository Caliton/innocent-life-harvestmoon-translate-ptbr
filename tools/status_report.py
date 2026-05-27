#!/usr/bin/env python3
"""
status_report.py - Panorama de progresso da traducao (SCP + SYSTEM.MSG/DAT).

Por arquivo SCP: total de strings, traduzidas, intactas(EN), overflow.
Resumo dos arquivos DAT/MSG.
Nota: "traduzido" = texto difere do EN. Nomes proprios mantidos contam como nao-traduzidos.
"""
import os, re, glob
from collections import Counter

def txt_to_text(line):
    out = []; i = 0
    while i < len(line):
        if line[i:i+2] == '\\n':
            out.append('\n'); i += 2
        elif line[i:i+2] == '\\\\':
            out.append('\\'); i += 2
        else:
            out.append(line[i]); i += 1
    return ''.join(out)

def parse_scp(path):
    c = open(path, encoding='utf-8').read()
    pat = re.compile(r'^\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
    return [(int(m.group(1)), int(m.group(3)), m.group(4).rstrip('\n')) for m in pat.finditer(c)]

def parse_dat(path):
    c = open(path, encoding='utf-8').read()
    pat = re.compile(r'^\[(\d+)\|([^\]]+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
    out = []
    for m in pat.finditer(c):
        meta = {}
        for kv in m.group(2).split('|'):
            if '=' in kv:
                k, v = kv.split('=', 1); meta[k] = v
        out.append((int(m.group(1)), meta, m.group(3).rstrip('\n')))
    return out

print("=== SCP (dialogos) — por arquivo: trad/total | falta | overflow ===")
g_tot = g_tr = g_over = 0
pend = []
done = []
for tf in sorted(glob.glob('work/scp_translated/*.txt')):
    name = os.path.basename(tf)
    df = os.path.join('work/scp_decoded', name)
    if not os.path.exists(df):
        continue
    dec = {i: t for i, c, t in parse_scp(df)}
    tot = tr = over = 0
    for i, chars, text in parse_scp(tf):
        tot += 1; g_tot += 1
        if i not in dec or txt_to_text(text) != txt_to_text(dec[i]):
            tr += 1; g_tr += 1
        if len(txt_to_text(text)) > chars:
            over += 1; g_over += 1
    falta = tot - tr
    if falta == 0 and over == 0:
        done.append(name)
    else:
        pend.append((name, tot, tr, falta, over))

pend.sort(key=lambda r: -(r[3] + r[4]))
for name, tot, tr, falta, over in pend:
    tag = []
    if falta: tag.append(f"falta {falta}")
    if over: tag.append(f"OVERFLOW {over}")
    print(f"  {name:22} {tr:>4}/{tot:<4}  {'  '.join(tag)}")
print(f"\n  [{len(done)} arquivos 100% OK e sem overflow]")
print(f"  GERAL SCP: {g_tr}/{g_tot} traduzidas, {g_over} overflow")

print("\n=== SYSTEM.MSG + SI_*.DAT ===")
for tf in sorted(glob.glob('work/translated/*.txt')):
    name = os.path.basename(tf)
    df = os.path.join('work/decoded', name)
    if not os.path.exists(df):
        continue
    dec = {i: t for i, meta, t in parse_dat(df)}
    tot = tr = 0
    for i, meta, text in parse_dat(tf):
        d = dec.get(i, '')
        if d.strip() == '':
            continue
        tot += 1
        if text != d:
            tr += 1
    print(f"  {name:16} {tr}/{tot}")
