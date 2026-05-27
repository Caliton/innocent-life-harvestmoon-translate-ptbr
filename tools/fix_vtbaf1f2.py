#!/usr/bin/env python3
"""Fix overflows in VTBAF1F2.SCP.txt - apply all corrections"""
import re

def count_text(text):
    count = 0
    i = 0
    while i < len(text):
        if text[i:i+2] == r'\n':
            count += 1
            i += 2
        else:
            count += 1
            i += 1
    return count

# All corrections - carefully sized to fit within char limits
# Format: idx -> new PT text
fixes = {
    11: 'Franco: So brincando.\\nDr. Hope me mataria se\\ndanificasse aquele robo.',
    # 11: chars=87, this text=73 OK
    12: 'Franco: Entao voce\\nfinalmente criou\\nanimais, hein?',
    # 12: chars=56, this text=46 OK
    16: 'Moonlight: O balido dos animais\\npode ser ouvido\\nentre essas ruinas!',
    # 16: chars=74, =71 OK
    17: 'Moonlight: Sua forca vital\\najudara a revitalizar\\nesta terra!',
    # 17: chars=90, =62 OK
    19: 'Franco: Se eu tivesse um buggy,\\nlevaria a Rose num passeio\\ninesquecivel!',
    # 19: chars=89, =75 OK
    22: 'Moonlight: Com esse buggy\\nvoce pode ir\\na quase qualquer lugar!',
    # 22: chars=63, =63 OK
    24: 'Franco: Quando jovem, todos\\nlevavam paqueras\\na essa caverna.',
    # 24: chars=73, =62 OK
    28: 'Franco: Ouvi que voce\\nplantou poinsettias.',
    # 28: chars=49, =41 OK
    30: 'Franco: Nao vejo\\na hora!',
    # 30: chars=21, =21 OK exact
    32: 'Franco: Sei que esta preocupado\\ncom ele, mas tem trabalho\\nimportante a terminar.',
    # 32: chars=96, =83 OK
    33: 'Franco: A melhor coisa para\\no Dr. Hope e ver o quanto\\nvoce esta trabalhando.',
    # 33: chars=89, =73 OK
    34: 'Moonlight: Nunca soube\\nque Dr. Hope\\nestava doente...',
    # 34: chars=52, =52 OK exact
    35: 'Moonlight: Por isso ele\\ncorria tanto para\\nterminar com voce...',
    # 35: chars=86, =67 OK
    36: 'Franco: Sei que voce\\nesta triste, Hope,',
    # 36: chars=42, F-r-a-n-c-o-:-space=8, S-e-i-space-q-u-e-space-v-o-c-e=12, \n=1, e-s-t-a-space-t-r-i-s-t-e-,-space-H-o-p-e-,=18 = 8+12+1+18=39 OK
    37: 'P. Eu tambem.',
    # 37: chars=12, =13. Need <=12. "P. Tambem." = 10 OK
    41: 'Moonlight: O que quero dizer\\ne que Dr. Hope\\nsempre estara com voce,',
    # 41: chars=91, =70 OK
    44: 'Franco: Nao devemos\\nnos preocupar\\ndemais com isso.',
    # 44: chars=61, =50 OK
    45: 'Franco: Um alien\\nmorando no\\nnovo quarto?',
    # 45: chars=43, =42 OK
    47: 'Franco: Nao devemos\\nnos preocupar\\ndemais com isso.',
    # 47: chars=61, =50 OK
    53: 'Jonathan: Sou Jonathan Branch.\\nCuido da fazenda\\nna colina.',
    # 53: chars=61, =61 OK exact
    57: 'Jonathan: Criar animais\\nnos lembra\\ndo nosso lugar na natureza.',
    # 57: chars=97, =56 OK
    62: 'P.\\nSou a Nana.',
    # 62: chars=18, P+.+\n+Sou+space+a+space+Nana+. = 1+1+1+3+1+1+1+4+1=14 OK
    63: 'Nana: Adoraria te convidar,\\nmas temo que voce nao\\ntem idade suficiente.',
    # 63: chars=92, =72 OK
    66: 'Masami: Oh, voce deve ser',
    # 66: chars=24, M-a-s-a-m-i-:-space-O-h-,-space-v-o-c-e-space-d-e-v-e-space-s-e-r = 25 OVER. "Masami: Oh, deve ser" = 20 OK
    68: 'Masami: Oh, voce deve ser',
    # same
    70: 'Masami: O velho Franco\\nfala muito de voce.',
    # 70: chars=41, M+a+s+a+m+i+:+sp=8, O+sp+v+e+l+h+o+sp+F+r+a+n+c+o=14, \n=1, f+a+l+a+sp+m+u+i+t+o+sp+d+e+sp+v+o+c+e+.=19 = 8+14+1+19=42 OVER. "Masami: O Franco\\nfala muito de voce." = 8+8+1+19=36 OK
    71: 'Masami: O velho Franco\\nfala muito de voce.',
    74: 'Masami: Hihihi.\\nEle e fofo.',
    # 74: chars=29, M+a+s+a+m+i+:+sp=8, H+i+h+i+h+i+.=7, \n=1, E+l+e+sp+e+sp+f+o+f+o+.=11 = 8+7+1+11=27 OK
    75: 'Masami: Hihihi.\\nEle e fofo.',
    86: 'Masami: Acredito que plantas\\ntem alma. Observe e\\nadivinhe o que pensam.',
    # 86: chars=113, =72 OK
    87: 'Masami: Acredito que plantas\\ntem alma. Observe e\\nadivinhe o que pensam.',
    103: 'P.\\nSou a Nana.',
    105: 'P.\\nSou a Nana.',
    108: 'Nana: Nunca se sabe\\nque pessoas\\nvoce vai encontrar.',
    # 108: chars=53, =51 OK
    109: 'Nana: Nunca se sabe\\nque pessoas\\nvoce vai encontrar.',
    110: 'Gallion: Voce deve ser',
    # 110: chars=21, G+a+l+l+i+o+n+:+sp+V+o+c+e+sp+d+e+v+e+sp+s+e+r=22 OVER. "Gallion: Deve ser" = 18 OK
    112: 'Gallion: Masami e minha esposa,\\nnao tenha ideias erradas\\nsobre ela. Hahaha!',
    # 112: chars=81, =78 OK
    113: 'Gallion: Queria que meu filho\\nMillion achasse\\numa boa mulher.',
    # 113: chars=77, =63 OK
    115: 'Max: Me preocupo tanto com\\nminha esposa aqui que\\npasso todo dia.',
    # 115: chars=101, =65 OK
    121: 'Jonathan: Sou Jonathan Branch.\\nCuido da fazenda\\nna colina.',
    125: 'Lionel: Estou entediado...\\nQueria uma erupcao.\\nSeria diferente.',
    # 125: chars=95, =65 OK
    129: 'Bobby: Ensino na Escola\\nde Volcano Town.\\nApareca quando quiser.',
    # 129: chars=68, =61 OK
    130: 'Masami: Mesmo trabalhando,\\nsempre preparo o almoco\\npara meu marido.',
    # 130: chars=82, =69 OK
    141: 'Jonathan: Os participantes\\nsao todos mais velhos,\\nnao e divertido pra crianca.',
    # 141: chars=106, =76 OK
    142: 'Jonathan: Estou impressionado.\\nUma fazenda inteira\\nnas Ruinas sozinho...',
    # 142: chars=113, =72 OK
    149: 'P.\\nSou Dorothy,\\nesposa do prefeito.',
    # 149: chars=33, P+.=2, \n=1, S+o+u+sp+D+o+r+o+t+h+y+,=12, \n=1, e+s+p+o+s+a+sp+d+o+sp+p+r+e+f+e+i+t+o+.=19 = 2+1+12+1+19=35 OVER. "P.\\nSou Dorothy,\\nesposa prefeito." = 2+1+12+1+16=32 OK
    153: 'Jonathan: Uma galinha robo\\najuda a manter\\nas galinhas na linha.',
    # 153: chars=78, =65 OK
    159: 'Jonathan: Criar animais\\nnos lembra\\ndo nosso lugar na natureza.',
    # 159: chars=97, =56 OK
    163: 'Nana: Quero ganhar o Concurso\\nde Cozinha de Cogumelos.\\nNao consigo com normais...',
    # 163: chars=109, =83 OK
    164: 'Nana: Voce poderia pegar\\nalgunos Porcinis pra mim?\\nDevem estar na epoca amanha.',
    # 164: chars=111, =77 OK
    166: 'Nana: Vejamos... 100g\\ndeve ser suficiente.',
    # 166: chars=49, =42 OK
    175: 'Nana: Acho que ela cozinha\\nmelhor do que eu.',
    # 175: chars=53, =46 OK
    176: 'Nana: Acho que ela cozinha\\nmelhor do que eu.',
    184: 'Gallion: Pedi ao meu filho\\npara pedir Areia Poder\\ne sementes de ervas.',
    # 184: chars=82, =71 OK
    188: 'Masami: Com tanta fumaca,\\nos Espiritos da Natureza\\nnao chegam a caverna.',
    # 188: chars=99, =73 OK
    189: 'Masami: Com tanta fumaca,\\nos Espiritos da Natureza\\nnao chegam a caverna.',
    196: 'Masami: Talvez te\\nchamando para\\na Floresta Gigante.',
    # 196: chars=54, =52 OK
    197: 'Masami: Talvez te\\nchamando para\\na Floresta Gigante.',
    201: 'Dorothy: Oh, fico feliz\\nque veio,\n',
    # 201: chars=32, D-o-r-o-t-h-y-:-sp=9, O-h-,-sp-f-i-c-o-sp-f-e-l-i-z=14, \n=1, q-u-e-sp-v-e-i-o-,=9, \n=1 = 9+14+1+9+1=34 OVER.
    # "Dorothy: Oh, que bom\\nque veio,\n" = 9+12+1+9+1=32 OK
    203: 'Dorothy: Ja assistiu meu\\nprograma de TV,\\nVida de Cozinha?',
    # 203: chars=56, =57 STILL OVER. count: D-o-r-o-t-h-y-:-sp=9, J-a-sp-a-s-s-i-s-t-i-u-sp-m-e-u=15, \n=1, p-r-o-g-r-a-m-a-sp-d-e-sp-T-V-,=15, \n=1, V-i-d-a-sp-d-e-sp-C-o-z-i-n-h-a-?=16 = 9+15+1+15+1+16=57 OVER
    # "Dorothy: Ja assistiu\\nprograma TV,\\nVida de Cozinha?" = 9+12+1+12+1+16=51 OK
    207: 'Masami: O tempo voa. Mal posso\\nacreditar que e hora da\\nFesta de Natal de novo.',
    # 207: chars=106, =74 OK
    208: 'Masami: O tempo voa. Mal posso\\nacreditar que e hora da\\nFesta de Natal de novo.',
    209: 'Masami: Prepare-se tambem.\\nO prefeito so compra\\npoinsettias pro Prefeit...',
    # 209: chars=109, =75 OK
    210: 'Masami: Prepare-se tambem.\\nO prefeito so compra\\npoinsettias pro Prefeit...',
    220: 'Gallion: Sao Sementes Poinsettia.\\nCresce\\nate no Invern.',
    # 220: chars=68, =55 OK
    225: 'Lionel: Estou entediado...\\nQueria que aliens\\naparecessem...',
    # 225: chars=54, =54 STILL OVER. count: L+8+sp=9, E+s+t+o+u+sp+e+n+t+e+d+i+a+d+o+...=19, \n=1, Q+u+e+r+i+a+sp+q+u+e+sp+a+l+i+e+n+s=17, \n=1, a+p+a+r+e+c+e+s+s+e+m+...=12 = 9+19+1+17+1+12=59 OVER
    # "Lionel: Estou\\nentediado...\\nQueria aliens!" = 7+5+1+12+1+14=40 OK
    226: 'Lionel: Estou\\nentediado...\\nEi,',
    # 226: chars=28, = 7+5+1+12+1+3=29 OVER. "Lionel: Entediado\\nEi," = 7+9+1+3=20 OK
    233: 'Masami: Arranjo floral da\\npaz interior... mas\\nvoce prefira pescar.',
    # 233: chars=86, =65 OK
    234: 'Masami: Arranjo floral da\\npaz interior... mas\\nvoce prefira pescar.',
    236: 'Lucia: Arranjo floral e dificil.\\nMeu marido deveria\\ninventar um automatico...',
    # 236: chars=112, =75 OK
    240: 'Gallion: Ho ho...\\nArranjo floral da Masami\\nesta cheio.',
    # 240: chars=64, =52 OK
    243: 'Liberta: Por isso\\nnao me importo\\nde beber no bar dela.',
    # 243: chars=45, =53 OVER. count: L+8+sp=9, P+o+r+sp+i+s+s+o=8, \n=1, n+a+o+sp+m+e+sp+i+m+p+o+r+t+o=14, \n=1, d+e+sp+b+e+b+e+r+sp+n+o+sp+b+a+r+sp+d+e+l+a+.=21 = 9+8+1+14+1+21=54 OVER
    # Need <=45. "Liberta: Nao me\\nimporto de beber\\nno bar dela." = 9+6+1+14+1+12=43 OK
    244: 'Masami: Desculpe, estou\\nocupada com minha\\naula de haiku.',
    # 244: chars=61, =55 OK
    245: 'Masami: Desculpe, estou\\nocupada com minha\\naula de haiku.',
    252: 'P.\\nTalvez nao queira\\nautomatizar a fazenda, mas...',
    # 252: chars=62, =50 OK
    253: 'Jonathan: Seria divertido\\ntestar os Trilhos\\num dia.',
    # 253: chars=50, =50 OK exact
    260: 'P? Nao esqueca\\nde usar palavra da estacao.',
    # 260: chars=44, P+?+sp+N+a+o+sp+e+s+q+u+e+c+a=14, \n=1, d+e+sp+u+s+a+r+sp+p+a+l+a+v+r+a+sp+d+a+sp+e+s+t+a+c+a+o+.=27 = 14+1+27=42 OK
    262: 'P? Nao esqueca\\nde usar palavra da estacao.',
    265: 'Franco: "Pegue um kewpie\\nde a ele um ukulele.\\nE uma roquestar."',
    # 265: chars=69, =65 OK
    267: 'Liberta: Precisa educacao\\npara apreciar\\no vinho de verdade.',
    # 267: chars=62, =58 OK
    268: 'Liberta: Por isso estou aqui.\\nNao so para\\nolhar Masami...',
    # 268: chars=68, =60 OK
    275: 'Jessica: "E uma primerose?\\nOu uma flor de lotus?\\nNao, e amor-perfeito."',
    # 275: chars=73, =73 OK exact
    278: 'Gallion: Ho ho.\\nAula de haiku\\nda Masami esta cheia.',
    # 278: chars=51, =51 OK exact
    279: 'Gallion: Franco so\\nescreve haiku\\nbobos.',
    # 279: chars=45, =41 OK
    282: 'Franco: "Observe a cadente.\\nNao brigue se ela\\nnao realizar o desejo."',
    # 282: chars=84, =72 OK
    284: 'Liberta: Precisa educacao\\npara apreciar\\no vinho de verdade.',
    285: 'Liberta: Por isso estou aqui.\\nNao so para\\nolhar Masami...',
    286: 'Liberta: "Bam bam bam bam\\nBam bam bam bam bam bam\\nBombos da Prima."',
    # 286: chars=81, =70 OK
    288: 'Jessica: "Mancha maquiagem\\nna toalha que usei\\nna testa suada."',
    # 288: chars=74, =65 OK
    293: 'Gallion: Ho ho.\\nAula de haiku\\nda Masami esta cheia.',
    294: 'Gallion: Franco so\\nescreve haiku\\nbobos.',
    299: 'Liberta: Precisa educacao\\npara apreciar\\no vinho de verdade.',
    300: 'Liberta: Por isso estou aqui.\\nNao so para\\nolhar Masami...',
    301: 'Liberta: "Nem folhas Outono\\nsao tao vermelhas\\nquanto meu extrato."',
    # 301: chars=79, =70 OK
    308: 'Gallion: Ho ho.\\nAula de haiku\\nda Masami esta cheia.',
    309: 'Gallion: Franco so\\nescreve haiku\\nbobos.',
    310: 'Franco: "Mulheres lindas\\ncultivam melhores\\npoinsettias. Nao acha?"',
    # 310: chars=79, =70 OK
    316: 'Franco: As vezes gosto\\nde escrever haiku\\nserio tambem...',
    # 316: chars=54, =56 OVER. "Franco: Gosto de\\nescrever haiku\\nserio tambem..." = 8+8+1+14+1+15=47 OK
    319: 'Liberta: Precisa educacao\\npara apreciar\\no vinho de verdade.',
    320: 'Liberta: Por isso estou aqui.\\nNao so para\\nolhar Masami...',
    321: 'Liberta: "Oh frigideira negra,\\nvoce deve cozinhar,\\nnao ser arma."',
    # 321: chars=80, =67 OK
    323: 'Gallion: "Uma pegadinha.\\nSai de boneco de neve\\nmas todos desmaiaram."',
    # 323: chars=78, =70 OK
    324: 'Gallion: "Cachecol que aquece\\npreso na porta\\ntambem enforca voce."',
    # 324: chars=84, =69 OK
    325: 'Gallion: Ho ho.\\nAula de haiku\\nda Masami esta cheia.',
    326: 'Jessica: Haiku e\\nprofundo! Tenho\\ntanto a aprender.',
    # 326: chars=51, =48 OK
    327: 'Jessica: "Amar e ser amado.\\nSonho de qualquer mulher.\\nE de qualquer homem."',
    # 327: chars=72, =77 OVER. "Jessica: \"Amar e ser amado,\nsonho de mulher\ne de homem.\"" = 8+19+1+15+1+10=54 OK
    328: 'Jessica: Espera, nao tem\\npalavra de estacao\\nnisso...',
    # 328: chars=54, =53 OK
    329: 'Masami: Lenny faz jantar\\nnos Domingos.\\nE uma grande ajuda.',
    # 329: chars=64, =59 OK
    330: 'Masami: Lenny faz jantar\\nnos Domingos.\\nE uma grande ajuda.',
    336: 'Franco: "Cortando a grama,\\numa pausa de duas horas\\nse passou..."',
    # 336: chars=64, =66 OVER. "Franco: \"Cortando a grama,\numa pausa, duas horas\nse passou...\"" = 8+20+1+21+1+14=65 OVER
    # "Franco: \"Cortando grama,\numa pausa, duas horas\nse passou...\"" = 8+16+1+21+1+14=61 OK
    340: 'Jessica: "Sapatos novos,\\narruinados por uma crianca\\nnum dia de chuva..."',
    # 340: chars=76, =72 OK
    342: 'Franco: "Sou pescador,\\no ceu de jantar\\ne de cavalinha..."',
    # 342: chars=50, =57 OVER. "Franco: \"Sou pescador,\nceu de cavalinha...\"" = 8+13+1+19=41 OK
    344: 'Liberta: "Noite de Outono,\\nCantabile vai\\nsaborear o vinho..."',
    # 344: chars=61, =64 OVER. "Liberta: \"Noite Outono,\nCantabile vai\nsaborear vinho...\"" = 8+14+1+14+1+15=53 OK
    347: 'Jessica: Ah~!\\nEstou com\\nfome...',
    # 347: chars=35, =34 OK
    348: 'Liberta: "Com roupas vintage,\\nhibernar ate\\nficarem frescas..."',
    # 348: chars=63, =63 OK exact
    350: 'Jessica: "Velha Mulher de Neve\\nnunca tricotou\\num sueter sequer..."',
    # 350: chars=62, =66 OVER. "Jessica: \"Velha Mulher Neve\nnunca tricotou\num sueter...\"" = 8+19+1+14+1+12=55 OK
    353: 'P!\\nVoce me ajudou\\na ganhar!',
    # 353: chars=21, P+!=2, \n=1, V+o+c+e+sp+m+e+sp+a+j+u+d+o+u=14, \n=1, a+sp+g+a+n+h+a+r+!=9 = 2+1+14+1+9=27 OVER
    # "P!\\na ganhar!" = 2+1+9=12 OK - but original is 21 chars, so we have room: "P!\\nMuito obrigada!" = 2+1+16=19 OK
    354: 'Nana: Hm... Pensei que\\nessa vez\\nia ganhar...',
    # 354: chars=55, N-a-n-a-:-sp=6, H-m-...-sp-P-e-n-s-e-i-sp-q-u-e=15, \n=1, e-s-s-a-sp-v-e-z=8, \n=1, i-a-sp-g-a-n-h-a-r-...=10 = 6+15+1+8+1+10=41 OK
    357: 'Max: Como gratidao,\\nmandei algo\\na sua Caixa de Itens!',
    # 357: chars=83, =54 OK
    360: 'Sharon: Essas trufas negras\\ncheiraram\\nmaravilhosamente...',
    # 360: chars=53, S-h-a-r-o-n-:-sp=8, E-s-s-a-s-sp-t-r-u-f-a-s-sp-n-e-g-r-a-s=19, \n=1, c-h-e-i-r-a-r-a-m=9, \n=1, m-a-r-a-v-i-l-h-o-s-a-m-e-n-t-e-...=17 = 8+19+1+9+1+17=55 OVER
    # "Sharon: Trufas negras\\ncheiraram\\nmaravilhosamente..." = 8+13+1+9+1+17=49 OK
    366: 'Charles: Nana ganhou o\\nConcurso de Cogumelos\\ncom seus Porcinis.',
    # 366: chars=82, =64 OK
    367: 'Charles: Sharon ganhou o\\nConcurso de Cogumelos\\ncom trufas negras.',
    # 367: chars=81, =66 OK
    368: 'Charles: Dorothy ganhou o\\nConcurso de\\nCogumelos deste ano.',
    # 368: chars=58, =58 OK exact
    377: 'Dorothy: Os Porcinis da Nana\\nficaram perfeitos\\nno molho. Delicioso.',
    # 377: chars=85, =70 OK
    379: 'Dorothy: Fico feliz que\\ntodos se divertiram.\\nCozinhar deve ser divertido.',
    # 379: chars=71, D+8=9, F-i-c-o-sp-f-e-l-i-z-sp-q-u-e=14, \n=1, t-o-d-o-s-sp-s-e-sp-d-i-v-e-r-t-i-r-a-m-.=20, \n=1, C-o-z-i-n-h-a-r-sp-d-e-v-e-sp-s-e-r-sp-d-i-v-e-r-t-i-d-o-.=29 = 9+14+1+20+1+29=74 OVER
    # "Dorothy: Fico feliz.\\nTodos se divertiram.\\nCozinhar e diversao." = 9+12+1+20+1+19=62 OK
    380: 'Franco: Nao e legal\\ntodo mundo cozinhar\\njunto uma vez por ano?',
    # 380: chars=89, =62 OK
    387: 'Historia Rosa Branca Vol2',
    # 387: chars=25, =25 OK exact
    388: 'Masso reprovou\\nno exame da cidade\\nde novo...',
    # 388: chars=52, =47 OK
    403: 'Becky: Mas que rosa\\nfloresce\\nno Invern...',
    # 403: chars=57, =43 OK
    406: 'Historia Rosa Branca\\nVol.2,',
    # 406: chars=25, H-i-s-t-o-r-i-a-sp-R-o-s-a-sp-B-r-a-n-c-a=20, \n=1, V-o-l-.-2-,=6 = 20+1+6=27 OVER
    # "Rosa Branca\\nVol.2," = 11+1+6=18 OK
    408: 'Ha um cartao preso\\nentre as portas\\ndo elevador.',
    # 408: chars=54, =50 OK
    410: 'Esta torto, como se\\nescrito pela\\nmao esquerda.',
    # 410: chars=40, E-s-t-a-sp-t-o-r-t-o-,-sp-c-o-m-o-sp-s-e=19, \n=1, e-s-c-r-i-t-o-sp-p-e-l-a=12, \n=1, m-a-o-sp-e-s-q-u-e-r-d-a-.=13 = 19+1+12+1+13=46 OVER
    # "Esta torto, escrito\\npela mao\\nesquerda." = 18+1+8+1+9=37 OK
    413: 'Marcia: OK, entao.',
    # 413: chars=17, = M+a+r+c+i+a+:+sp=8+O+K+,+sp+e+n+t+a+o+.=9 = 8+9=17 OK exact (removed the lowercase 'k')
    414: 'Marcia: Estivemos\\nesperando,\n',
    # 414: chars=36, M+8=9, E-s-t-i-v-e-m-o-s=9, \n=1, e-s-p-e-r-a-n-d-o-,=10, \n=1 = 9+9+1+10+1=30 OK
    417: 'P.\\nFecha os olhos\\num segundo...',
    # 417: chars=31, P+.=2, \n=1, F+e+c+h+a+sp+o+s+sp+o+l+h+o+s=14, \n=1, u+m+sp+s+e+g+u+n+d+o+...=11 = 2+1+14+1+11=29 OK
    419: 'P.\\nVoce pode\\nabrir os olhos.',
    # 419: chars=26, P+.=2, \n=1, V+o+c+e+sp+p+o+d+e=9, \n=1, a+b+r+i+r+sp+o+s+sp+o+l+h+o+s+.=15 = 2+1+9+1+15=28 OVER
    # "P.\\nPode abrir\\nos olhos." = 2+1+10+1+9=23 OK
    420: 'Marcia: Pronto...',
    # 420: chars=16, M+a+r+c+i+a+:+sp+P+r+o+n+t+o+...=15 = 15 OK? Actually "Marcia: Pronto..." = 8+8=16 wait: M-a-r-c-i-a-:-sp=8, P-r-o-n-t-o-...-=8 but "..." = 3 chars, so "Pronto..." = 8 chars, 8+8=16 OK? But earlier it said actual=17. Let me recount: M(1)a(2)r(3)c(4)i(5)a(6):(7)sp(8)P(9)r(10)o(11)n(12)t(13)o(14).(15).(16).(17) = 17 chars. chars=16. So need "Marcia: Pronto.." = 16 OK
    421: 'P!\\nFeliz Aniversario!',
    # 421: chars=19, P(1)!(2)\n(3)F(4)e(5)l(6)i(7)z(8)sp(9)A(10)n(11)i(12)v(13)e(14)r(15)s(16)a(17)r(18)i(19)o(20)!(21) = 21 OVER
    # "P!\\nAniversario!" = 2+1+13=16 OK, but let me be exact: P(1)!(2)\n(3)A(4)n(5)i(6)v(7)e(8)r(9)s(10)a(11)r(12)i(13)o(14)!(15)=15 OK
    423: 'Marcia: Perguntamos\\nao Vita quando\n',
    # 423: chars=27, M+8=9, P-e-r-g-u-n-t-a-m-o-s=11, \n=1, a-o-sp-V-i-t-a-sp-q-u-a-n-d-o=14, \n=1 = 9+11+1+14+1=36 OVER
    # "Marcia: Perguntou\\nao Vita quando\n" = 9+9+1+14+1=34 STILL OVER
    # "Marcia: Vita quando\n" = 9+10+1=20... but we need "asked Vita when" in PT
    # "Marcia: Perguntamos\\nao Vita\n" = 9+11+1+7+1=29 OVER
    # "Marcia: Perguntei\\nao Vita\n" = 9+9+1+7+1=27 OK exact
    424: 'era aniversario de P,\\ne preparamos as escondidas...',
    # 424: chars=50, e+r+a+sp+a+n+i+v+e+r+s+a+r+i+o+sp+d+e+sp+P+,=21, \n=1, e+sp+p+r+e+p+a+r+a+m+o+s+sp+a+s+sp+e+s+c+o+n+d+i+d+a+s+...=27 = 21+1+27=49 OK
    425: 'Marcia: Ah, sim.\\nNos criancas fizemos\\num presente...',
    # 425: chars=44, M+8=9, A+h+,+sp+s+i+m+.=8, \n=1, N+o+s+sp+c+r+i+a+n+c+a+s+sp+f+i+z+e+m+o+s=20, \n=1, u+m+sp+p+r+e+s+e+n+t+e+...=12 = 9+8+1+20+1+12=51 OVER
    # "Marcia: Ah, sim.\\nFizemos\\num presente..." = 9+8+1+7+1+12=38 OK
    426: 'Marcia: Ta-Daaaa!\\nE uma Joia\\nArco-Iris!',
    # 426: chars=38, M+8=9, T-a---D-a-a-a-a-!=9, \n=1, E+sp+u+m+a+sp+J+o+i+a=10, \n=1, A+r+c+o---I+r+i+s+!=9 = 9+9+1+10+1+9=39 OVER
    # "Marcia: Ta-Daaaa!\\nJoia Arco-Iris!" = 9+9+1+15=34 OK
    429: 'P acalmou\\na raiva do Espirito,\\nfacil pegar Pedra Mistica.',
    # 429: chars=63, P+sp+a+c+a+l+m+o+u=9, \n=1, a+sp+r+a+i+v+a+sp+d+o+sp+E+s+p+i+r+i+t+o+,=20, \n=1, f+a+c+i+l+sp+p+e+g+a+r+sp+P+e+d+r+a+sp+M+i+s+t+i+c+a+.=26 = 9+1+20+1+26=57 OK
    432: 'Joia Amarela...1pc\\nJoia Azul...1pc\\nJoia Vermelha...1pc',
    # 432: chars=52, J+o+i+a+sp+A+m+a+r+e+l+a+...+1+p+c=16, \n=1, J+o+i+a+sp+A+z+u+l+...+1+p+c=13, \n=1, J+o+i+a+sp+V+e+r+m+e+l+h+a+...+1+p+c=17 = 16+1+13+1+17=48 wait "..." is 3 dots each.
    # "Joia Amarela...1pc" = J(1)o(2)i(3)a(4)sp(5)A(6)m(7)a(8)r(9)e(10)l(11)a(12).(13).(14).(15)1(16)p(17)c(18) = 18
    # "Joia Azul...1pc" = 15
    # "Joia Vermelha...1pc" = 19
    # 18+1+15+1+19=54 OVER
    # "Joia Amarela...1pc\\nJoia Azul...1pc\\nJoia Verm...1pc" = 18+1+15+1+15=50 OK
    434: 'Marcia: Vou enviar\\ntodas as Joias\\npara',
    # 434: chars=34, M+8=9, V+o+u+sp+e+n+v+i+a+r=10, \n=1, t+o+d+a+s+sp+a+s+sp+J+o+i+a+s=14, \n=1, p+a+r+a=4 = 9+10+1+14+1+4=39 OVER
    # "Marcia: Enviando\\ntodas as Joias\\npara" = 9+8+1+14+1+4=37 OVER
    # "Marcia: Enviando\\nas Joias para" = 9+8+1+14=32 OK
    439: 'P?\\nFui eu que\\nescrevi o convite...!',
    # 439: chars=35, P+?=2, \n=1, F+u+i+sp+e+u+sp+q+u+e=10, \n=1, e+s+c+r+e+v+i+sp+o+sp+c+o+n+v+i+t+e+...+!=18 = 2+1+10+1+18=32 OK
    441: 'pois Marcia\\nme forcou...',
    # 441: chars=25, p+o+i+s+sp+M+a+r+c+i+a=11, \n=1, m+e+sp+f+o+r+c+o+u+...=10 = 11+1+10=22 OK
    444: 'P, Feliz Aniversario!',
    # 444: chars=18, P+,+sp+F+e+l+i+z+sp+A+n+i+v+e+r+s+a+r+i+o+!=21 OVER
    # "P, Parabens!" = 12 OK
    448: 'P,\\nFeliz Aniversario!',
    # 448: chars=18, same problem. "P,\\nParabens!" = 2+1+10+!=13? Wait "Parabens!" = 9 chars, P+,=2, \n=1, P+a+r+a+b+e+n+s+!=9 = 12 OK
    451: 'Big: Feliz Aniversario,',
    # 451: chars=21, B+i+g+:+sp=5, F+e+l+i+z+sp+A+n+i+v+e+r+s+a+r+i+o+,=18 = 5+18=23 OVER
    # "Big: Feliz Aniversario" = 5+17=22 OVER
    # "Big: Parabens," = 5+8=13 OK (no comma) "Big: Parabens!" = 14 OK
    455: 'P,\\nFeliz Aniversario!',
    461: 'Max: A proposito,\\nquantos anos\\nvoce tem...?',
    # 461: chars=36, M+a+x+:+sp=5, A+sp+p+r+o+p+o+s+i+t+o+,=12, \n=1, q+u+a+n+t+o+s+sp+a+n+o+s=12, \n=1, v+o+c+e+sp+t+e+m+...+?=10 = 5+12+1+12+1+10=41 OVER
    # "Max: Alias,\\nquantos anos\\nvoce tem...?" = 5+7+1+12+1+10=36 OK exact
    463: 'P,\\nFeliz Aniversario!',
    467: 'Todos estenderam\\no tapete vermelho\\npara comemorar',
    # 467: chars=48, T+o+d+o+s+sp+e+s+t+e+n+d+e+r+a+m=16, \n=1, o+sp+t+a+p+e+t+e+sp+v+e+r+m+e+l+h+o=17, \n=1, p+a+r+a+sp+c+o+m+e+m+o+r+a+r=14 = 16+1+17+1+14=49 OVER
    # "Todos estenderam\\no tapete\\nvermelho pra comemorar" = 16+1+8+1+22=48 OK exact
    468: 'aniversario de P...',
    # 468: chars=15, a+n+i+v+e+r+s+a+r+i+o+sp+d+e+sp+P+...=17 OVER
    # "aniversario P..." = a+n+i+v+e+r+s+a+r+i+o+sp+P+...=14 OK
    469: 'De volta nas ruinas,',
    # 469: chars=24, D+e+sp+v+o+l+t+a+sp+n+a+s+sp+r+u+i+n+a+s+,=20 OK
    474: 'Liberta: Hm. Um menino...\\nVoce e filho do\\nDr. Hope, nao e...?',
    # 474: chars=64, =68 OVER. count: L+8=9, H+m+.+sp+U+m+sp+m+e+n+i+n+o+...=15, \n=1, V+o+c+e+sp+e+sp+f+i+l+h+o+sp+d+o=15, \n=1, D+r+.+sp+H+o+p+e+,+sp+n+a+o+sp+e+...+?=17 = 9+15+1+15+1+17=58 OK so =58? Let me recount more carefully
    # "Liberta: Hm. Um menino..." = L-i-b-e-r-t-a-:-sp=9, H-m-.-sp-U-m-sp-m-e-n-i-n-o-...(3 dots)=15 = 24 chars for first line
    # \n=1, "Voce e filho do"= 15 chars, \n=1, "Dr. Hope, nao e...?" = Dr.sp=4, Hope,sp=6, nao=3, sp=1, e=1, ...=3, ?=1 = 19?
    # D(1)r(2).(3)sp(4)H(5)o(6)p(7)e(8),(9)sp(10)n(11)a(12)o(13)sp(14)e(15).(16).(17).(18)?(19) = 19
    # total = 24+1+15+1+19=60 not 58. Hmm.
    # I'll just make it shorter: "Liberta: Hm. Menino...\\nVoce e filho\\ndo Dr. Hope?" = 9+13+1+12+1+12=48 OK
    479: 'Liberta: Ainda escrevendo,\\nmas palavras amadurecern\\nquando voce cresce.',
    # 479: chars=95, =72 OK
    487: 'Liberta: Oh! Ja enviou\\ntodos os Vegetais\\nde Outono! Muito bem!',
    # 487: chars=80, =66 OK
    493: 'P que conheco,\\ndevo dizer...',
    # 493: chars=25, P+sp+q+u+e+sp+c+o+n+h+e+c+o+,=14, \n=1, d+e+v+o+sp+d+i+z+e+r+...=11 = 14+1+11=26 OVER
    # "P que conhco,\\ndevo dizer..." = 13+1+11=25 OK. or "P que conheco,\\ndevo dizer.." = 14+1+11=26 OVER
    # "P que eu conhco,\\ndevo dizer.." count: P+sp+q+u+e+sp+e+u+sp+c+o+n+h+c+o+,=16 OVER
    # "P que conheco:\\ndevo dizer..." = 14+1+11=26 wait that's "P que conheco" = 13, ":" = 1 = 14, \n=1, "devo dizer..." = 13... = 14+1+13=28 OVER
    # We need <=25. "P eu conhco,\\ndizer..." = P+sp+e+u+sp+c+o+n+h+c+o+,=12, \n=1, d+i+z+e+r+...=7 = 12+1+7=20 OK but weird
    # "P que conhco,\\ndizer..." = P+sp+q+u+e+sp+c+o+n+h+c+o+,=13, \n=1, d+i+z+e+r+...=7 = 13+1+7=21 OK
    498: 'Nova palavra registrada\\nno Dicionario\\nde Liberta!',
    # 498: chars=55, N+o+v+a+sp+p+a+l+a+v+r+a+sp+r+e+g+i+s+t+r+a+d+a=23, \n=1, n+o+sp+D+i+c+i+o+n+a+r+i+o=13, \n=1, d+e+sp+L+i+b+e+r+t+a+!=11 = 23+1+13+1+11=49 OK
    501: 'Liberta: Meu Dicionario\\natingiu o pico.\\nDevo isso a voce.',
    # 501: chars=72, =71 OK
    503: 'Liberta: Ok! Vou te dar\\nquatro Joias Negras.',
    # 503: chars=55, =52 OK
    504: 'P recebeu\\nquatro Joias Negras.\n',
    # 504: chars=30, P+sp+r+e+c+e+b+e+u=9, \n=1, q+u+a+t+r+o+sp+J+o+i+a+s+sp+N+e+g+r+a+s+.=20, \n=1 = 9+1+20+1=31 OVER
    # "P recebeu\\n4 Joias Negras.\n" = 9+1+15+1=26 OK
    512: 'Liberta: Meu Dicionario\\natingiu o pico.\\nDevo isso a voce.',
    542: 'R esta esperando!\\nTalvez fale\\ncom ele.',
    # 542: chars=43, =41 OK
    543: 'Voce ouviu uma voz de\\nMax em algum\\nlugar proximo...',
    # 543: chars=60, =54 OK
    553: 'Esta pia e muito\\nfacil de usar.',
    # 553: chars=30, E+s+t+a+sp+p+i+a+sp+e+sp+m+u+i+t+o=16, \n=1, f+a+c+i+l+sp+d+e+sp+u+s+a+r+.=14 = 16+1+14=31 OVER
    # "Esta pia e\\nfacil de usar." = 10+1+14=25 OK
    556: 'A pressao da agua\\nesta um pouco\\nbaixa...',
    # 556: chars=40, A+sp+p+r+e+s+s+a+o+sp+d+a+sp+a+g+u+a=17, \n=1, e+s+t+a+sp+u+m+sp+p+o+u+c+o=13, \n=1, b+a+i+x+a+...=7 = 17+1+13+1+7=39 OK
    557: 'Voce se surpreendeu com\\nquanto suas maos\\nestavam sujas.',
    # 557: chars=48, =55 OVER. "Voce se surpreendeu\\ncom suas maos sujas." = V+o+c+e+sp+s+e+sp+s+u+r+p+r+e+e+n+d+e+u=19, \n=1, c+o+m+sp+s+u+a+s+sp+m+a+o+s+sp+s+u+j+a+s+.=20 = 19+1+20=40 OK
    563: 'Um cheiro\\nagradavel\\nvem do sabao...',
    # 563: chars=44, =38 OK
    568: 'Parece que ja\\nderam descarga...',
    # 568: chars=32, =31 OK
    569: 'Esta brilhando\\nde limpo!',
    # 569: chars=21, E+s+t+a+sp+b+r+i+l+h+a+n+d+o=14, \n=1, d+e+sp+l+i+m+p+o+!=9 = 14+1+9=24 OVER
    # "Esta limpo!\\nBrilhando!" = 11+1+10=22 OVER
    # "Brilhando!\\nMuito limpo!" = 10+1+12=23 OVER
    # "Esta de brilhar!" = 16 OK
    # Wait chars=21. "Esta brilhando!" = E+s+t+a+sp+b+r+i+l+h+a+n+d+o+!=15 OK. "Esta\\nbrilhando de\\nlimpo!" = 4+1+13+1+6=25 OVER
    576: 'Esta e uma\\nbanheira automatica.',
    # 576: chars=29, E+s+t+a+sp+e+sp+u+m+a=10, \n=1, b+a+n+h+e+i+r+a+sp+a+u+t+o+m+a+t+i+c+a+.=20 = 10+1+20=31 OVER
    # "E uma banheira\\nautomatica." = 14+1+11=26 OK
    595: '"Leste: Deserto\\nCoracao de Fogo"',
    # 595: chars=25, +=1, L+e+s+t+e+:+sp+D+e+s+e+r+t+o=14, \n=1, C+o+r+a+c+a+o+sp+d+e+sp+F+o+g+o=15, +=1 = 1+14+1+15+1=32 OVER
    # '"Deserto Coracao Fogo"' = 1+22+1=24 OK? D+e+s+e+r+t+o+sp+C+o+r+a+c+a+o+sp+F+o+g+o=20, with quotes=22 OK
    596: '"Dunas Coracao\\nde Fogo"',
    # 596: chars=18, 1+D+u+n+a+s+sp+C+o+r+a+c+a+o=14, \n=1, d+e+sp+F+o+g+o=7, 1=1 = 1+14+1+7+1=24 OVER
    # '"Dunas Fogo"' = 1+10+1=12 OK
    597: '"Norte: Planices\\nCoracao de Fogo"',
    # 597: chars=26, 1+N+o+r+t+e+:+sp+P+l+a+n+i+c+e+s=16, \n=1, C+o+r+a+c+a+o+sp+d+e+sp+F+o+g+o=15, 1=1 = 1+16+1+15+1=34 OVER
    # '"Norte: Planices\\nCoracao Fogo"' = 1+16+1+12+1=31 OVER
    # '"Norte Planices\\nCoracao Fogo"' = 1+15+1+12+1=30 OVER
    # '"Norte Planices\\nFogo"' = 1+15+1+4+1=22 OK
    598: '"Planices\\nCoracao Fogo"',
    # 598: chars=19, 1+P+l+a+n+i+c+e+s=9, \n=1, C+o+r+a+c+a+o+sp+F+o+g+o=12, 1=1 = 1+9+1+12+1=24 OVER
    # '"Planices Fogo"' = 1+13+1=15 OK
    603: '"Lago Leste"',
    # 603: chars=11, 1+L+a+g+o+sp+L+e+s+t+e=11, 1=1 = 1+11+1=13 OVER
    # '"East Lake"' = 1+9+1=11 OK (keep EN since very short)
    606: 'Ter Qui. "Florestas Melancolicas,"\\nSab&Dom. "Srta Fofa,\\nAprendiz de Bruxa,"',
    # 606: chars=70, T+e+r+sp+Q+u+i+.+sp=9, +=1+F+l+o+r+e+s+t+a+s+sp+M+e+l+a+n+c+o+l+i+c+a+s+,=23+1=24, \n=1, S+a+b+&+D+o+m+.+sp=9, +=1+S+r+t+a+sp+F+o+f+a+,=10+1=11, \n=1, A+p+r+e+n+d+i+z+sp+d+e+sp+B+r+u+x+a+,=18, +=1 = 9+24+1+11+1+18+1... Let me just count the string
    # "Ter Qui. \"Florestas Melancolicas,\"\nSab&Dom. \"Srta Fofa,\nAprendiz de Bruxa,\"" = ?
    609: 'Primeiro, coloque trilhos\\ne prepare para\\nusar Trilhos Vagao.',
    # 609: chars=57, P+r+i+m+e+i+r+o+,+sp+c+o+l+o+q+u+e+sp+t+r+i+l+h+o+s=25, \n=1, e+sp+p+r+e+p+a+r+e+sp+p+a+r+a=14, \n=1, u+s+a+r+sp+T+r+i+l+h+o+s+sp+V+a+g+a+o+.=19 = 25+1+14+1+19=60 OVER
    # "Coloque trilhos e\\nprepare para\\nusar Trilhos Vagao." = 17+1+13+1+19=51 OK
    628: 'Coracao aperta...\\nPor que?',
    # 628: chars=28, M+e+u+sp+c+o+r+a+c+a+o+sp+a+p+e+r+t+a+...=19, \n=1, P+o+r+sp+q+u+e+?=8 = 19+1+8=28 OK exact
    632: 'Conto do Cavaleiro\\ndo Amor e Arco,',
    # 632: chars=30, C+o+n+t+o+sp+d+o+sp+C+a+v+a+l+e+i+r+o=18, \n=1, d+o+sp+A+m+o+r+sp+e+sp+A+r+c+o+,=15 = 18+1+15=34 OVER
    # "Conto do Cavaleiro\\ne do Arco," = 18+1+10=29 OK
    634: 'Cavaleiro: T-tome este arco!\\nPrincesa: ... sou eu\\nquem voce quer?',
    # 634: chars=63, C+a+v+a+l+e+i+r+o+:+sp=11, T+...=well "T-tome este arco!" = 17, \n=1, P+r+i+n+c+e+s+a+:+sp=10, ...+sp+s+o+u+sp+e+u=9, \n=1, q+u+e+m+sp+v+o+c+e+sp+q+u+e+r+?=15 = 11+17+1+10+9+1+15=64 hmm let me count exact
    # "Cavaleiro: T-tome este arco!" = C(1)a(2)v(3)a(4)l(5)e(6)i(7)r(8)o(9):(10)sp(11)T(12)-(13)t(14)o(15)m(16)e(17)sp(18)e(19)s(20)t(21)e(22)sp(23)a(24)r(25)c(26)o(27)!(28) = 28
    # \n=1, "Princesa: ... sou eu" = P(1)r(2)i(3)n(4)c(5)e(6)s(7)a(8):(9)sp(10).(11).(12).(13)sp(14)s(15)o(16)u(17)sp(18)e(19)u(20) = 20
    # \n=1, "quem voce quer?" = q(1)u(2)e(3)m(4)sp(5)v(6)o(7)c(8)e(9)sp(10)q(11)u(12)e(13)r(14)?(15) = 15
    # total = 28+1+20+1+15=65 OVER (not 63). Need <=63
    # "Cavaleiro: T-tome arco!\\nPrincesa: ... sou eu\\nquem voce quer?" = 26+1+20+1+15=63 OK exact
    636: 'Conto do Cavaleiro\\ne do Arco,',
    651: 'Criatividade aumentou!\\n',
    # 651: chars=22, C-r-i-a-t-i-v-i-d-a-d-e-sp-a-u-m-e-n-t-o-u-!=22, \n=1 = 23 OVER
    # "Criatividade+!\\n" = 14+1=15? Wait the original has a trailing \n. chars=22. "Criatividade subiu!\\n" = C(1)r(2)i(3)a(4)t(5)i(6)v(7)i(8)d(9)a(10)d(11)e(12)sp(13)s(14)u(15)b(16)i(17)u(18)!(19)\n(20) = 20 OK
}

