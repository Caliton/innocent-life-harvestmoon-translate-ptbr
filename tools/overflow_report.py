#!/usr/bin/env python3
"""Relatorio de overflow: strings PT que excedem 'chars' (ficariam em ingles no build)."""
import os, re, glob, argparse

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
    content = open(path, encoding='utf-8').read()
    pat = re.compile(r'^\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
    return [(int(m.group(1)), int(m.group(3)), m.group(4).rstrip('\n')) for m in pat.finditer(content)]

ap = argparse.ArgumentParser()
ap.add_argument('--list', action='store_true', help='lista cada string em overflow')
ap.add_argument('--by', type=int, default=0, help='filtra overflow por excesso >= N')
args = ap.parse_args()

dec_dir = 'work/scp_decoded'
rows = []
for tf in sorted(glob.glob('work/scp_translated/*.txt')):
    name = os.path.basename(tf)
    dec = {i: t for i, c, t in parse_scp(os.path.join(dec_dir, name))} if os.path.exists(os.path.join(dec_dir, name)) else {}
    for i, chars, text in parse_scp(tf):
        rl = len(txt_to_text(text))
        if rl > chars:
            rows.append((name, i, chars, rl, rl - chars, text, dec.get(i, '')))

rows.sort(key=lambda r: -r[4])
small = sum(1 for r in rows if r[4] <= 3)
print(f"TOTAL overflow: {len(rows)} | excesso<=3: {small} | excesso>3: {len(rows)-small}")
from collections import Counter
byfile = Counter(r[0] for r in rows)
print("\nPor arquivo:")
for name, n in byfile.most_common():
    print(f"  {name}: {n}")
if args.list:
    print("\n--- strings em overflow (excesso desc) ---")
    for name, i, chars, rl, over, text, en in rows:
        if over < args.by:
            continue
        print(f"{name}[{i}] chars={chars} PT={rl} (+{over})")
        print(f"   EN : {en[:90]!r}")
        print(f"   PT : {text[:90]!r}")
