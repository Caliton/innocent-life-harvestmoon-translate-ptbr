#!/usr/bin/env python3
"""
fix_accents.py - Remove acentos e corrige look-alikes cirilicos nos .txt traduzidos.

A fonte do jogo so tem ASCII; acentos renderizam como glifo invalido. Cada char
acentuado -> ASCII (1:1, nao muda a contagem de chars). Preserva ▽ (U+25BD), que e
um glifo legitimo de menu presente tambem no EN.

Uso:
  python tools/fix_accents.py           # dry-run
  python tools/fix_accents.py --apply
"""
import os, glob, argparse

MAP = {
    # acentos latinos PT
    'á':'a','à':'a','â':'a','ã':'a','ä':'a',
    'é':'e','è':'e','ê':'e','ë':'e',
    'í':'i','ì':'i','î':'i','ï':'i',
    'ó':'o','ò':'o','ô':'o','õ':'o','ö':'o',
    'ú':'u','ù':'u','û':'u','ü':'u',
    'ç':'c','ñ':'n',
    'Á':'A','À':'A','Â':'A','Ã':'A','Ä':'A',
    'É':'E','È':'E','Ê':'E','Ë':'E',
    'Í':'I','Ì':'I','Î':'I','Ï':'I',
    'Ó':'O','Ò':'O','Ô':'O','Õ':'O','Ö':'O',
    'Ú':'U','Ù':'U','Û':'U','Ü':'U',
    'Ç':'C','Ñ':'N',
    # look-alikes cirilicos -> latino
    'а':'a','е':'e','о':'o','р':'p','с':'c','у':'y','х':'x',
    'г':'g','т':'t','в':'v','н':'h','к':'k','м':'m','і':'i',
    'А':'A','Е':'E','О':'O','Р':'P','С':'C','Т':'T','В':'B','Н':'H','К':'K','М':'M',
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dirs = ['work/scp_translated', 'work/translated']
    total = 0
    files_changed = 0
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, '*.txt'))):
            lines = open(f, encoding='utf-8').read().split('\n')
            changed = 0
            new_lines = []
            for line in lines:
                if line.startswith('#') or line.startswith('['):
                    new_lines.append(line); continue
                nl = ''.join(MAP.get(c, c) for c in line)
                if nl != line:
                    changed += sum(1 for a, b in zip(line, nl) if a != b)
                    if not args.apply:
                        print(f"  {os.path.basename(f)}: {line.strip()[:60]!r}")
                new_lines.append(nl)
            if changed:
                total += changed
                files_changed += 1
                if args.apply:
                    open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(new_lines))
    print(f"\n{'Aplicado' if args.apply else 'Dry-run'}: {total} chars corrigidos em {files_changed} arquivos")

if __name__ == '__main__':
    main()
