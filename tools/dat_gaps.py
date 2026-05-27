#!/usr/bin/env python3
"""Analisa lacunas e overflow nos arquivos DAT (SI_*.DAT, SYSTEM.MSG)."""
import re, sys, os

def parse_dat(path):
    content = open(path, encoding='utf-8').read()
    pat = re.compile(r'^\[(\d+)\|([^\]]+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
    out = []
    for m in pat.finditer(content):
        meta = {}
        for kv in m.group(2).split('|'):
            if '=' in kv:
                k, v = kv.split('=', 1); meta[k] = v
        out.append((int(m.group(1)), meta, m.group(3).rstrip('\n')))
    return out

def count_chars_dat(text):
    # <HHLL> (4 hex) e <XX> (2 hex) contam como 1 char; resto literal. \n literal = 2 chars aqui?
    # No DAT (SI_*) o texto NAO usa \n de quebra como 1 char — usa <0a00>? Verificar: encode_utf16_string
    # trata <HHLL> como 1 char e cada outro char como 1. Nao ha tratamento de \\n.
    n = 0; i = 0
    while i < len(text):
        if text[i] == '<' and i + 5 < len(text) and text[i+5] == '>':
            tok = text[i+1:i+5]
            if all(d in '0123456789abcdefABCDEF' for d in tok):
                n += 1; i += 6; continue
        n += 1; i += 1
    return n

for slug in [a for a in sys.argv[1:] if not a.startswith('--')]:
    dec = {i: (meta, t) for i, meta, t in parse_dat(f'work/decoded/{slug}.txt')}
    tr = {i: (meta, t) for i, meta, t in parse_dat(f'work/translated/{slug}.txt')}
    if set(dec) != set(tr):
        print(f"{slug}: !!! BLOCOS DIVERGENTES decoded={len(dec)} translated={len(tr)}"); continue
    total = tr_count = over = empty = 0
    overs = []; untrans = []
    for i in dec:
        dmeta, den = dec[i]
        tmeta, tpt = tr[i]
        if den.strip() == '':
            empty += 1; continue
        total += 1
        if tpt != den:
            tr_count += 1
        else:
            untrans.append((i, den))
        limit = int(tmeta.get('chars', 0))
        if count_chars_dat(tpt) > limit:
            over += 1; overs.append((i, limit, count_chars_dat(tpt), tpt))
    print(f"{slug}: traduzidas {tr_count}/{total} | vazios={empty} | OVERFLOW={over}")
    for i, lim, got, pt in overs[:10]:
        print(f"    OVER [{i}] chars={lim} got={got}: {pt[:50]!r}")
    if '--list' in sys.argv:
        print(f"  -- nao traduzidos ({len(untrans)}):")
        for i, en in untrans[:60]:
            print(f"    [{i}] {en[:60]!r}")