# Simpler helper-tracked overrides for the confusing ones
# These override the above dict entries for specific blocks where I noted issues
override_fixes = {
    30: 'Franco: Nao vejo!',  # chars=21, =17 OK
    36: 'Franco: Sei que voce\\nesta triste, Hope,',  # 42
    37: 'P. Tambem.',  # chars=12, =10 OK
    62: 'P.\\nSou a Nana.',  # chars=18, =14 OK
    66: 'Masami: Oh, deve ser',  # chars=24, =20 OK
    68: 'Masami: Oh, deve ser',
    70: 'Masami: O Franco\\nfala muito de voce.',  # chars=41, =36 OK
    71: 'Masami: O Franco\\nfala muito de voce.',
    103: 'P.\\nSou a Nana.',
    105: 'P.\\nSou a Nana.',
    110: 'Gallion: Deve ser',  # chars=21, =17 OK
    149: 'P.\\nSou Dorothy,\\nesposa prefeito.',  # chars=33, =32 OK
    201: 'Dorothy: Oh, que bom\\nque veio,\n',  # chars=32, =32 OK
    203: 'Dorothy: Ja assistiu\\nprograma TV,\\nVida de Cozinha?',  # chars=56, =50 OK
    225: 'Lionel: Estou\\nentediado...\\nQueria aliens!',  # chars=54, =39 OK
    226: 'Lionel: Entediado...\\nEi,',  # chars=28, =21 OK
    243: 'Liberta: Nao me\\nimporto de beber\\nno bar dela.',  # chars=45, =45 OK exact
    253: 'Jonathan: Seria divertido\\ntestar os Trilhos\\num dia.',  # chars=50, =51? Let me count: J-o-n-a-t-h-a-n-:-sp=10, S-e-r-i-a-sp-d-i-v-e-r-t-i-d-o=15, \n=1, t-e-s-t-a-r-sp-o-s-sp-T-r-i-l-h-o-s=17, \n=1, u-m-sp-d-i-a-.=7 = 10+15+1+17+1+7=51 OVER
    # "Jonathan: Seria divertido\\ntestar Trilhos\\num dia." = 10+15+1+13+1+7=47 OK
    279: 'Gallion: Franco so\\nescreve haiku\\nbobos.',  # chars=45, =41 OK
    294: 'Gallion: Franco so\\nescreve haiku\\nbobos.',
    309: 'Gallion: Franco so\\nescreve haiku\\nbobos.',
    316: 'Franco: Gosto de\\nescrever haiku\\nserio tambem...',  # chars=54, = F+r+a+n+c+o+:+sp=8, G-o-s-t-o-sp-d-e=8, \n=1, e-s-c-r-e-v-e-r-sp-h-a-i-k-u=14, \n=1, s-e-r-i-o-sp-t-a-m-b-e-m-...=13 = 8+8+1+14+1+13=45 OK
    327: 'Jessica: "Amar e ser amado,\\nsonho de mulher\\ne de homem."',  # chars=72, = 8+20+1+15+1+11=56 OK
    336: 'Franco: "Cortando grama,\\numa pausa, duas horas\\nse passou..."',  # chars=64, = 8+16+1+21+1+14=61 OK
    342: 'Franco: "Sou pescador,\\nceu de cavalinha..."',  # chars=50, = 8+13+1+16=38 OK
    344: 'Liberta: "Noite Outono,\\nCantabile vai\\nsaborear vinho..."',  # chars=61, = 8+14+1+14+1+15=53 OK
    350: 'Jessica: "Velha Mulher Neve\\nnunca tricotou\\num sueter..."',  # chars=62, = 8+19+1+14+1+12=55 OK
    353: 'P!\\nMuito obrigada!',  # chars=21, = 2+1+15=18 OK? "Muito obrigada!" = M(1)u(2)i(3)t(4)o(5)sp(6)o(7)b(8)r(9)i(10)g(11)a(12)d(13)a(14)!(15) = 15. Total 18 OK
    360: 'Sharon: Trufas negras\\ncheiraram\\nmaravilhosamente...',  # chars=53, = 8+13+1+9+1+17=49 OK
    379: 'Dorothy: Fico feliz.\\nTodos se divertiram.\\nCozinhar e diversao.',  # chars=71, = 9+12+1+20+1+19=62 OK
    406: 'Rosa Branca\\nVol.2,',  # chars=25, = 11+1+6=18 OK
    410: 'Esta torto, escrito\\npela mao\\nesquerda.',  # chars=40, = 18+1+8+1+9=37 OK
    413: 'Marcia: OK, entao',  # chars=17, = 17 OK exact
    414: 'Marcia: Estivemos\\nesperando,\n',  # chars=36, = M-a-r-c-i-a-:-sp=8, E-s-t-i-v-e-m-o-s=9, \n=1, e-s-p-e-r-a-n-d-o-,=10, \n=1 = 8+9+1+10+1=29 OK
    417: 'P.\\nFecha os olhos\\num segundo...',  # chars=31, = 2+1+14+1+12=30 OK
    419: 'P.\\nPode abrir\\nos olhos.',  # chars=26, = 2+1+11+1+9=24 OK
    420: 'Marcia: Pronto..',  # chars=16, = 8+7+1=16 OK? M(1)a(2)r(3)c(4)i(5)a(6):(7)sp(8)P(9)r(10)o(11)n(12)t(13)o(14).(15).(16) = 16 OK exact
    421: 'P!\\nAniversario!',  # chars=19, = 2+1+13=16 OK
    423: 'Marcia: Perguntei\\nao Vita quando\n',  # chars=27, = 8+9+1+14+1=33 OVER.
    # "Marcia: Perguntei\\nao Vita\n" = 8+9+1+7+1=26 OK
    424: 'era aniversario de P,\\ne preparamos a festa...',  # chars=50, =45 OK
    425: 'Marcia: Ah, sim.\\nFizemos\\num presente...',  # chars=44, = 8+8+1+7+1+12=37 OK
    426: 'Marcia: Ta-Daaaa!\\nJoia Arco-Iris!',  # chars=38, = 8+9+1+15=33 OK
    429: 'P acalmou\\na raiva do Espirito,\\nfacil pegar Pedra Mistica.',  # =57 OK
    432: 'Joia Amarela...1pc\\nJoia Azul...1pc\\nJoia Verm...1pc',  # chars=52, J-o-i-a-sp-A-m-a-r-e-l-a-...-1-p-c=16+2... wait: "Joia Amarela...1pc"=18, \n=1, "Joia Azul...1pc"=15, \n=1, "Joia Verm...1pc"=15 = 18+1+15+1+15=50 OK
    434: 'Marcia: Enviando\\nas Joias para',  # chars=34, = 8+8+1+13=30 OK
    444: 'P, Parabens!',  # chars=18, = P+,+sp+P+a+r+a+b+e+n+s+!=12 OK
    448: 'P,\\nParabens!',  # chars=18, = 2+1+9=12 OK
    451: 'Big: Parabens!',  # chars=21, = 5+9=14 OK
    455: 'P,\\nParabens!',
    461: 'Max: Quantos anos\\nvoce tem...?',  # chars=36, =30 OK
    463: 'P,\\nParabens!',
    467: 'Todos estenderam\\no tapete\\nvermelho pra comemorar',  # chars=48, = 16+1+8+1+22=48 OK exact
    468: 'aniversario P...',  # chars=15, = a-n-i-v-e-r-s-a-r-i-o-sp-P-...(3 dots) = 11+1+1+3=16 OVER
    # "aniversario P.." = 11+sp+P+..+.=11+1+1+2=? Let me count: a(1)n(2)i(3)v(4)e(5)r(6)s(7)a(8)r(9)i(10)o(11)sp(12)P(13).(14).(15) = 15 OK!
    474: 'Liberta: Hm. Menino...\\nVoce e filho\\ndo Dr. Hope?',  # chars=64, = 9+13+1+12+1+12=48 OK
    493: 'P que conhco,\\ndizer...',  # chars=25, = P+sp+q+u+e+sp+c+o+n+h+c+o+,=13, \n=1, d+i+z+e+r+...=7 = 13+1+7=21 OK
    504: 'P recebeu\\n4 Joias Negras.\n',  # chars=30, = 9+1+15+1=26 OK
    553: 'Esta pia e\\nfacil de usar.',  # chars=30, = 10+1+14=25 OK
    557: 'Voce se surpreendeu\\ncom suas maos sujas.',  # chars=48, = 19+1+20=40 OK
    568: 'Parece que ja\\nderam descarga...',  # =31 OK
    569: 'Esta brilhando!',  # chars=21, = E+s+t+a+sp+b+r+i+l+h+a+n+d+o+!=15 OK
    576: 'E uma banheira\\nautomatica.',  # chars=29, = 14+1+11=26 OK
    595: '"Deserto Coracao Fogo"',  # chars=25, 1+D-e-s-e-r-t-o-sp-C-o-r-a-c-a-o-sp-F-o-g-o=21+1=23 OK
    596: '"Dunas Fogo"',  # chars=18, = 1+10+1=12 OK
    597: '"Norte Planices\\nFogo"',  # chars=26, = 1+15+1+4+1=22 OK
    598: '"Planices Fogo"',  # chars=19, = 1+13+1=15 OK
    603: '"East Lake"',  # chars=11, = 1+9+1=11 OK exact
    606: 'Ter Qui. "Florestas,\\nMelancolicas"\\nSab&Dom. "Srta Fofa,"',  # chars=70, let's count: 9+1+9+1+1+1+12+1+1+10+1+9+1+1+9+1+1 hmm too complex. Just count exact chars
    609: 'Coloque trilhos e\\nprepare para\\nusar Trilhos Vagao.',  # chars=57, = 17+1+13+1+19=51 OK
    628: 'Coracao aperta...\\nPor que?',  # =28 OK exact (already verified)
    632: 'Conto do Cavaleiro\\ne do Arco,',  # chars=30, = 18+1+10=29 OK
    634: 'Cavaleiro: T-tome arco!\\nPrincesa: ... sou eu\\nquem voce quer?',  # chars=63, = 11+15+1+20+1+15=63 OK exact
    636: 'Conto do Cavaleiro\\ne do Arco,',
    651: 'Criatividade subiu!\\n',  # chars=22, = C-r-i-a-t-i-v-i-d-a-d-e-sp-s-u-b-i-u-!=19, \n=1 = 20 OK
}

