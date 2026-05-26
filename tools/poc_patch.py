#!/usr/bin/env python3
"""
poc_patch.py - POC v3: traducoes do tutorial inicial (Gayak/Iron Hoe + menu).

Sem mexer em tamanhos/offsets - so substitui chars UTF-16.

NAO copia a ISO. Edita a ISO que voce passar IN-PLACE. Faca copia ANTES manualmente
(Ctrl+C / Ctrl+V no Windows e instantaneo) e rode no arquivo de copia.

Uso:
  # 1. Copia "Innocent Life - A Futuristic Harvest Moon - Special Edition (USA).iso"
  #    e renomeia pra "InnocentLife_PT_POC.iso"
  # 2. Roda:
  python tools/poc_patch.py --iso InnocentLife_PT_POC.iso
"""
import argparse, sys, os

# === BASE OFFSETS DOS ARQUIVOS NA ISO ===
SYSMSG_BASE   = 0x3ca5e000  # SYSTEM.MSG
SI_MN00_BASE  = 0x403c6800  # SI_MN00.DAT (menu)
SI_MN2_BASE   = 0x403cd000  # SI_MN0~2.DAT (duplicata do menu)
SI_LT00_BASE  = 0x403ad800  # SI_LT00.DAT (descricoes de item)

# === PATCHES DE STRING UTF-16 SEM HEADER (mesma length) ===
# Formato: (offset_absoluto, original_pra_validar, novo)
# Tem que ter EXATAMENTE o mesmo numero de chars.

PATCHES_UTF16_INPLACE = [
    # --- SI_LT00.DAT: descricao da enxada que Gayak DA NO TUTORIAL ---
    # Aparece quando voce equipa/olha a Iron Hoe (1a ferramenta do tutorial)
    (SI_LT00_BASE + 0xb0da, "A small hoe given to you by Gayak.", "Uma pequena enxada dada por Gayak."),
    (SI_LT00_BASE + 0xb1b4, "Only a master farmer could ever hope", "So um mestre fazendeiro pode esperar"),

    # --- SI_MN00.DAT: menu de pause (apertar Triangle/Start) ---
    (SI_MN00_BASE + 0x31a6, "Items",  "Itens"),
    (SI_MN00_BASE + 0x1458, "Cancel", "Anular"),
    (SI_MN00_BASE + 0x5a78, "Autumn", "Outono"),
    # SI_MN0~2.DAT (duplicata do menu)
    (SI_MN2_BASE  + 0x31a6, "Items",  "Itens"),
    (SI_MN2_BASE  + 0x1458, "Cancel", "Anular"),
    (SI_MN2_BASE  + 0x5a78, "Autumn", "Outono"),
]

# === PATCHES DE SLOT FIXO NO SYSTEM.MSG ===
# Formato: <0002> + texto UTF-16 + <0002><0a00> + padding
# (offset_absoluto, slot_size, texto)

PATCHES_SYSMSG_SLOT = [
    # Aparecem em variados momentos do gameplay (porta, inventario, geladeira)
    (SYSMSG_BASE + 0x37a2, 48, "Porta trancada!"),
    (SYSMSG_BASE + 0x37d2, 48, "Porta trancada!"),
    (SYSMSG_BASE + 0x80b2, 60, "Voce abre a geladeira."),
    (SYSMSG_BASE + 0x81f6, 66, "Bolsa cheia!"),
    (SYSMSG_BASE + 0x92e2, 66, "Bolsa cheia!"),
    (SYSMSG_BASE + 0x954a, 66, "Bolsa cheia!"),
]

def patch_inplace(f, abs_off, original, new):
    if len(original) != len(new):
        raise ValueError(f"tamanhos diferentes: {original} ({len(original)}) vs {new} ({len(new)})")
    f.seek(abs_off)
    cur = f.read(len(original) * 2)
    expected = original.encode('utf-16-le')
    if cur != expected:
        return False, cur
    f.seek(abs_off)
    f.write(new.encode('utf-16-le'))
    return True, cur

def patch_sysmsg_slot(f, abs_off, slot, text):
    PREFIX = b'\x02\x00'
    SUFFIX = b'\x02\x00\x0a\x00'
    body = text.encode('utf-16-le')
    full = PREFIX + body + SUFFIX
    if len(full) > slot:
        raise ValueError(f"texto nao cabe: {len(full)} > {slot}")
    full += b'\x00' * (slot - len(full))
    f.seek(abs_off)
    f.write(full)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--iso", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if not os.path.exists(args.iso):
        sys.exit(f"ISO nao existe: {args.iso}")

    expected_size = 1356595200
    actual_size = os.path.getsize(args.iso)
    if actual_size != expected_size:
        print(f"AVISO: tamanho da ISO ({actual_size:,}) != esperado ({expected_size:,})")

    print(f"=== Patches em {args.iso} ===")
    if args.dry_run:
        print("(dry-run: nao vai gravar nada)")
    print()

    print(f"--- {len(PATCHES_UTF16_INPLACE)} trocas in-place (mesmo char count) ---")
    ok = 0
    with open(args.iso, "r+b") as f:
        for abs_off, orig, new in PATCHES_UTF16_INPLACE:
            f.seek(abs_off)
            cur = f.read(len(orig) * 2)
            expected = orig.encode('utf-16-le')
            match = (cur == expected)
            status = "OK" if match else "BYTES NAO BATEM"
            print(f"  0x{abs_off:08x}: '{orig[:30]}...' -> '{new[:30]}'  {status}")
            if match:
                if not args.dry_run:
                    f.seek(abs_off)
                    f.write(new.encode('utf-16-le'))
                ok += 1

        print(f"\n--- {len(PATCHES_SYSMSG_SLOT)} trocas SYSTEM.MSG (slot fixo) ---")
        for abs_off, slot, text in PATCHES_SYSMSG_SLOT:
            print(f"  0x{abs_off:08x} slot={slot}: '{text}'")
            if not args.dry_run:
                patch_sysmsg_slot(f, abs_off, slot, text)

    if args.dry_run:
        print(f"\nDry-run completo. ({ok}/{len(PATCHES_UTF16_INPLACE)} patches in-place validados)")
    else:
        total = ok + len(PATCHES_SYSMSG_SLOT)
        print(f"\nPronto! {total} patches aplicados em {args.iso}")
        print()
        print("=== Onde validar no PCSX2 (em ordem de FACILIDADE) ===")
        print()
        print("[1] TUTORIAL DO GAYAK — assim que ele te der a enxada:")
        print("    Abre o INVENTARIO/ITEMS, seleciona a 'Small Hoe' / Iron Hoe.")
        print("    A descricao mostra:")
        print("       'Uma pequena enxada dada por Gayak.'")
        print("       (no lugar de 'A small hoe given to you by Gayak.')")
        print()
        print("[2] MENU DE PAUSE — em qualquer momento:")
        print("    Aperta Start/Triangle, ve 'Itens' (era 'Items')")
        print("    Em qualquer prompt de confirmacao, 'Anular' (era 'Cancel')")
        print("    Na aba Status, 'Outono' se for outono (uma das estacoes)")
        print()
        print("[3] EM GAMEPLAY (apos fazenda):")
        print("    Porta trancada -> 'Porta trancada!'")
        print("    Bolsa cheia    -> 'Bolsa cheia!'")
        print("    Geladeira      -> 'Voce abre a geladeira.'")

if __name__ == "__main__":
    main()
