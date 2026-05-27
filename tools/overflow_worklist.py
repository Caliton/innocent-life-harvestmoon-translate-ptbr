#!/usr/bin/env python3
"""Gera worklist de strings em overflow, deduplicadas por (chars, EN)."""
import os, re, glob, json, argparse
from collections import defaultdict

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

def rlen(t):
    return len(txt_to_text(t))

BLOCK = re.compile(r'^\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)

def parse(path):
    c = open(path, encoding='utf-8').read()
    return [(int(m.group(1)), int(m.group(3)), m.group(4).rstrip('\n')) for m in BLOCK.finditer(c)]

ap = argparse.ArgumentParser()
ap.add_argument('--json', help='escreve worklist json')
ap.add_argument('--show', type=int, default=0, help='mostra N exemplos')
args = ap.parse_args()

dec = 'work/scp_decoded'
uniq = {}  # (chars, en) -> {pt, over, count, files}
for tf in sorted(glob.glob('work/scp_translated/*.txt')):
    name = os.path.basename(tf)
    decmap = {i: t for i, c, t in parse(os.path.join(dec, name))} if os.path.exists(os.path.join(dec, name)) else {}
    for i, chars, text in parse(tf):
        if rlen(text) > chars:
            en = decmap.get(i, '')
            key = (chars, en)
            e = uniq.setdefault(key, {'pt': text, 'chars': chars, 'en': en, 'over': rlen(text) - chars, 'count': 0, 'files': set()})
            e['count'] += 1
            e['files'].add(name)
            # keep the longest current PT as representative
            if rlen(text) > rlen(e['pt']):
                e['pt'] = text

items = list(uniq.values())
items.sort(key=lambda e: -e['count'])
total_occ = sum(e['count'] for e in items)
print(f"Strings em overflow: {total_occ} ocorrencias, {len(items)} UNICAS (por chars+EN)")
print(f"  unicas com excesso<=3: {sum(1 for e in items if e['over']<=3)}")
print(f"  unicas com excesso>3 : {sum(1 for e in items if e['over']>3)}")
if args.show:
    for e in items[:args.show]:
        print(f"\n  x{e['count']} chars={e['chars']} (+{e['over']})")
        print(f"    EN: {e['en']!r}")
        print(f"    PT: {e['pt']!r}")
if args.json:
    out = [{'i': idx, 'chars': e['chars'], 'en': e['en'], 'pt': e['pt'], 'over': e['over'],
            'count': e['count'], 'files': sorted(e['files'])} for idx, e in enumerate(items)]
    json.dump(out, open(args.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"\nworklist -> {args.json}")
