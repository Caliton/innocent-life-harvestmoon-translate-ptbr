#!/usr/bin/env python3
"""
scp_pipeline.py - Extrai, decoda e re-empacota .SCP do Innocent Life.

Estrutura:
  work/
    scp_raw/                 binarios .SCP comprimidos extraidos da ISO
    scp_decompressed/        binarios .SCP descomprimidos
    scp_decoded/             .txt com UTF-16 strings extraidos (referencia)
    scp_translated/          .txt editaveis (vira PT)
    scp_repacked/            .SCP recomprimidos PT

Cada .txt tem formato:
  # NOME.SCP - N strings UTF-16
  # Formato: [N|off=0xXXXX|chars=CC] header. Texto na linha seguinte.
  # MANTENHA chars EXATOS (PT mesma qtd ou usa padding com espaco)
  
  [0|off=0x100|chars=37]
  Mayor: Hmm... I guess he really wants
"""
import argparse, os, sys, re, glob, struct

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _ensure_slus_extracted(work_dir):
    """Garante que SLUS_216.41 esta em work/original/. Se nao, extrai da ISO."""
    slus_path = os.path.join(work_dir, 'original', 'SLUS_216.41')
    if os.path.exists(slus_path):
        return slus_path
    # extrair da ISO (procura no diretorio pai)
    project_dir = os.path.dirname(os.path.abspath(work_dir))
    iso_candidates = [
        os.path.join(project_dir, 'Innocent Life - A Futuristic Harvest Moon - Special Edition (USA).iso'),
        os.path.join(os.getcwd(), 'Innocent Life - A Futuristic Harvest Moon - Special Edition (USA).iso'),
    ]
    iso_path = next((p for p in iso_candidates if os.path.exists(p)), None)
    if not iso_path:
        return None
    print(f"  Extraindo SLUS_216.41 da ISO original...")
    os.makedirs(os.path.dirname(slus_path), exist_ok=True)
    try:
        import pycdlib
        iso = pycdlib.PyCdlib()
        iso.open(iso_path)
        with open(slus_path, 'wb') as f:
            iso.get_file_from_iso_fp(f, iso_path="/SLUS_216.41;1")
        iso.close()
        return slus_path
    except Exception as e:
        print(f"  ERRO ao extrair SLUS: {e}")
        return None


