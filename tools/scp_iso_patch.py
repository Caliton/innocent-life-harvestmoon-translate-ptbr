#!/usr/bin/env python3
"""
scp_iso_patch.py - Aplica .SCP recompilados in-place na ISO.

Estrategia:
- Para cada .SCP em work/scp_repacked/, descobrir LBA original na ISO
- Substituir bytes; se novo_size > orig_size, validar que cabe no padding
- Padding com 0x00 ate atingir tamanho original (jogo le tamanho via header SL01 interno)
"""
import argparse, os, sys, glob, struct
import pycdlib

SECTOR = 2048

def load_scp_lba_map(iso_path):
    """Retorna dict {nome_arquivo: (lba, size_original)}."""
    iso = pycdlib.PyCdlib()
    iso.open(iso_path)
    result = {}
    for child in iso.list_children(iso_path="/DATAIMG/SCRIPT/USA"):
        name = child.file_identifier().decode('latin-1', errors='replace')
        if name in ('.','..'): continue
        # Strip ;1 e normalizar ~ pra _
        clean = name.replace(';1','').replace('~','_').upper()
        # Original name no scp_raw segue convencao do pycdlib que usa _ pra ~
        result[clean] = (child.extent_location(), child.get_data_length())
    iso.close()
    return result

def patch_iso(iso_path, work_dir):
    """Aplica todos .SCP em scp_repacked/ na ISO."""
    lba_map = load_scp_lba_map(iso_path)
    repacked = sorted(glob.glob(os.path.join(work_dir, 'scp_repacked', '*.SCP')))
    
    if not repacked:
        print("  Nenhum .SCP recompilado pra aplicar.")
        return 0, 0
    
    applied = 0
    skipped = 0
    overflows = []
    
    with open(iso_path, 'r+b') as f:
        for path in repacked:
            name = os.path.basename(path).upper()
            if name not in lba_map:
                print(f"  ERR: {name} nao mapeado na ISO")
                continue
            lba, orig_size = lba_map[name]
            with open(path, 'rb') as g: new_data = g.read()
            
            orig_padded = (orig_size + SECTOR - 1) // SECTOR * SECTOR
            if len(new_data) > orig_padded:
                overflows.append((name, len(new_data), orig_padded))
                skipped += 1
                continue
            
            # Padding com 0x00 ate orig_padded
            padded = new_data + b'\x00' * (orig_padded - len(new_data))
            abs_off = lba * SECTOR
            f.seek(abs_off)
            f.write(padded)
            applied += 1
    
    print(f"\n  {applied} .SCP aplicados, {skipped} skipped")
    if overflows:
        print(f"\n  OVERFLOWS ({len(overflows)}):")
        for name, new_sz, padded_sz in overflows[:10]:
            print(f"    {name}: {new_sz:,} > {padded_sz:,} (excede +{new_sz-padded_sz:,}B)")
    return applied, skipped


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--iso", required=True, help="ISO PT pra patchear in-place")
    p.add_argument("--work", required=True)
    args = p.parse_args()
    
    if not os.path.exists(args.iso):
        sys.exit(f"ISO nao existe: {args.iso}")
    
    print(f"=== Aplicando .SCP recompilados em {args.iso} ===")
    patch_iso(args.iso, args.work)


if __name__ == '__main__':
    main()
