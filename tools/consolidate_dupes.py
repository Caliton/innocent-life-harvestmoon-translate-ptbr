#!/usr/bin/env python3
"""
consolidate_dupes.py - Consolida traducao entre arquivos .SCP com conteudo EN identico.

Para cada grupo de arquivos identicos (mesmo texto EN), escolhe a melhor traducao
de cada string e escreve em TODOS os arquivos do grupo (preservando os headers
proprios de cada arquivo, pois o off= pode diferir).

Melhor PT por indice: traduzida(difere do EN) E cabe(<=chars) > traduzida porem
overflow(menor excesso) > EN. Empate: mais frequente, depois mais longa-que-cabe.

Uso:
  python tools/consolidate_dupes.py            # dry-run (relatorio)
  python tools/consolidate_dupes.py --apply
"""
import os, re, glob, argparse
from collections import Counter

GROUPS = {
    'D0_67': ['D01B1','D02F1','D02F2','D02F3','D03B1','D03B2A','D03F1A','D03F1B',
              'D04B1A','D04B1B','D04F1A','D04F1B','D04F1C','D05B1A','D05F1D','D06B1',
              'D06F1','D06OUT','D07B1','D07B2','D07F1','D08F1','D08F2'],
    'F_157': ['F03KIN_1','F04TSURO','F05SAKYU','F06OUT','F08KIN_1'],
    'V_39':  ['TEMPLATE','VTBRAU_1','VTBRAU_2','VTMAF1','VTOUT2'],
}

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

BLOCK = re.compile(r'(\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n)((?:(?!\[\d+\|off=).)*)', re.S)

def parse(path):
    """retorna (header_template_list, dict idx->(chars, body, trailing))"""
    content = open(path, encoding='utf-8').read()
    blocks = {}
    order = []
    for m in BLOCK.finditer(content):
        idx = int(m.group(2)); chars = int(m.group(4))
        body = m.group(5)
        bs = body.rstrip('\n'); trail = body[len(bs):]
        blocks[idx] = (chars, bs, trail)
        order.append(idx)
    return content, blocks

def rlen(t):
    return len(txt_to_text(t))

def pick_best(idx, chars, candidates, en):
    # candidates: list of PT body strings (one per file)
    translated = [c for c in candidates if txt_to_text(c) != txt_to_text(en)]
    if not translated:
        return en, 'EN'
    fits = [c for c in translated if rlen(c) <= chars]
    pool = fits if fits else translated
    cnt = Counter(pool)
    best = max(pool, key=lambda c: (cnt[c], len(c) if rlen(c) <= chars else -rlen(c)))
    return best, ('FIT' if fits else 'OVER')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    tr = 'work/scp_translated'
    dec = 'work/scp_decoded'
    for gname, files in GROUPS.items():
        # load EN (from first file's decoded)
        en_content, en_blocks = parse(os.path.join(dec, files[0] + '.SCP.txt'))
        parsed = {}
        for f in files:
            parsed[f] = parse(os.path.join(tr, f + '.SCP.txt'))
        idxs = sorted(en_blocks.keys())
        # sanity: chars match across files
        bad = []
        for idx in idxs:
            cs = set(parsed[f][1].get(idx, (None,))[0] for f in files)
            if len(cs) > 1:
                bad.append((idx, cs))
        chosen = {}
        stats = Counter()
        for idx in idxs:
            chars = en_blocks[idx][0]
            en_body = en_blocks[idx][1]
            cands = [parsed[f][1][idx][1] for f in files if idx in parsed[f][1]]
            best, kind = pick_best(idx, chars, cands, en_body)
            chosen[idx] = best
            stats[kind] += 1
        n = len(idxs)
        print(f"=== {gname}: {len(files)} arquivos, {n} strings ===")
        if bad:
            print(f"  !! AVISO: {len(bad)} indices com chars divergentes -> {bad[:3]}")
        print(f"  apos consolidar: FIT(traduz+cabe)={stats['FIT']} OVER(traduz+estoura)={stats['OVER']} EN(falta)={stats['EN']}")
        if args.apply:
            for f in files:
                content, blocks = parsed[f]
                # rebuild this file's content, swapping bodies
                def repl(m):
                    idx = int(m.group(2))
                    hdr = m.group(1)
                    _, _, trail = blocks[idx]
                    return hdr + chosen[idx] + trail
                new = BLOCK.sub(repl, content)
                open(os.path.join(tr, f + '.SCP.txt'), 'w', encoding='utf-8', newline='\n').write(new)
            print(f"  -> aplicado em {len(files)} arquivos")
        print()

if __name__ == '__main__':
    main()
