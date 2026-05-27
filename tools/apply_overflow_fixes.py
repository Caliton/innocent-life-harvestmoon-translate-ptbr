#!/usr/bin/env python3
"""
apply_overflow_fixes.py - Aplica fixes de overflow (deduplicados) em todos os .SCP.

Le work/overflow_worklist.json (chars, en por entrada) e um arquivo de fixes
(lista alinhada por indice: cada item {"i": N, "pt": "..."} ou pt=null).
Para cada string em overflow cujo (chars, en) casa com uma entrada corrigida,
substitui o corpo. Valida: real_len<=chars, sem <XX>, sem nao-ASCII.

Uso:
  python tools/apply_overflow_fixes.py --fixes work/overflow_fixes.json            # dry-run+validacao
  python tools/apply_overflow_fixes.py --fixes work/overflow_fixes.json --apply
"""
import os, re, glob, json, argparse

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

TOK = re.compile(r'<[0-9a-fA-F]{2}>')
BLOCK = re.compile(r'(\[(\d+)\|off=0x[0-9a-fA-F]+\|chars=(\d+)\]\n)((?:(?!\[\d+\|off=).)*)', re.S)

def validate(pt, chars):
    errs = []
    if TOK.search(pt):
        errs.append('contem token <XX>')
    for ch in pt:
        if ord(ch) > 0x7e and ch != '▽':
            errs.append(f'nao-ASCII U+{ord(ch):04X} {ch!r}')
            break
    if rlen(pt) > chars:
        errs.append(f'len {rlen(pt)} > chars {chars}')
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fixes', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    worklist = json.load(open('work/overflow_worklist.json', encoding='utf-8'))
    fixes_raw = json.load(open(args.fixes, encoding='utf-8'))
    # map worklist index -> fixed pt
    fix_by_i = {}
    for item in fixes_raw:
        if item.get('pt') is not None:
            fix_by_i[item['i']] = item['pt']
    # build lookup (chars, en) -> fixed pt
    lut = {}
    bad = []
    skipped_null = 0
    for i, wl in enumerate(worklist):
        if i not in fix_by_i:
            skipped_null += 1
            continue
        pt = fix_by_i[i]
        errs = validate(pt, wl['chars'])
        if errs:
            bad.append((i, wl['chars'], wl['en'], pt, errs))
            continue
        lut[(wl['chars'], wl['en'])] = pt

    print(f"Fixes validos: {len(lut)} | invalidos: {len(bad)} | sem fix(null): {skipped_null}")
    for i, chars, en, pt, errs in bad[:40]:
        print(f"  [#{i}] chars={chars} {errs}")
        print(f"     EN: {en[:80]!r}")
        print(f"     PT: {pt[:80]!r}")
    if bad and not args.apply:
        print("\n!! Corrija os invalidos antes de --apply (eles serao ignorados).")

    if not args.apply:
        print("\n(dry-run)")
        return

    dec = 'work/scp_decoded'
    changed_total = 0
    for tf in sorted(glob.glob('work/scp_translated/*.txt')):
        name = os.path.basename(tf)
        decf = os.path.join(dec, name)
        if not os.path.exists(decf):
            continue
        decmap = {int(m.group(2)): m.group(4).rstrip('\n') for m in BLOCK.finditer(open(decf, encoding='utf-8').read())}
        content = open(tf, encoding='utf-8').read()
        n = 0
        def repl(m):
            nonlocal n
            idx = int(m.group(2)); chars = int(m.group(3)); body = m.group(4)
            bs = body.rstrip('\n'); trail = body[len(bs):]
            if rlen(bs) > chars:
                en = decmap.get(idx, '')
                key = (chars, en)
                if key in lut:
                    n += 1
                    return m.group(1) + lut[key] + trail
            return m.group(0)
        new = BLOCK.sub(repl, content)
        if n:
            open(tf, 'w', encoding='utf-8', newline='\n').write(new)
            changed_total += n
    print(f"Aplicado: {changed_total} ocorrencias corrigidas")

if __name__ == '__main__':
    main()
