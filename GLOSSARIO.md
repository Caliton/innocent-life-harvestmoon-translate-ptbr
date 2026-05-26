# Glossario PT-BR — Innocent Life

Mantenha estes termos consistentes em TODOS os arquivos traduzidos.

## Personagens (NAO TRADUZIR — manter nome original)

| Original | PT-BR | Notas |
|----------|-------|-------|
| Gayak | Gayak | tutor agricola |
| Dr. Hope | Dr. Hope | cientista, criador do protagonista |
| Vita | Vita | robo assistente |
| Franco | Franco | NPC |
| Moonlight | Moonlight | NPC |
| Marco | Marco | NPC |

## Lugares (manter)

| Original | PT-BR |
|----------|-------|
| Volcano Town | Volcano Town |
| Masami's Bar | Bar do Masami |
| Cluck-o-Matic | Cluck-o-Matic |

## Items / Ferramentas

| Original | PT-BR | Notas |
|----------|-------|-------|
| Hoe / Iron Hoe | Enxada / Enxada de Ferro | (iron = ferro) |
| Hammer | Martelo |
| Sickle | Foice |
| Axe | Machado |
| Watering Can | Regador |
| Cart Rails | Trilhos | (sem acento) |
| Seed Box | Caixa de Sementes |
| Bag | Bolsa |

## Animais

| Original | PT-BR |
|----------|-------|
| Chicken | Galinha |
| Cow | Vaca |
| Sheep | Ovelha |
| Cat | Gato |

## Cultivos / Cores

| Original | PT-BR |
|----------|-------|
| Crops | Plantacoes |
| Seeds | Sementes |
| Bulbs | Bulbos |
| Pepino | Pepino |
| Vegetables | Vegetais |
| Fruit | Fruta |
| Flowers | Flores |
| Herb | Erva |
| Mushroom | Cogumelo |

## Estações / Tempo

| Original | PT-BR |
|----------|-------|
| Spring | Prima | (6 chars - encurtar de "Primavera" pra caber em slots menores) |
| Summer | Verao |
| Autumn | Outono |
| Winter | Invern | (6 chars - encurtar) |

## Conceitos do jogo

| Original | PT-BR |
|----------|-------|
| Human Status | Nivel Humano (Status Humano em contexto) |
| Fire Spirit | Espirito do Fogo |
| Nature Sprites | Espiritos da Natureza |
| Harvest Goddess | Deusa da Colheita |

## UI / Botões

| Original | PT-BR | Chars |
|----------|-------|-------|
| Yes | Sim | 3 |
| No | Nao | 3 |
| OK | OK | 2 |
| Cancel | Anular | 6 |
| Back | Voltar (se nao couber: "Trasn") | 4-6 |
| Save | Salvar (se nao couber: "Grava") | 5-6 |
| Load | Carrega | 7 |
| Start | Iniciar (se nao couber: "Comec") | 5-7 |
| Quit | Sair | 4 |
| Items | Itens | 5 |
| Map | Mapa (se nao couber: "Map") | 3-4 |
| Status | Status | 6 |
| Volume | Volume | 6 |
| Normal | Normal | 6 |

## Tom de voz

- **Vita** (robo assistente): formal-mas-amigavel, trata o player como "Mestre <06>P"
- **Franco**: descontraido, fofoqueiro, tom de "amigo de boteco"
- **Moonlight**: poetico, espiritual, frases curtas e diretas
- **Dr. Hope**: cientifico mas caloroso, paternal
- **Narrador** (mensagens do sistema): neutro, factual

## Limitacoes tecnicas

- **SEM ACENTOS**: a fonte do jogo so tem ASCII. Substitua `ã→a, ç→c, é→e, ô→o`. Use "voce" no lugar de "você", "nao" no lugar de "não", "atras" em vez de "atrás", etc.
- **CHAR COUNT EXATO**: cada string tem header `chars=N`. A traducao PT precisa ter EXATAMENTE N chars. PT mais curto pode ser preenchido com espacos (faz isso automaticamente, mas tente caber natural). PT mais longo = ERRO.
- **TOKENS — NAO TRADUZIR**:
  - `<06>P` = nome do jogador (placeholder)
  - `<0002>`, `<02>`, `<08>`, `<03>`, etc = bytes de controle do engine
  - `<XXXX>` (4 dig hex) = 2 bytes brutos = conta como 1 char UTF-16
  - `<XX>` (2 dig hex) = 1 byte de controle = conta como 1 char UTF-16
  - `\n` = quebra de linha literal (2 chars: barra + n)

## Exemplos de estilo

**Original**: `<0002><08><02>Franco: So you've finally started\nraising livestock, eh?<02>\n`
**PT**: `<0002><08><02>Franco: Entao voce finalmente comecou\na criar gado, hein?<02>\n`

**Original**: `<0002>This door is locked!<02>\n`
**PT**: `<0002>Porta trancada!<02>\n`  (cabe no slot 48)

**Original**: `A small hoe given to you by Gayak.` (34 chars)
**PT**: `Uma pequena enxada dada por Gayak.` (34 chars EXATOS)