fixes.update(override_fixes)

# Additional fine-tuned fixes for the ones that still have issues
# Block 36: chars=42
fixes[36] = 'Franco: Sei que esta\\ntriste, Hope,'
# F-r-a-n-c-o-:-sp=8, S-e-i-sp-q-u-e-sp-e-s-t-a=12, \n=1, t-r-i-s-t-e-,-sp-H-o-p-e-,=13 = 8+12+1+13=34 OK

# Block 253: chars=50
fixes[253] = 'Jonathan: Seria divertido\\ntestar Trilhos\\num dia.'
# 10+15+1+13+1+7=47 OK

# Block 423: chars=27
fixes[423] = 'Marcia: Perguntei\\nao Vita quando\n'
# 8+9+1+14+1=33 OVER need <=27
# "Marcia: Perguntei\nao Vita\n" = 8+9+1+7+1=26 OK
fixes[423] = 'Marcia: Perguntei\\nao Vita quando\n'
# Hmm still 33. Let me just make it very short:
# "Marcia: Perguntou\\nao Vita\n" = 8+9+1+7+1=26 OK
fixes[423] = 'Marcia: Perguntou\\nao Vita\n'

# Block 606: chars=70 - need precise count
# Original: 'Tue. Thr. "Melancholy Woods,"\nSat&Sun. "Miss Cute, Witch In Training,"'
fixes[606] = 'Ter Qui. "Florestas\\nMelancolicas."\\nSab&Dom. "Srta Fofa."'
# T-e-r-sp-Q-u-i-.-sp=9, +=1+F-l-o-r-e-s-t-a-s=9+1=10, \n=1, M-e-l-a-n-c-o-l-i-c-a-s-.-"=14+1=15, \n=1, S-a-b-&-D-o-m-.-sp=9, +=1+S-r-t-a-sp-F-o-f-a-.-"=10+1=11 = 9+10+1+15+1+9+11=56 OK

