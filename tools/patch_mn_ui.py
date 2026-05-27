#!/usr/bin/env python3
"""
patch_mn_ui.py - Corrige strings de UI (status/menu) que o scan_mn01 NAO extraiu
de SI_MN00.DAT / SI_MN0~2.DAT. Faz patch por byte direto na ISO, preservando as
demais traducoes (so casa o padrao <chars LE><string EN><...>, que so existe onde
a label ainda esta em ingles).

Cada PT deve ter <= len(EN) chars; e preenchido com espaco ate len(EN) (mesmo
numero de bytes), entao o tamanho do arquivo nao muda.

Uso:
  python tools/patch_mn_ui.py --iso InnocentLife_PT.iso          # dry-run (valida)
  python tools/patch_mn_ui.py --iso InnocentLife_PT.iso --apply
"""
import argparse, struct, sys, io
import pycdlib

# EN -> PT (PT deve ter <= len(EN); padding com espaco e automatico).
# Entradas omitidas ou PT==EN ficam em ingles (ex.: nomes de 3 chars sem PT que caiba).
T = {
    # descricoes de robos (1a linha; o scanner so pegou as continuacoes)
    'This makes your maximum PP': 'Torna seu PP maximo',
    'The robot will remove unnecessary things': 'O robo remove coisas desnecessarias',
    'The robot will collect materials such': 'O robo ira coletar materiais',
    'The robot will prepare the soil for': 'O robo prepara o solo',
    'This helps prevent you from getting': 'Ajuda a evitar que voce fique',
    'This helps you regain energy faster': 'Ajuda a recuperar energia rapido',
    'Send Seeds to Seed Box': 'Enviar a Caixa Sement.',
    'Total Amount Made': 'Total Produzido',
    'Individual Price': 'Preco Individual',
    'Put in the Trash': 'Jogar no Lixo',
    'Take out of Bag': 'Tirar da Bolsa',
    'Highest Price': 'Maior Preco',
    'Selling Price': 'Preco Venda',
    'Fishing Pole': 'Vara Pesca',
    'Intelligence': 'Inteligencia',
    'Watering Can': 'Regador',
    'Days Raised': 'Dias Criado',
    'Human Level': 'Niv. Humano',
    'Player Info': 'Perfil',
    'SP Obtained': 'SP Obtido',
    'Set in This': 'Encaixar',
    'Total Price': 'Preco Total',
    ' more days': ' mais dias',
    'Creativity': 'Criacao',
    'Times Made': 'Qtd. Feito',
    'Tool Skill': 'Hab. Ferr.',
    'Until Next': 'P/ Proximo',
    'Challenge': 'Desafio',
    'Happiness': 'Alegria',
    'PP Used: ': 'PP Usado:',
    'Tool Lvl ': 'Niv. Ferr',
    'more days': 'mais dias',
    ' per use': ' por uso',
    'Contents': 'Conteudo',
    'Equipped': 'Equipado',
    'PP Used:': 'PP Usado',
    'View Map': 'Ver Mapa',
    'Cooking': 'Cozinha',
    'Setting': 'Config.',
    'Shipped': 'Enviado',
    'squares': 'campos',
    ' to go': ' resta',
    'Hammer': 'Martel',
    'Normal': 'Normal',
    'Sickle': 'Foice',
    'Status': 'Status',
    'Weight': 'Peso',
    'Humor': 'Humor',
    'Model': 'Tipo',
    'Money': 'Grana',
    'Price': 'Preco',
    'Back': 'Sair',
    'Day ': 'Dia ',
    'Days': 'Dias',
    'Good': 'Bom',
    'Love': 'Amor',
    'Mood': 'Veia',
    'Name': 'Nome',
    'Next': 'Prox',
    'None': 'Nada',
    'Ring': 'Anel',
    'Save': 'Salv',
    'Tool': 'Ferr',
    'Bad': 'Mal',
    'Day': 'Dia',
    'Lv': 'Nv',
    # mantidos em EN (sem PT que caiba): 'Hoe', 'Axe', 'PP', 'MAX!'
}

DAT_FILES = [
    ('/DATAIMG/MENU/FORM/SI_MN00.DAT;1', 0x403c6800),
    ('/DATAIMG/MENU/FORM/SI_MN0~2.DAT;1', 0x403cd000),
]
SECTOR = 2048

def patch_bytes(data: bytearray):
    n = 0; errs = []
    for en, pt in T.items():
        if pt == en:
            continue
        if len(pt) > len(en):
            errs.append(f'{en!r}: PT {len(pt)} > {len(en)}'); continue
        needle = struct.pack('<H', len(en)) + en.encode('utf-16-le')
        padded = (pt + ' ' * (len(en) - len(pt))).encode('utf-16-le')
        repl = struct.pack('<H', len(en)) + padded
        start = 0
        while True:
            idx = data.find(needle, start)
            if idx < 0: break
            data[idx:idx+len(needle)] = repl
            n += 1; start = idx + len(repl)
    return n, errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--iso', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    # valida tamanhos
    bad = [f'{en!r}: PT {len(pt)} > EN {len(en)}' for en, pt in T.items() if pt != en and len(pt) > len(en)]
    if bad:
        print('ERRO de tamanho:'); [print('  ', b) for b in bad]; sys.exit(1)

    iso = pycdlib.PyCdlib(); iso.open(args.iso)
    total = 0
    writes = []
    for path, off in DAT_FILES:
        b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=path)
        data = bytearray(b.getvalue())
        orig_len = len(data)
        n, errs = patch_bytes(data)
        assert len(data) == orig_len, 'tamanho mudou!'
        total += n
        print(f'  {path}: {n} ocorrencias patcheadas')
        writes.append((off, bytes(data)))
    iso.close()

    if args.apply:
        with open(args.iso, 'r+b') as f:
            for off, data in writes:
                f.seek(off); f.write(data)
        print(f'APLICADO: {total} patches na ISO')
    else:
        print(f'(dry-run) {total} patches seriam aplicados. Use --apply.')

if __name__ == '__main__':
    main()
