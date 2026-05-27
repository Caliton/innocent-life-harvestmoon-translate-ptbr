#!/usr/bin/env python3
"""
fix_scp_tokens.py - Remove tokens <XX> escritos por engano em arquivos .SCP traduzidos.

Fundamento (verificado no binario descomprimido):
  - Tokens de controle (ex: <06> = nome do jogador) vivem SEMPRE no gap de 2 bytes
    ENTRE dois slots de string escaneados, NUNCA dentro do texto de um slot.
  - Se o gap antes de um slot e '06 00', o slot COMECA com o 'P' (parametro do nome).
  - O codec .SCP NAO interpreta <XX>; escreve-los como texto da 4 chars literais "<06>".

Regra de correcao por slot:
  - param_start (gap anterior == 06 00): manter o 'P' inicial; remover literal "<06>"
    no inicio; truncar em qualquer "<06>" restante.
  - caso contrario: truncar o texto no primeiro "<06>" (tudo dali em diante e lixo
    anexado que pertence ao gap/slot seguinte).

Uso:
  python tools/fix_scp_tokens.py            # dry-run: so relatorio
  python tools/fix_scp_tokens.py --apply    # aplica nos .txt
"""
import os, re, glob, sys, argparse

WORK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'work')

def scan_utf16_strings(data, min_len=4):
    strings = []
    i = 0
    while i < len(data) - min_len*2:
        if i % 2:
            i += 1; continue
        b1, b2 = data[i], data[i+1]
        if b2 == 0 and (0x20 <= b1 <= 0x7e or b1 == 0x0a):
            start = i
            chars = []
            while i < len(data) - 1:
                b1, b2 = data[i], data[i+1]
                if b1 == 0 and b2 == 0:
                    break
                if b2 == 0 and (0x20 <= b1 <= 0x7e or b1 == 0x0a):
                    chars.append(chr(b1)); i += 2
                else:
                    break
            if len(chars) >= min_len:
                strings.append((start, len(chars), ''.join(chars)))
        else:
            i += 2
    return strings

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

def real_len(line):
    return len(txt_to_text(line))

TOK = '<06>'
tok_any = re.compile(r'<[0-9a-fA-F]{2}>')

def param_start_map(decomp_path):
    """offset -> bool: slot e precedido por gap '06 00'."""
    data = open(decomp_path, 'rb').read()
    strings = scan_utf16_strings(data)
    m = {}
    for off, chars, text in strings:
        pre = data[off-2:off]
        m[off] = (pre == b'\x06\x00')
    return m

block_re = re.compile(r'(\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n)((?:(?!\[\d+\|off=).)*)', re.S)

def fix_text(pt, is_param_start):
    if TOK not in pt and not tok_any.search(pt):
        return pt, 'no-token'
    if is_param_start:
        # remove leading <06> (exposes the param P), then truncate at any remaining <06>
        new = pt
        # strip leading whitespace-preserving: only remove token if it's the very first thing
        if new.startswith(TOK):
            new = new[len(TOK):]
        # truncate at first remaining token
        idx = new.find(TOK)
        if idx != -1:
            new = new[:idx]
        # also remove any stray other <XX> tokens (rare)
        new = tok_any.sub('', new)
        return new.rstrip(), 'param'
    else:
        # truncate at first token
        idx = pt.find(TOK)
        new = pt[:idx] if idx != -1 else pt
        new = tok_any.sub('', new)  # safety
        return new.rstrip(), 'trunc'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    tr_dir = os.path.join(WORK, 'scp_translated')
    dec_dir = os.path.join(WORK, 'scp_decoded')
    decomp_dir = os.path.join(WORK, 'scp_decompressed')

    total_fixed = 0
    flags = []
    files_changed = 0
    for tf in sorted(glob.glob(os.path.join(tr_dir, '*.txt'))):
        name = os.path.basename(tf)
        scp = name[:-4]  # strip .txt
        decomp = os.path.join(decomp_dir, scp + '.decomp')
        if not os.path.exists(decomp):
            continue
        content = open(tf, encoding='utf-8').read()
        if TOK not in content:
            continue
        pmap = param_start_map(decomp)
        # EN reference for content-loss check
        en_map = {}
        decf = os.path.join(dec_dir, name)
        if os.path.exists(decf):
            for m in block_re.finditer(open(decf, encoding='utf-8').read()):
                en_map[int(m.group(2))] = m.group(5).rstrip('\n')

        new_parts = []
        last = 0
        changed_here = 0
        for m in block_re.finditer(content):
            hdr = m.group(1)
            idx = int(m.group(2)); off = int(m.group(3), 16); chars = int(m.group(4))
            body = m.group(5)
            body_stripped = body.rstrip('\n')
            trailing = body[len(body_stripped):]
            if TOK in body_stripped:
                is_ps = pmap.get(off, False)
                fixed, mode = fix_text(body_stripped, is_ps)
                if fixed != body_stripped:
                    changed_here += 1
                    total_fixed += 1
                    # checks
                    en = en_map.get(idx, '')
                    note = None
                    if fixed.strip() == '':
                        note = 'RESULTADO VAZIO'
                    elif en and real_len(fixed) < 0.4 * real_len(en):
                        note = f'PERDA DE CONTEUDO (PT={real_len(fixed)} vs EN={real_len(en)})'
                    elif real_len(fixed) > chars:
                        note = f'AINDA OVERFLOW ({real_len(fixed)}>{chars})'
                    if note:
                        flags.append((name, idx, chars, mode, note, en, body_stripped, fixed))
                # rebuild
                new_parts.append(content[last:m.start(5)])
                new_parts.append(fixed + trailing)
                last = m.end(5)
        new_parts.append(content[last:])
        if changed_here and args.apply:
            open(tf, 'w', encoding='utf-8', newline='\n').write(''.join(new_parts))
            files_changed += 1

    print(f"Total de strings com token corrigidas: {total_fixed}")
    if args.apply:
        print(f"Arquivos reescritos: {files_changed}")
    else:
        print("(dry-run -- nada escrito; use --apply)")
    print(f"\nCasos a REVISAR manualmente: {len(flags)}")
    for name, idx, chars, mode, note, en, pt, fixed in flags:
        print(f"  {name}[{idx}] chars={chars} mode={mode} :: {note}")
        print(f"    EN : {en[:85]!r}")
        print(f"    PT : {pt[:85]!r}")
        print(f"    FIX: {fixed[:85]!r}")

if __name__ == '__main__':
    main()
