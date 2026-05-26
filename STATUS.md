# Innocent Life PT-BR — STATUS

Projeto de traducao para PT-BR de "Innocent Life: A Futuristic Harvest Moon - Special Edition" (PS2, NTSC-U, SLUS-216.41).

## Estado atual

- POC validada: troca de strings em SYSTEM.MSG, SI_LT00.DAT, SI_MN00.DAT funciona no PCSX2.
- Pipeline completo de extracao/build operacional.
- ~2,500 strings traduziveis identificadas (~65,000 chars).

## Volume de texto identificado

| Arquivo | Strings | Conteudo |
|---------|---------|----------|
| `SYSTEM.MSG` | 715 mensagens | Dialogos, UI, dicionario do jogo |
| `SI_LT00.DAT` | 1647 strings | Descricoes de itens |
| `SI_LT0~1.DAT` | ~1000 strings | (variantes) |
| `SI_MN00.DAT` | 172+ strings | Menu de pause/status |
| `SI_MN0~1.DAT` | poucas | Submenu |
| `SI_MN0~2.DAT` | 172 strings | Duplicata de SI_MN00.DAT |
| `SI_DB00.DAT` | 163 strings | Categorias |
| `SLUS_216.41` | 74 strings | UI hardcoded no exe |

## Formato

- **SYSTEM.MSG**: count + tabela `(uint32 offset, uint32 msgid)` + strings UTF-16 LE em slot fixo. Cada slot: `<0002> + UTF-16 + <0002> + <000a> + padding null`.
- **SI_*.DAT** (magic `MN01`): strings UTF-16 LE precedidas de header com length explicito. Tres tipos:
  - `01 00 05 42 00 00 00 00 ID LL` (item start, 12B header, com ID)
  - `01 00 05 40 00 00 LL` (continuation, 8B header)
  - `05 40 00 00 LL` (flex, 6B header)
  LL = char count uint16 LE. String tem LL*2 bytes.

## Pipeline (workflow)

```
1_extrair.bat                                 (uma vez)
  -> work/original/   binarios extraidos
  -> work/decoded/    .txt com texto EN original (referencia)
  -> work/translated/ .txt para editar (copia do decoded)

(edita work/translated/*.txt)

2_aplicar.bat
  -> copia ISO original pra InnocentLife_PT.iso
  -> aplica patches in-place
  -> testar no PCSX2
```

## Regras importantes

- Mantenha o tamanho exato dos slots. Para `SYSTEM.MSG`, nao ultrapasse o tamanho do slot original. Para `SI_*.DAT`, mantenha EXATAMENTE o mesmo `chars=N` no header (PT menor preenche com espacos automaticamente; PT maior da erro).
- Sem acentos (a fonte do jogo so tem ASCII por default).
- Tokens `<XX>` (1 byte) e `<HHLL>` (2 bytes) sao bytes brutos do engine — NAO traduzir, manter.
- `\n` literal de 2 chars (`\` + `n`) representa quebra de linha. Mantenha onde fazia sentido.
- `<06>P` = nome do jogador (placeholder). Deixe como esta.

## Arquivos do projeto

```
ilhm/
  Innocent Life ... (USA).iso       # original (NAO MEXER)
  InnocentLife_PT.iso               # ISO traduzida (gerada pelo 2_aplicar.bat)
  1_extrair.bat                     # passo 1
  2_aplicar.bat                     # passo 2
  STATUS.md                         # este arquivo
  tools/
    ilhm_codec.py                   # parsers UTF-16, SYSTEM.MSG e MN01
    ilhm_extract.py                 # ISO -> work/decoded/*.txt
    ilhm_build.py                   # work/translated/*.txt -> ISO PT
    poc_patch.py                    # POC standalone (validado)
  work/
    original/                       # binarios extraidos da ISO
    decoded/                        # .txt EN original (NAO editar)
    translated/                     # .txt editaveis (vira PT)
    lba_map.txt                     # offsets dos arquivos na ISO
```

## Diferencas vs Wonderful Life

| Aspecto | WL | IL |
|---------|----|----|
| Encoding | Tilemap custom | UTF-16 LE puro |
| Container | AFS + .mes + DAT TOC | MN01 + slot fixo |
| Total strings | ~22,400 | ~2,500 |
| Acentos | nao (font hack necessario) | nao (font hack necessario) |
| Engine quirks | Yes/No bug, slot rigido | Aparentemente permissivo |

## Proximos passos

1. Decidir se vale fazer font hacking pra acentos PT (otherwise PT sem acento como WL).
2. Escalar traducao das 2,500 strings via agentes (similar ao WL Grupos A-D).
3. QA passes em PCSX2.

## POC validada

- "Items" -> "Itens" no menu de pause ✓
- "Cancel" -> "Anular" em confirmacoes ✓
- "Autumn" -> "Outono" em Status ✓
- "A small hoe given to you by Gayak." -> "Uma pequena enxada dada por Gayak." ✓
- "This door is locked!" -> "Porta trancada!" ✓
- "Bolsa cheia!" / "Voce abre a geladeira." ✓
