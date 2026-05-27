# Briefing — Tradução PT-BR dos arquivos SI_*.DAT (Innocent Life, PS2)

Estes arquivos sao DESCRICOES DE ITENS e textos de MENU. Formato e codec DIFERENTES
dos .SCP — leia com atencao.

## Formato
- Referencia EN (NAO editar): `work/decoded/<slug>.txt`.
- Arquivo a editar: `work/translated/<slug>.txt`.
- Cada bloco:
  ```
  [N|kind=K|chars=CC|...]
  <texto>
  ```
- Voce edita SO a linha de texto. **NUNCA altere a linha de header `[N|...]`.**
- Traduza apenas blocos ainda em ingles (texto == referencia EN). Preserve os que ja estao em PT.

## Regras OBRIGATORIAS
1. **TAMANHO <= chars**: o texto traduzido deve ter no MAXIMO `chars` caracteres. Contagem: cada `<HHLL>` (4 digitos hex entre <>) conta como **1 caractere**; todo o resto conta 1 por caractere. Maior que `chars` = ERRO (o build descarta). Menor e OK (preenchido com espaco). Se a traducao natural nao couber, encurte; se impossivel, deixe em ingles.
2. **SEM ACENTOS / so ASCII** (0x20-0x7E): `a e i o u c` no lugar de acentuados. NUNCA digite acento nem caractere nao-ASCII (cuidado com cirilico que parece latino).
3. **PRESERVE tokens e simbolos especiais EXATAMENTE como aparecem no EN:**
   - `<HHLL>` (ex.: `<0600>`, `<0a00>`) = bytes brutos do engine — copie igual.
   - `%s`, `%d` = placeholders de formato — copie igual, na mesma posicao logica.
   - `^` no inicio (ex.: `^See %s...`) — mantenha o `^`.
   - `▽` = glifo de mapa — mantenha igual (e o unico nao-ASCII permitido).
   - Linhas que sao so `----` (separadores) — NAO traduza, deixe igual.
4. **FRAGMENTOS**: algumas descricoes sao quebradas em varios blocos consecutivos (um `item` seguido de `cont`/`flex`). LEIA os blocos vizinhos na referencia EN para entender a frase inteira e traduza cada fragmento de modo que, lidos em sequencia, formem uma frase natural em PT — respeitando o `chars` de CADA fragmento.
5. **Glossario** (`GLOSSARIO.md` na raiz): use os termos fixos (Enxada, Foice, Regador, Sementes, Bulbos, Galinha, Vaca, Ovelha, Deusa da Colheita, etc.) e NAO traduza nomes proprios (Cluck-o-Matic, Volcano Town, Dr. Hope, Heartflame, etc.).

## Verificacao (rode ao terminar)
`PYTHONIOENCODING=utf-8 python tools/dat_gaps.py <slug>` — confirme `OVERFLOW=0`. Cheque tambem que nao ha caractere nao-ASCII (exceto `▽`) e que os `<HHLL>`/`%s` foram preservados.
