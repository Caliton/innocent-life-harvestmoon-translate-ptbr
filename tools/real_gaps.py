#!/usr/bin/env python3
"""Conta lacunas REAIS por arquivo: blocos nao-traduzidos com texto substancial
(ignora onomatopeias, rotulos curtos, nomes proprios, Yes/No)."""
import re, glob, os

B = re.compile(r'^\[(\d+)\|off=0x[0-9a-fA-F]+\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
def parse(p):
    return {int(m.group(1)): (int(m.group(2)), m.group(3).rstrip('\n')) for m in B.finditer(open(p, encoding='utf-8').read())}
def t2t(l):
    o = []; i = 0
    while i < len(l):
        if l[i:i+2] == '\\n': o.append('\n'); i += 2
        elif l[i:i+2] == '\\\\': o.append('\\'); i += 2
        else: o.append(l[i]); i += 1
    return ''.join(o)

# heuristica de onomatopeia/nao-traduzivel
ONO = re.compile(r'^[\*A-Za-z ]*:?\s*[~]?(Ga|Gaga|Zzz|Moo|Neigh|Chomp|Snore|Snort|Baa|Ruff|Cluck|Oink|Meow|La~|Yawn|Hmm|Zzzz|Rumble|RUMBLE|Splash|Splish|Blub|Beep|Heheh|Aggh|Ugh|Cough|Sob|Gulp|Pant|Sigh|Sniff|Achoo|Wah|Waaa|Boo|Ah+h|Oh+h|Hm+|Grr)', re.I)
def is_real(en):
    s = en.strip()
    if not s: return False
    if s == 'Yes\\nNo': return False
    if len(s) <= 8: return False
    # linhas so de pontuacao/reticencias (ex.: "Miss Cute: .......")
    body = re.sub(r'^[\*A-Za-z .]*:', '', s).strip()
    if body and not re.search(r'[A-Za-z]', body): return False
    # tem pelo menos 2 palavras com vogais (texto de verdade)
    words = re.findall(r'[A-Za-z]{3,}', t2t(s))
    if len(words) < 2: return False
    if ONO.match(s): return False
    return True

total_real = 0
rows = []
for tf in sorted(glob.glob('work/scp_translated/*.txt')):
    name = os.path.basename(tf)
    if name.startswith('TEST_'): continue
    df = os.path.join('work/scp_decoded', name)
    if not os.path.exists(df): continue
    dec = parse(df); tr = parse(tf)
    real = 0
    for i, (c, en) in dec.items():
        pt = tr.get(i, (c, ''))[1]
        if t2t(pt) == t2t(en) and is_real(en):
            real += 1
    if real:
        rows.append((name, real)); total_real += real
rows.sort(key=lambda r: -r[1])
print(f"LACUNAS REAIS restantes (excl. TEST_, onomatopeia, rotulos, nomes): {total_real}")
for name, n in rows:
    print(f"  {name}: {n}")
