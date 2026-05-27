#!/usr/bin/env python3
import re, sys

def t2t(l):
    o = []; i = 0
    while i < len(l):
        if l[i:i+2] == '\\n': o.append('\n'); i += 2
        elif l[i:i+2] == '\\\\': o.append('\\'); i += 2
        else: o.append(l[i]); i += 1
    return ''.join(o)

B = re.compile(r'^\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
def parse(p):
    return [(int(m.group(1)), int(m.group(3)), m.group(4).rstrip('\n')) for m in B.finditer(open(p, encoding='utf-8').read())]
TOK = re.compile(r'<[0-9a-fA-F]{2}>')

for name in sys.argv[1:]:
    dec = {i: t for i, c, t in parse('work/scp_decoded/' + name)}
    tot = tr = over = tokn = nonascii = yesno = 0
    overdet = []; nadet = []
    for i, chars, text in parse('work/scp_translated/' + name):
        tot += 1
        if i not in dec or t2t(text) != t2t(dec[i]): tr += 1
        rl = len(t2t(text))
        if rl > chars:
            over += 1
            if dec.get(i) == 'Yes\\nNo': yesno += 1
            else: overdet.append((i, chars, rl, text[:40]))
        if TOK.search(text): tokn += 1
        for ch in text:
            if ord(ch) > 0x7e and ch != '▽':
                nonascii += 1; nadet.append((i, hex(ord(ch)), text[:40])); break
    print(f"{name}: trad {tr}/{tot} | overflow={over} (YesNo={yesno}, outros={over-yesno}) | tokens={tokn} | nao-ASCII={nonascii}")
    for d in overdet[:8]: print("    OVERFLOW:", d)
    for d in nadet[:8]: print("    NAO-ASCII:", d)