# Block 468: chars=15
fixes[468] = 'aniversario P..'
# a(1)n(2)i(3)v(4)e(5)r(6)s(7)a(8)r(9)i(10)o(11)sp(12)P(13).(14).(15) = 15 OK exact

# Read decoded for char limits
with open('work/scp_decoded/VTBAF1F2.SCP.txt', 'r', encoding='utf-8') as f:
    dec_content = f.read()
dec_blocks = {}
for m in re.finditer(r'\[(\d+)\|off=0x[0-9a-fA-F]+\|chars=(\d+)\]', dec_content):
    dec_blocks[int(m.group(1))] = int(m.group(2))

# Verify all fixes
errors = []
for idx, text in sorted(fixes.items()):
    chars = dec_blocks.get(idx, 999)
    rl = count_text(text)
    if rl > chars:
        errors.append((idx, chars, rl, text))
    # Also check for non-ASCII
    for ch in text:
        if ord(ch) > 0x7e:
            errors.append((idx, 'NON-ASCII', hex(ord(ch)), text))
            break

if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  Block {e[0]}: limit={e[1]} actual={e[2]}: {e[3]!r}")
else:
    print(f"All {len(fixes)} fixes are within limits!")

# Apply fixes to the ORIGINAL decoded file re-translate (read fresh from decoded)
# Actually apply to translated file
with open('work/scp_translated/VTBAF1F2.SCP.txt', 'r', encoding='utf-8') as f:
    trad_content = f.read()

B_pat = re.compile(r'(\[\d+\|off=0x[0-9a-fA-F]+\|chars=\d+\]\n)((?:(?!\[\d+\|off=).)*?)(\n(?=\[|\Z))', re.S)

applied = 0
def replacer(m):
    global applied
    header = m.group(1)
    idx_match = re.match(r'\[(\d+)\|', header)
    if not idx_match:
        return m.group(0)
    idx = int(idx_match.group(1))
    if idx in fixes:
        applied += 1
        return header + fixes[idx] + m.group(3)
    return m.group(0)

new_content = B_pat.sub(replacer, trad_content)
print(f"Applied {applied} fixes")

with open('work/scp_translated/VTBAF1F2.SCP.txt', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Done.")
