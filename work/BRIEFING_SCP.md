# Briefing — Tradução PT-BR de diálogos .SCP (Innocent Life, PS2)

Você vai traduzir EN→PT-BR um arquivo de diálogo `.SCP` do jogo. O texto fica em
slots de tamanho FIXO. Siga estas regras à risca — elas evitam bugs no jogo.

## Formato do arquivo
- Em `work/scp_decoded/<NOME>.txt` está a REFERÊNCIA em inglês (NÃO editar).
- Em `work/scp_translated/<NOME>.txt` está o arquivo a EDITAR (já vem como cópia EN; muitos blocos podem já estar em PT).
- Cada bloco é:
  ```
  [N|off=0xXXXX|chars=CC]
  <texto do bloco>
  ```
- Você só edita a linha de texto. **NUNCA altere a linha de header `[N|off=...|chars=...]`.**
- Traduza apenas blocos ainda em inglês (ou claramente mal traduzidos). Mantenha os que já estão bons.

## Regras OBRIGATÓRIAS
1. **TAMANHO ≤ chars**: o texto traduzido, contando cada `\n` como **1 caractere**, deve ter no MÁXIMO `chars` caracteres. Maior = o jogo descarta e mostra inglês. Menor é OK (preenchido com espaço). Ex.: `Yes\nNo` tem 7 chars (S,i,m,quebra,N,a,o).
2. **SEM ACENTOS / só ASCII** (0x20–0x7E): `á→a à→a â→a ã→a, é→e ê→e, í→i, ó→o ô→o õ→o, ú→u, ç→c`. NUNCA digite acento. CUIDADO com autocorreção inserindo letras cirílicas que parecem latinas (а, е, о, с, р...).
3. **NUNCA escreva tokens `<XX>`** (ex.: `<06>`, `<02>`). O codec NÃO os interpreta — virariam texto literal ou estourariam. **Importante:** se o texto EN de um bloco começa com a letra `P` solta (ex.: `P!`, `P.`, `P, ...`), esse `P` é o PLACEHOLDER do nome do jogador — MANTENHA o `P` inicial e traduza o resto. O mesmo vale para outras letras isoladas no início (`I`, `J`, `R`) que são ícones de botão. Não adicione tokens.
4. **Quebra de linha = `\n` literal** (barra + n), conta 1 char. As caixas de diálogo são estreitas (~3 linhas curtas); posicione `\n` para caber bem. Mantenha o texto em UMA linha no arquivo, usando `\n` para as quebras.
5. **Glossário** (`GLOSSARIO.md` na raiz): use os termos fixos e NÃO traduza nomes próprios (Gayak, Dr. Hope, Vita, Franco, Moonlight, Volcano Town, Easter/Pascoa, etc.).
6. **Tom de voz por personagem** (o falante vem antes do `:`):
   - Vita (robô assistente): formal-amigável, trata o jogador como "Mestre".
   - Franco: descontraído, fofoqueiro, "amigo de boteco".
   - Moonlight: poético, espiritual, frases curtas.
   - Dr. Hope: científico mas caloroso, paternal.
   - Narrador / texto de sistema: neutro, factual.

## Como verificar você mesmo
Antes de terminar, rode no diretório do projeto:
```
PYTHONIOENCODING=utf-8 python tools/overflow_report.py
```
e confirme que seu arquivo NÃO aparece com OVERFLOW (exceto o caso `Yes\nNo` de chars=6, que é impossível e pode ficar em inglês). Cheque também que não há tokens `<XX>` nem caracteres não-ASCII no que você escreveu.