# Garante SLUS disponivel ANTES de importar scp_codec (que verifica path no import)
def _bootstrap_slus():
    # Procurar work_dir tipico
    for guess in [os.path.join(os.getcwd(), 'work'),
                  os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work')]:
        if os.path.isdir(guess):
            slus = _ensure_slus_extracted(guess)
            if slus:
                os.environ['SLUS_ELF'] = slus
                return
_bootstrap_slus()

from scp_codec import unpack_scp, pack_scp


def scan_utf16_strings(data, min_len=4):
    """Retorna lista (offset, chars, text) de strings UTF-16 LE."""
    strings = []
    i = 0
    while i < len(data) - min_len*2:
        if i % 2: i += 1; continue
        b1, b2 = data[i], data[i+1]
        if b2 == 0 and (0x20 <= b1 <= 0x7e or b1 == 0x0a):
            start = i
            chars = []
            while i < len(data) - 1:
                b1, b2 = data[i], data[i+1]
                if b1 == 0 and b2 == 0: break
                if b2 == 0 and (0x20 <= b1 <= 0x7e or b1 == 0x0a):
                    chars.append(chr(b1))
                    i += 2
                else: break
            if len(chars) >= min_len:
                strings.append((start, len(chars), ''.join(chars)))
        else:
            i += 2
    return strings


def text_to_txt(text):
    """Escapa newline pra .txt single-line: \\n -> 'N' literal."""
    return text.replace('\\', '\\\\').replace('\n', '\\n')


def txt_to_text(line):
    """Inverso: '\\n' literal -> newline."""
    out = []
    i = 0
    while i < len(line):
        if line[i:i+2] == '\\n':
            out.append('\n')
            i += 2
        elif line[i:i+2] == '\\\\':
            out.append('\\')
            i += 2
        else:
            out.append(line[i])
            i += 1
    return ''.join(out)


def decompress_to_decoded(scp_dir_raw, scp_dir_decomp, scp_dir_decoded):
    """Descompacta .SCP e gera .txt com strings UTF-16."""
    os.makedirs(scp_dir_decomp, exist_ok=True)
    os.makedirs(scp_dir_decoded, exist_ok=True)
    files = sorted(glob.glob(os.path.join(scp_dir_raw, '*.SCP')))
    total_strings = 0
    for path in files:
        name = os.path.basename(path)
        decomp_path = os.path.join(scp_dir_decomp, name + '.decomp')
        decoded_path = os.path.join(scp_dir_decoded, name + '.txt')
        
        with open(path, 'rb') as f: raw = f.read()
        if not os.path.exists(decomp_path):
            plain = unpack_scp(raw)
            with open(decomp_path, 'wb') as f: f.write(plain)
        else:
            with open(decomp_path, 'rb') as f: plain = f.read()
        
        # Scan strings
        strings = scan_utf16_strings(plain)
        
        # Gerar .txt
        lines = [
            f"# {name} - {len(strings)} strings UTF-16",
            f"# Formato: [N|off=0xXXXX|chars=CC] linha de header.",
            f"# Texto traduzido na linha seguinte ate proximo bloco.",
            f"# IMPORTANTE: PT precisa ter EXATAMENTE 'chars' caracteres (padding com espaco se PT menor).",
            f"# SEM ACENTOS. \\n literal = quebra de linha (1 char).",
            ""
        ]
        for i, (off, chars, text) in enumerate(strings):
            lines.append(f"[{i}|off=0x{off:x}|chars={chars}]")
            lines.append(text_to_txt(text))
            lines.append("")
        with open(decoded_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(lines))
        total_strings += len(strings)
    print(f"  Total: {total_strings:,} strings em {len(files)} .SCP")


def parse_translated_txt(path):
    """Le .txt e retorna lista (idx, off, chars, text)."""
    with open(path, encoding='utf-8') as f:
        content = f.read()
    blocks = []
    pattern = re.compile(r'^\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.MULTILINE | re.DOTALL)
    for m in pattern.finditer(content):
        idx = int(m.group(1))
        off = int(m.group(2), 16)
        chars = int(m.group(3))
        text = m.group(4).rstrip('\n')
        blocks.append((idx, off, chars, text))
    return blocks


def encode_utf16_padded(text_with_escapes, target_chars):
    """Encoda string PT em UTF-16 LE, com padding espaco se menor que target_chars.
    \\n vira newline (1 char). Erro se PT > target_chars."""
    real_text = txt_to_text(text_with_escapes)
    char_count = len(real_text)
    if char_count > target_chars:
        raise ValueError(f"texto tem {char_count} chars, slot tem {target_chars}: {real_text!r}")
    # padding com espaco
    padded = real_text + ' ' * (target_chars - char_count)
    return padded.encode('utf-16-le')


def build_scp_repacked(scp_dir_translated, scp_dir_decomp, scp_dir_repacked, scp_dir_raw):
    """Para cada .txt traduzido, patch in-place o buffer decomp e recomprime."""
    os.makedirs(scp_dir_repacked, exist_ok=True)
    txt_files = sorted(glob.glob(os.path.join(scp_dir_translated, '*.txt')))
    
    stats = {'unchanged': 0, 'changed': 0, 'errors': 0, 'bytes_total': 0, 'bytes_extra': 0}
    
    for txt_path in txt_files:
        name = os.path.basename(txt_path).replace('.txt','')  # ex: 'ETMYROOM.SCP'
        decomp_path = os.path.join(scp_dir_decomp, name + '.decomp')
        raw_path = os.path.join(scp_dir_raw, name)
        out_path = os.path.join(scp_dir_repacked, name)
        
        if not os.path.exists(decomp_path) or not os.path.exists(raw_path):
            continue
        
        with open(decomp_path, 'rb') as f: plain = bytearray(f.read())
        with open(raw_path, 'rb') as f: original_scp = f.read()
        
        # Aplicar patches do .txt
        blocks = parse_translated_txt(txt_path)
        n_changed = 0
        errors_local = []
        for idx, off, chars, text in blocks:
            # comparar com texto original no buffer
            orig_bytes = bytes(plain[off:off + chars*2])
            try:
                new_bytes = encode_utf16_padded(text, chars)
            except Exception as e:
                errors_local.append(f"[{idx}]: {e}")
                continue
            if new_bytes != orig_bytes:
                plain[off:off + chars*2] = new_bytes
                n_changed += 1
        
        if n_changed == 0:
            stats['unchanged'] += 1
            continue
        
        # Recomprimir
        try:
            new_scp = pack_scp(bytes(plain))
        except Exception as e:
            print(f"  ERR pack {name}: {e}")
            stats['errors'] += 1
            continue
        
        with open(out_path, 'wb') as f: f.write(new_scp)
        delta = len(new_scp) - len(original_scp)
        stats['changed'] += 1
        stats['bytes_total'] += len(new_scp)
        stats['bytes_extra'] += max(0, delta)
        if delta != 0:
            print(f"  {name}: {n_changed} strings PT, delta={delta:+d} bytes")
        if errors_local:
            for err in errors_local[:3]:
                print(f"      {err}")
    
    print(f"\nTotais: {stats['changed']} alterados, {stats['unchanged']} unchanged, {stats['errors']} erros")
    print(f"Extra bytes total: {stats['bytes_extra']:,} (precisa caber em padding ou realocacao)")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd', required=True)
    
    e = sub.add_parser('decompress', help='Descomp .SCP -> gera .decomp e .txt')
    e.add_argument('--work', required=True)
    
    b = sub.add_parser('build', help='Aplica .txt PT e gera .SCP recomprimidos')
    b.add_argument('--work', required=True)
    
    args = p.parse_args()
    
    scp_raw       = os.path.join(args.work, 'scp_raw')
    scp_decomp    = os.path.join(args.work, 'scp_decompressed')
    scp_decoded   = os.path.join(args.work, 'scp_decoded')
    scp_translated = os.path.join(args.work, 'scp_translated')
    scp_repacked  = os.path.join(args.work, 'scp_repacked')
    
    if args.cmd == 'decompress':
        print(f"=== Decomp .SCP -> {scp_decomp}/ + {scp_decoded}/ ===")
        decompress_to_decoded(scp_raw, scp_decomp, scp_decoded)
        # copy decoded -> translated como start
        os.makedirs(scp_translated, exist_ok=True)
        import shutil
        for src in glob.glob(os.path.join(scp_decoded, '*.txt')):
            dst = os.path.join(scp_translated, os.path.basename(src))
            if not os.path.exists(dst):
                shutil.copy2(src, dst)
        print(f"  Copy decoded -> translated em {scp_translated}/")
    elif args.cmd == 'build':
        print(f"=== Build .SCP traduzidos -> {scp_repacked}/ ===")
        build_scp_repacked(scp_translated, scp_decomp, scp_repacked, scp_raw)


if __name__ == '__main__':
    main()
