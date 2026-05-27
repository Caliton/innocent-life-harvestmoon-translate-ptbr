# -*- coding: utf-8 -*-
import re, sys

PATH_DEC = 'work/scp_decoded/ETRENT.SCP.txt'
PATH_TR  = 'work/scp_translated/ETRENT.SCP.txt'

def t2t(l):
    o = []; i = 0
    while i < len(l):
        if l[i:i+2] == '\\n': o.append('\n'); i += 2
        elif l[i:i+2] == '\\\\': o.append('\\'); i += 2
        else: o.append(l[i]); i += 1
    return ''.join(o)

# Translation map: index -> PT-BR (literal text with \n as two chars backslash-n)
T = {}

# ============ Onomatopoeias / dots / labels kept as-is (NOT included; left EN) ============
# These stay English: dots, Zzzz, BAM, POP, CRASH, Beep, Splash, etc. Not added to T.

# ============ Early blocks ============
T[1] = 'Esta e uma HDTV fabricada pela\\nBanks Corporation.'                 # c=54
T[2] = 'Mas voce nao tem tempo de\\nassistir TV agora...'                    # c=48

# ============ Final Z Rangers ============
T[781] = "Red: Bem, ao menos nao podemos sair\\npior que o pessoal dos outros\\ncapitulos!"
T[782] = 'Green: Isso me deixa bem mais\\naliviado!'
# 783 = "To be continued" banner -> translate the text portion
T[784] = '"Final Z Rangers"\\n                    Parte 13'
T[785] = "Pink: Vamos revisar... Os aliens sao\\nvitimas inocentes controladas de\\nalgum jeito, nao podemos ataca-los..."
T[786] = "Red: E tem os Raios Gaga saindo\\ndos olhos deles, entao nao podemos\\nnem olhar..."
T[787] = 'Green: Entao a unica chance e tentar\\ndestruir as pulseiras que os\\ncontrolam a distancia.'
T[788] = "Green: Vamos usar o Super MagnetoRifle!"
T[789] = 'Blue: Nao! O Super MagnetoRifle e uma\\narma muito ineficiente!\\nO custo por tiro e astronomico!'
T[790] = 'Blue: Sabe quantos almocos podiamos\\ncomprar com o custo de um unico\\ntiro dessa arma?'
T[791] = 'Red: Voce mede tudo em almocos?'
T[792] = "Blue: So tento ajudar este capitulo\\na sobreviver! O chefe me disse\\nexatamente quais eram meus deveres!"
T[793] = 'Green: Sim, mas precisamos de algo que\\nfuncione mesmo, e o Super MagnetoRifle\\ntem mira automatica!'
T[794] = 'Blue: Nao. Treinei por meses para ter\\nmelhores resultados com armas baratas\\ndo que com as caras.'
T[795] = 'Blue: Esta e finalmente minha chance\\nde me provar!'
T[796] = 'Blue: Testemunhem minha Lanca de\\nBambu Azul especial!'
T[797] = "Blue: Ei, nao esta aqui!\\nAi nao, deixei la na base!"
T[798] = 'Red: Idiota.'
T[800] = '"Final Z Rangers"\\n                    Parte 14'
T[801] = 'Blue: .........................'
T[802] = "Green: Ei, Blue. Sei que esta deprimido\\npor ter esquecido sua lanca e tudo,\\nmas nao se deixe abater."
T[803] = 'Red: E, nao fique tao azul, Blue.\\nHeehee...'
T[804] = 'Pink: Nao e hora pra piadas!\\nOs aliens estao fugindo!'
T[805] = 'Green: Certo. Hora de todos se\\ntransformarem! Depois vamos atras\\ndaqueles aliens!'
T[806] = 'Red & Pink: Entendido!'
T[807] = 'Red & Green & Pink: Poderes Final Z\\nativar! Forma de..... Super Final Z!!'
T[808] = 'Os Final Z Rangers viraram suas formas\\nsuper, ampliando os 5 sentidos e\\naumentando forca e velocidade!'
T[809] = "Super Pink: Blue? Voce nao vai se\\ntransformar?"
T[810] = "Blue: Desculpe, so tenho o equipamento\\nminimo. Nao posso me transformar."
T[811] = 'Blue: Alem disso, sabe quanta energia\\nleva pra se transformar?! Davamos pra\\ncomer semanas com esse dinheiro!'
T[812] = "Blue: Mas nem se importem comigo...\\nSou inutil..."
T[816] = "Super Pink: O que vamos fazer? Temos\\nde ir atras dos aliens, mas nao\\npodemos deixar o Blue pra tras, ne?"
T[817] = 'Super Red: Por que nao? Vamos logo!\\nDai usamos todas as armas caras\\nque quisermos! Hahaha!'
T[818] = "Super Pink: Voce mudou, Red..."
T[819] = "Super Green: Ele anda sob muito\\nestresse ultimamente..."
T[820] = "Super Red: Vamos la! Saquem os Super\\nMagnetoRifles e as MegaloBazookas!"
T[821] = 'Blue: E-espera um pouco! Esqueci que\\nainda tenho mais um poder...'
T[822] = "Super Red: Se voce quase esqueceu,\\nnao deve ser muito bom..."
T[823] = "Blue: Nao, tenho um plano. Vou fechar\\nos olhos e usar meus poderes de ESP\\npra lutar contra os aliens."
T[824] = "Blue: Treinei anos por este momento!\\nAgora afastem-se enquanto mostro\\nmeu verdadeiro poder! Ha!"
T[825] = "Super Green: E-ei, isso nao!"
T[827] = 'Super Green: Ofa!'
T[828] = 'Super Pink: Nossa, ele correu pra rua\\ne foi atropelado por um carro...'
T[829] = 'Super Green: E estava correndo na\\ndirecao oposta aos aliens,\\ntambem...'
T[830] = "Super Red: Bem, ele foi uma grande\\najuda. De quem foi a ideia de\\ncontrata-lo, afinal?"
T[832] = '"Final Z Rangers"\\n                    Parte 16'
T[833] = 'Chefe (Por radio): Entendo...\\nEntao o Blue nao ajudou...'
T[834] = "Chefe (Por radio): Temo que nao temos\\nescolha senao continuar a perseguir\\nos aliens."
T[835] = 'Super Green: Entendido.'
T[836] = "Super Pink: Bem, esse e o 987o Blue\\nque ja passou por aqui..."
T[837] = 'Super Red: E... E eu achei mesmo\\nque esse ia durar...'
T[838] = "Super Green: Acho que e o uniforme.\\nDeve estar amaldicoado.\\nVou manda-lo pra lavar depois."
T[839] = "Super Green: Vamos, temos de pegar\\naqueles aliens! Nao podemos deixa-los\\nfugir pra cidade!"
T[840] = 'Super Red: Mesmo assim, parte de mim\\nacha que se o povo fosse afetado pelos\\nraios alien, seria mais feliz.'
T[841] = 'Super Pink: Sim, eu tambem!'
T[842] = 'Super Green: Mas temos de lembrar que\\nos proprios aliens estao sendo\\ncontrolados por aquelas pulseiras.'
T[843] = "Super Pink: Hmm... Acho que tem razao.\\nE se nao fizermos algo, nosso capitulo\\nvai a falencia..."
T[844] = "Super Red: Entao vamos indo!"
T[845] = 'Super Green & Super Pink: Certo!'
T[847] = '"Final Z Rangers"\\n                    Parte 17'
T[848] = 'Super Red: Certo, me passe aquele\\nMagnetoRifle e'
T[849] = " Ei!\\nEspera um pouco! Eles estao\\nescondendo as pulseiras! Nao consigo ver!"
T[850] = "Super Green: Nao temos escolha senao\\ntentar combate corpo a corpo. E\\nperigoso, mas nao vejo alternativa..."
T[851] = 'Super Red: Escutem todos!\\nSo nao se esquecam de ficar longe\\ndos Raios Gaga!'
T[852] = "Super Red: Se olharem pra eles,\\nvao-- Ugh! Gagagagaaaa."
T[853] = 'Super Green: Nossa, foi rapido!\\nJa pegaram o Red!'
T[854] = "Super Pink: Somos so eu e voce, Green."
T[855] = "Super Green: Tudo bem. Sinto que\\nposso finalmente te dizer, Pink... Eu....\\nTe amo! Estou totalmente gaga por voce!"
T[856] = "Super Green: Entao nenhum raio alien\\nvai mudar o que eu sinto!"
T[857] = 'Super Pink: Green!'
T[858] = "Super Green: Vamos!"
T[859] = "Super Green: Se olhar pra eles,\\nvao--ugh! Gagagagaaaa."
T[860] = 'Super Pink: G-green'
T[861] = "Super Pink: Isso nao tem graca...\\nSoluco..."
T[863] = '"Final Z Rangers"\\n                    Parte 18'
T[864] = 'Super Red & Super Green: Heeheehee!\\nAdoro estes aliens!\\nGagagagaga!'
T[865] = "Super Pink: Suspiro... Sou a unica que\\nainda esta com a cabeca no lugar..."
T[866] = "Super Pink: Certo. Vou mostrar do que\\nesta garota e capaz!"
T[868] = 'Super Pink: La vem eles!\\nTenho de evitar olhar nos olhos\\ndeles!'
T[870] = "Super Pink: Iiii!\\nNao lembro dos aliens serem\\ntao fortes antes!"
T[871] = "Super Pink: Ai nao...\\nEstou cercada!\\nAcho que estou encrencada agora!"
T[872] = 'Super Red & Super Green: Gagagagagaga...'
T[873] = "Super Pink: Red e Green parecem\\nfelizissimos. Ate fico com um\\npouco de inveja deles..."
T[876] = "Super Pink: Ugh! Estou em menor numero...\\nNao aguento muito mais...\\nTudo esta... Ficando escuro..."
T[877] = '*: Nao! As pulseiras estao falhando!\\nEstao enlouquecendo! Transmitam o\\ncodigo de autodestruicao!!'
T[879] = '"Final Z Rangers"\\n                    Parte 19'
T[880] = 'Super Pink: Os aliens voltaram as suas\\nformas verdadeiras...'
T[881] = 'Super Red: O que?\\nO que estou fazendo aqui?'
T[882] = "Super Green: Pink!\\nAinda estou gaga por voce!"
T[883] = "Super Pink: Qual e! Nao temos tempo\\npra isso agora! Temos de descobrir\\nquem nos salvou..."
T[884] = 'Super Red: Sera aquele velho estranho\\nali?'
T[885] = 'Super Pink: V-vovo?\\nO que faz aqui?'
T[886] = "Vovo: Me desculpe, Pink.\\nNao estava tentando dominar o\\nmundo..."
T[887] = "Vovo: E so que o seu capitulo dos\\nFinal Z Rangers ia tao mal\\nque eu...."
T[888] = 'Vovo: Bem, pensei em te dar uma\\nchance de provar sua\\nutilidade...'
T[889] = 'Super Pink: Quer dizer que...\\nVoce comecou tudo isso?'
T[890] = 'Super Green: Entendo seus sentimentos\\npela sua neta, mas...'
T[891] = "Super Pink: Seu idiota!\\nQualquer um saberia que nao se sai\\nporai comecando invasoes alien!"
T[892] = "Vovo: Me desculpe... Por favor me\\nperdoe..."
T[895] = '"Final Z Rangers"\\n                    Parte Final'
T[896] = "Red: Pink! Quanto tempo!\\nComo tem passado?"
T[897] = 'Pink: Red!\\nE o Green, tambem!'
T[898] = 'Green: Desculpe pelo seu vovo levar\\na culpa do Blue desistir e tudo...'
T[899] = "Pink: Ele nao conseguia se conter.\\nSempre fui a favorita dele, desde\\nquando eu era pequena..."
T[900] = "Pink: Mas dessa vez ele foi longe demais.\\nO Capitulo Leste dos rangers acabou\\ne a culpa e toda dele..."
T[901] = "Red: Nao se preocupe tanto com isso.\\nHa mais na vida que os Final Z\\nRangers. Entao, o que tem feito?"
T[902] = "Pink: Tenho trabalhado meio periodo\\nenquanto estudo pra ser cuidadora\\nde criancas."
T[903] = 'Red: Isso e a sua cara, Pink. Voce\\nsempre gostou de criancas.\\nE voce, Green?'
T[904] = "Green: Sou policial.\\nAcho que preciso fazer algo pra\\nproteger as pessoas, sabe?"
T[905] = "Red: Nossa, isso e otimo.\\nAcho que sou o unico que nao sabe\\no que vai fazer."
T[906] = "Red: Mas tudo bem. Enquanto eu nao\\ndesistir, tenho a vida toda pela\\nfrente pra me decidir."
T[907] = "Red: Acho que vou continuar tentando\\ncoisas diferentes ate descobrir o\\nque quero fazer da vida."
T[908] = "Pink: Fico feliz de ter encontrado\\nvoces dois."
T[909] = "Green: Sim. Pode nao ter dado certo\\ndo jeito que queriamos, mas nunca\\nvou esquecer o tempo que passamos juntos."
T[910] = 'Red: Bem, acho que devo ir indo.\\nVer voces dois me inspirou a sair\\ne procurar um emprego.'
T[911] = "Red: Ate mais!\\nDa proxima vez, talvez eu tenha\\numa nova carreira pra contar!"
T[912] = 'Pink: Espero que sim.\\nBoa sorte!'
T[913] = 'Red & Green & Pink: Tchau!'
T[914] = '"Final Z Rangers"\\n                    Fim'
T[915] = 'Sintonize semana que vem para uma\\nreprise de "Final Z Rangers."'

# ============ Final Z Rangers extras (early) ============
T[604] = '"Final Z Rangers"\\n                    Parte 2'

# ============ Miss Cute, Witch In Training (Parts 1-20) ============
# Repeated boilerplate
INTRO_CUTE = "Sou a Miss Cute. Posso nao\\nparecer, mas sou uma\\nbruxa de carteirinha."                  # <=83
WELL_CUTE  = 'Bem, quase. Sabe,\\nmeu pai o Rei Bruxo me mandou\\ntreinar no mundo humano.'                # <=101
LOOK_CUTE  = "Vejamos...\\nTem alguem perto precisando de\\najuda?"                                          # <=50
AHA_CUTE    = 'Aha! Parece trabalho pra a\\nMiss Cute, Bruxa em Treino!'                                     # <=61
SOLVE_CUTE  = 'Miss Cute: Vou resolver seu\\nproblema com o poder da fofura!\\nHippity hoppity hoo! Te ajudo!'   # <=107
SOLVED_CUTE = 'Miss Cute: Mais um resolvido!\\nAte semana que vem!'                                          # <=61
# Super Training "solve own/your problem" (defined early so Training Part 20 can reuse)
SOLVE_OWN = 'Miss Cute: Vou resolver meu proprio\\nproblema com o poder da fofura!\\nHippity hoppity hee! Vou me ajudar!'
SOLVE_YOU = 'Miss Cute: Vou resolver seu\\nproblema com o poder da fofura!\\nHippity hoppity hoo! Vou te ajudar!'

# need-count lines, vary by number
def needN(n, person='people'):
    if person == 'first':
        return 'Deixar 20 pessoas felizes\\nantes de virar uma\\nbruxa de verdade!'                          # <=71
    return 'Deixar mais %d pessoas felizes\\nantes de virar uma\\nbruxa de verdade!' % n                     # <=75/76

# Part 1 (header built programmatically via TRAIN_HDR)
T[917] = INTRO_CUTE
T[918] = WELL_CUTE
T[919] = needN(20, 'first')
T[920] = LOOK_CUTE
T[921] = "*: Ai nao... O que vou fazer?\\nNao acredito que tirei 12 na prova.\\nSe minha mae ver isso, estou morto..."
T[922] = AHA_CUTE
T[923] = SOLVE_CUTE
T[924] = "*: Uau! Minha nota virou 100!\\nIsso e incrivel! Obrigado, Miss Cute!"
T[925] = SOLVED_CUTE
T[926] = '*: Ei, espera ai! Agora que reparo,\\nso a nota mudou! Todos os meus\\nerros ainda estao ai!'
T[927] = "*: Isso vai deixar minha mae ainda\\nmais brava comigo... Ugh..."
# Part 2
T[929] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 2'
T[930] = INTRO_CUTE; T[931] = WELL_CUTE; T[932] = needN(19)
T[933] = LOOK_CUTE
T[934] = '*: Ah, o que vou fazer?\\nPor que tive de me apaixonar por\\ndois homens diferentes?'
T[935] = '*: Cada um tem suas qualidades.'
T[936] = '*: Simplesmente nao consigo escolher.\\nSuspiro...'
T[937] = AHA_CUTE; T[938] = SOLVE_CUTE
T[939] = '*: Iii! O que aconteceu?\\nAgora tem duas de mim!'
T[940] = "*: Hmm... Agora nao preciso escolher\\nentre eles. Posso ter os dois!\\nObrigada, Miss Cute!"
T[941] = SOLVED_CUTE
T[942] = "*: O unico problema e que ainda nao\\nfalei com nenhum dos dois..."
# Part 3
T[944] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 3'
T[945] = INTRO_CUTE; T[946] = WELL_CUTE; T[947] = needN(18)
T[948] = LOOK_CUTE
T[949] = "*: Estou tao ocupada... Como diz o\\nditado, agradeceria ate a ajuda de\\num gato. Ai, estou tao ocupada!"
T[950] = AHA_CUTE; T[951] = SOLVE_CUTE
T[952] = "*: Uau! Minhas maos viraram patas\\nde gato! Agora vou terminar tudo sem\\nproblema! Obrigada, Miss Cute!"
T[953] = SOLVED_CUTE
T[954] = "*: Espera, como vou trabalhar com\\npatas de gato? Isso e so uma\\nexpressao! Me transforme de volta!"
# Part 4
T[956] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 4'
T[957] = INTRO_CUTE; T[958] = WELL_CUTE; T[959] = needN(17)
T[960] = LOOK_CUTE
T[961] = "*: Ugh... Engordei bastante ultimamente.\\nNao consigo nem fechar o ziper da\\nminha saia..."
T[962] = AHA_CUTE; T[963] = SOLVE_CUTE
T[964] = '*: Uau! Minha saia ficou maior de\\nrepente! Agora serve perfeitamente!\\nObrigada, Miss Cute!'
T[965] = SOLVED_CUTE
T[966] = "*: Claro, acho que preferia ter minha\\ncintura diminuida do que minha saia\\naumentada..."
# Part 5
T[968] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 5'
T[969] = INTRO_CUTE; T[970] = WELL_CUTE; T[971] = needN(16)
T[972] = LOOK_CUTE
T[973] = "*: Nao aguento mais. Todos vivem me\\nperturbando. Queria ser forte em vez\\nde fraco e magrelo..."
T[974] = AHA_CUTE; T[975] = SOLVE_CUTE
T[976] = "*: Uau! Meu corpo ficou enorme e\\ncheio de musculos! Nao vou mais ser\\nperturbado! Obrigado, Miss Cute!"
T[977] = SOLVED_CUTE
T[978] = '*: Mas agora minha pele esta roxa e\\nmanchada... Pareco um monstro! As\\ngarotas nunca vao gostar de mim...'
# Part 6
T[980] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 6'
T[981] = INTRO_CUTE; T[982] = WELL_CUTE; T[983] = needN(15)
T[984] = LOOK_CUTE
T[985] = "*: Suspiro... Acho que nao nasci pra\\nser chef. Adoro cozinhar, mas\\nsimplesmente nao sou bom nisso..."
T[986] = AHA_CUTE; T[987] = SOLVE_CUTE
T[988] = '*: O que? Meus bracos estao se\\nmovendo a velocidades incriveis!'
T[990] = "*: Incrivel! Corto vegetais mais\\nrapido que qualquer maquina!\\nObrigado, Miss Cute!"
T[991] = SOLVED_CUTE
T[992] = "*: Mas meu problema era que nao\\nconsigo acertar os temperos..."
T[993] = "*: Se ela vai realizar o desejo de\\nalguem, o minimo seria ouvir o que\\na pessoa quer primeiro..."
# Part 7
T[995] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 7'
T[996] = INTRO_CUTE; T[997] = WELL_CUTE; T[998] = needN(14)
T[999] = LOOK_CUTE
T[1000] = "*: Ai meu... Deixei cair meu precioso\\nmachado no lago. O que vou fazer?"
T[1001] = AHA_CUTE; T[1002] = SOLVE_CUTE
T[1003] = "*: O-o que e isso? Um machado novo?\\nObrigado, Miss Cute!"
T[1004] = SOLVED_CUTE
T[1005] = '*: Claro, o machado que deixei cair era\\numa antiguidade unica feita de ouro\\nmacico, nao um trambolho como este...'
# Part 8
T[1007] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 8'
T[1008] = INTRO_CUTE; T[1009] = WELL_CUTE; T[1010] = needN(13)
T[1011] = LOOK_CUTE
T[1012] = "*: Se eu crescesse so mais alguns\\ncentimetros, o tecnico me poria no\\ntime, com certeza... Suspiro..."
T[1013] = AHA_CUTE; T[1014] = SOLVE_CUTE
T[1016] = SOLVED_CUTE
T[1017] = 'Crianca: Olha mamae! Aquele menino\\ncaido no chao tem um galo na cabeca\\nde uns cinco centimetros de altura!'
T[1018] = "Mae: Vamos, querida. Nao e educado\\nficar encarando."
# Part 9
T[1020] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 9'
T[1021] = INTRO_CUTE; T[1022] = WELL_CUTE; T[1023] = needN(12)
T[1024] = LOOK_CUTE
T[1025] = "*: Minha TV quebrou e nao tenho\\ndinheiro pra comprar uma nova.\\nSuspiro..."
T[1026] = AHA_CUTE; T[1027] = SOLVE_CUTE
T[1028] = '*: Uau! Minha TV virou uma nova\\nem folha! Obrigado, Miss Cute!'
T[1029] = SOLVED_CUTE
T[1030] = '*: Ei, espera ai! Minha HDTV agora e\\num modelo preto e branco com\\nantena!'
T[1031] = "*: Nem sabia que ainda faziam\\nesses..."
# Part 10
T[1033] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 10'
T[1034] = INTRO_CUTE; T[1035] = WELL_CUTE; T[1036] = needN(11)
T[1037] = LOOK_CUTE
T[1038] = "*: Suspiro... Mamae me castigou de novo\\nhoje por nao comer minhas cenouras.\\nQueria poder, mas simplesmente nao da!"
T[1039] = AHA_CUTE; T[1040] = SOLVE_CUTE
T[1041] = "*: O que? Tive uma vontade subita de\\ncenouras! Vou pedir pra mamae fazer\\nagora! Obrigado, Miss Cute!"
T[1042] = SOLVED_CUTE
T[1043] = 'Passante: Papai papai! Olha o\\ncoelho gigante ali!'
# Part 11
T[1045] = '"Miss Cute, Bruxa em Treinamento"\\n                               Parte 11'
T[1046] = INTRO_CUTE; T[1047] = WELL_CUTE; T[1048] = needN(10)
T[1049] = LOOK_CUTE
T[1050] = "*: Suspiro. Nao quero mesmo correr\\nnaquela prova amanha. Talvez eu finja\\nestar doente e fique em casa..."
T[1051] = AHA_CUTE; T[1052] = SOLVE_CUTE
T[1053] = "*: Bem, acho que nao adianta ficar\\nsentado com pena de mim mesmo.\\nVou pra casa..."
T[1054] = SOLVED_CUTE
T[1055] = 'Velho: Fogo! Fogo! A escola esta\\npegando fogo! Socorro!'
# Part 12
T[1058] = INTRO_CUTE; T[1059] = WELL_CUTE; T[1060] = needN(9)
T[1061] = LOOK_CUTE
T[1062] = "*: Suspiro... Meu prazo esta chegando e\\nainda nao penso num tema pro meu\\ntrabalho. O que vou fazer?"
T[1063] = AHA_CUTE; T[1064] = SOLVE_CUTE
T[1065] = "*: Isso! Agora tenho todo tipo de\\nideia passando pela cabeca!\\nObrigado, Miss Cute!"
T[1066] = SOLVED_CUTE
T[1067] = '*: Espera ai! Todas essas ideias\\nsao pessimas! Acho que devia ter\\nsido mais especifico...'
# Part 13
T[1070] = INTRO_CUTE; T[1071] = WELL_CUTE; T[1072] = needN(8)
T[1073] = LOOK_CUTE
T[1074] = '*: Ugh... Comi demais...\\nSinto que meu estomago vai\\nexplodir...'
T[1075] = AHA_CUTE; T[1076] = SOLVE_CUTE
T[1077] = '*: Ei! Me sinto bem melhor agora!\\nObrigado, Miss Cute!'
T[1078] = SOLVED_CUTE
T[1079] = "*: Iii! Espera ai!\\nAgora estou com um estomago enorme!\\nNao e atoa que nao doi mais!"
# Part 14
T[1082] = INTRO_CUTE; T[1083] = WELL_CUTE; T[1084] = needN(7)
T[1085] = LOOK_CUTE
T[1086] = '*: Suspiro... Por que sou tao burro?\\nQueria ser inteligente em algo.\\nQualquer coisa...'
T[1087] = AHA_CUTE; T[1088] = SOLVE_CUTE
T[1089] = '*: Espera ai! Acho que sinto meu\\ncerebro comecar a funcionar mais rapido!'
T[1090] = SOLVED_CUTE
T[1092] = "*: Mas e a unica coisa que sei fazer.\\nQual e o sentido disso?"
# Part 15
T[1095] = INTRO_CUTE; T[1096] = WELL_CUTE; T[1097] = needN(6)
T[1098] = LOOK_CUTE
T[1099] = '*: Suspiro... Por que o Buster tinha de\\nser atropelado por aquele carro?'
T[1100] = AHA_CUTE; T[1101] = SOLVE_CUTE
T[1103] = '*: Buster!\\nVoce voltou!\\nObrigado, Miss Cute!'
T[1104] = SOLVED_CUTE
T[1105] = '*: Eh, Buster...\\nAi nao, o Buster e um cao zumbi!\\nUgh...'
# Part 16
T[1108] = INTRO_CUTE; T[1109] = WELL_CUTE; T[1110] = needN(5)
T[1111] = LOOK_CUTE
T[1112] = '*: Onde estao os meus oculos?\\nNunca acho essas coisas...'
T[1113] = AHA_CUTE; T[1114] = SOLVE_CUTE
T[1115] = '*: Espera ai! Aqui estao!\\nEstavam o tempo todo na minha\\ncabeca! Obrigado, Miss Cute!'
T[1116] = SOLVED_CUTE
T[1117] = "*: Ei! Estes oculos grudaram na minha\\ncabeca! Nao consigo tirar! Socorro!"
# Part 17
T[1120] = INTRO_CUTE; T[1121] = WELL_CUTE; T[1122] = needN(4)
T[1123] = LOOK_CUTE
T[1124] = "*: Suspiro... Queria poder fazer algo\\npra ajudar a empresa do meu\\nneto..."
T[1125] = AHA_CUTE; T[1126] = SOLVE_CUTE
T[1127] = '*: Espera ai! Tive uma ideia!\\nObrigado, Miss Cute!'
T[1128] = SOLVED_CUTE
T[1129] = "*: Mas sera que tudo bem fazer\\nalgo assim. Talvez meu neto\\nPink Mask fique chateado..."
# Part 18
T[1132] = INTRO_CUTE; T[1133] = WELL_CUTE; T[1134] = needN(3)
T[1135] = LOOK_CUTE
T[1136] = '*: Suspiro... Queria ter dinheiro...'
T[1137] = AHA_CUTE; T[1138] = SOLVE_CUTE
T[1139] = "*: O que e isso? Uma revista?\\nE a resposta pro meu problema?\\nObrigado, Miss Cute!"
T[1140] = SOLVED_CUTE
T[1141] = '*: Ei, e so uma revista de vagas\\nde emprego... Se eu quisesse um\\nemprego, ja teria um...'
# Part 19
T[1144] = INTRO_CUTE; T[1145] = WELL_CUTE; T[1146] = needN(2)
T[1147] = LOOK_CUTE
T[1148] = "*: Suspiro... Minha coluna esta me\\nmatando... Nao e nada bom envelhecer..."
T[1149] = AHA_CUTE; T[1150] = SOLVE_CUTE
T[1152] = SOLVED_CUTE
T[1153] = '*: Agora minha cabeca doi! Verdade,\\nesqueci da minha coluna, mas...\\nAi! Chamem uma ambulancia!'
# Part 20
T[1156] = INTRO_CUTE; T[1157] = WELL_CUTE; T[1158] = 'Deixar mais 1 pessoa feliz\\nantes de virar uma\\nbruxa de verdade!'
T[1159] = LOOK_CUTE
T[1160] = 'Rei Bruxo: Cute!'
T[1161] = 'Miss Cute: Essa voz! E voce,\\nPapai?'
T[1162] = "Rei Bruxo: Voce acha mesmo que ajudou\\naquelas pessoas? Voce nao deixou\\numa unica pessoa feliz!"
T[1163] = 'Rei Bruxo: Voce nunca sera uma bruxa\\nde carteirinha nesse ritmo! Vai ter\\nde comecar tudo de novo do zero!'
T[1164] = 'Miss Cute: Aaah! E eu me esforcei\\ntanto, tambem!'
T[1165] = 'Isso parece trabalho pra Miss Cute!\\nAcho.'
T[1166] = SOLVE_OWN
T[1167] = 'E assim Miss Cute voltou no tempo...'
T[1168] = '"Miss Cute, Bruxa em Treino"\\n   Episodios Classicos\\n   Comecando pela Parte 1'
T[1169] = 'O novo programa "Miss Cute, Bruxa\\nem Super Treino" vai ao ar semana\\nque vem neste horario. Nao perca!'
T[1170] = 'A reprise de "Miss Cute, Bruxa em\\nSuper Treino" vai ao ar semana\\nque vem neste horario. Nao perca!'

# ============ Dorothy's Cooking Life ============
DOR_HELLO = 'Dorothy: Ola. Dorothy Gremley aqui.'  # c=37 -> 35
DOR_BYE   = 'Dorothy: Ate semana que vem!\\nCurta sua Cooking Life!'  # c=52
def dor_part(n):
    return '"Dorothy\'s Cooking Life"\\n                                Parte %d' % n
# Part 1
T[1171] = dor_part(1)
T[1172] = DOR_HELLO
T[1173] = 'Dorothy: Na Cooking Life, explico o\\nbasico da culinaria de um jeito que\\nate iniciantes entendem facilmente.'
T[1174] = "Dorothy: Aposto que muitos de voces\\nraramente fazem algo na cozinha. Talvez\\nalguns nunca tenham cozinhado antes."
T[1175] = 'Dorothy: Mas quero que percebam que\\ncozinhar nao e dificil.'
T[1176] = "Dorothy: Que tal comecar entrando na\\ncozinha e fervendo um pouco de agua?\\nNao parece tao dificil, parece?"
T[1177] = 'Dorothy: Pode usar essa agua para fazer\\numa xicara relaxante de cha...'
T[1178] = 'Dorothy: E vai aprender sobre o mundo\\nmaravilhoso da culinaria ao mesmo\\ntempo.'
T[1179] = 'Dorothy: Quando este programa acabar,\\nque tal ir direto pra cozinha e tentar\\nalguns dos pratos que mencionei?'
T[1180] = 'Dorothy: Talvez voce descubra que\\ngosta de cozinhar. Pode tornar sua\\nvida ainda mais agradavel.'
T[1181] = 'Dorothy: Nas proximas semanas, vamos\\napresentar 4 tipos principais de\\npreparo: cortar, ferver, grelhar e assar.'
T[1182] = 'Dorothy: Vamos aprender algo novo a\\ncada semana, entao espero que aguarde\\nansioso nosso tempo juntos.'
T[1183] = 'Dorothy: Nosso tempo de hoje acabou,\\nmas espero que faca uma xicara de cha\\nhoje. Experimente! Voce vai gostar!'
T[1184] = DOR_BYE
# Part 2
T[1185] = dor_part(2); T[1186] = DOR_HELLO
T[1187] = 'Dorothy: Esta semana na Cooking Life,\\nvamos falar de pratos que\\nexigem corte.'
T[1188] = 'Dorothy: Nao importa que faca use,\\ndesde que esteja afiada o bastante\\npra cortar o alimento. So divirta-se.'
T[1189] = 'Dorothy: Dizem que e importante dobrar\\nos dedos pra dentro ao cortar pra\\nnao se cortar, mas...'
T[1190] = 'Dorothy: Nao se preocupe muito com isso\\nagora. O melhor e fazer o que parecer\\nmais facil pra voce.'
T[1191] = 'Dorothy: Se nao tem costume de cortar,\\nva com calma. Mas se ja e experiente,\\npode mandar ver mesmo.'
T[1192] = 'Dorothy: Se nao sabe que tamanho cortar\\nalgo, so tente corta-lo num tamanho que\\nlhe pareca certo.'
T[1193] = 'Dorothy: Se, na hora de comer, achar\\nque ficou grande ou pequeno demais,\\npode fazer diferente da proxima vez.'
T[1194] = 'Dorothy: Tambem recomendo que tente\\nas vezes partir as coisas com as\\nmaos.'
T[1195] = 'Dorothy: Voce se surpreenderia com\\nquantas donas de casa cozinham pra\\nliberar o estresse... Na verdade...'
T[1196] = 'Dorothy: Ah, me desculpe...\\nFugi um pouco do assunto ali.'
T[1197] = 'Dorothy: Quando terminar de cortar seus\\ningredientes, adicione molho ou\\nmaionese e esta pronto pra comer!'
T[1198] = 'Dorothy: Recomendo que procure na sua\\ngeladeira algo que possa cortar\\nhoje.'
T[1199] = DOR_BYE
# Part 3
T[1200] = dor_part(3); T[1201] = DOR_HELLO
T[1202] = 'Dorothy: Esta semana na Cooking Life,\\nvamos falar de como lavar coisas\\ncomo vegetais.'
T[1203] = 'Dorothy: Imagino que alguns de voces\\ntenham feito uma salada apos assistir\\nao programa da semana passada.'
T[1204] = 'Dorothy: Nesta ilha os cultivos crescem\\ncom fertilizantes e herbicidas seguros,\\nentao da pra comer sem lavar.'
T[1205] = 'Dorothy: Mas deixar terra neles pode\\narruinar um prato que seria delicioso.'
T[1206] = 'Dorothy: Voce pode usar uma escova pra\\nlavar vegetais que crescem na terra,\\ncomo cenouras e batatas.'
T[1207] = 'Dorothy: Coisas que crescem acima do\\nsolo como tomates e pepinos absorvem\\nagua facil, entao so lave rapidinho.'
T[1208] = 'Dorothy: Ao lavar verduras de folha,\\nuse bastante agua pra remover a\\nterra das raizes.'
T[1209] = 'Dorothy: Lavar arroz e igual a lavar\\nvegetais -- voce nao quer usar nenhum\\ntipo de sabao ou detergente.'
T[1210] = 'Dorothy: Ao lavar arroz, faca isso\\nrapido pra que o arroz nao absorva\\na agua suja.'
T[1211] = 'Dorothy: E nao se esqueca de que\\nlimpar faz parte de cozinhar.'
T[1212] = 'Dorothy: Voce nao vai se sentir bem\\ncom o que fez se sua cozinha ficar\\numa bagunca depois.'
T[1213] = 'Dorothy: Use o tempo livre que tem\\nenquanto grelha ou ferve alimentos\\npra limpar a cozinha.'
T[1214] = 'Dorothy: E claro, se tem uma lava-louca\\ntotalmente automatica, so precisa\\nenche-la e liga-la.'
T[1215] = DOR_BYE
# Part 4
T[1216] = dor_part(4); T[1217] = DOR_HELLO
T[1218] = 'Dorothy: Esta semana na Cooking Life,\\nvamos falar de ferver\\ndiferentes alimentos.'
T[1219] = 'Dorothy: Isso envolve por agua e caldo\\nnuma panela, adicionar seus\\ningredientes e cozinhar em fogo baixo.'
T[1220] = 'Dorothy: Voce pode fazer uma sopa ou\\nensopado com quase qualquer tipo de\\ningrediente.'
T[1221] = 'Dorothy: So escolha algumas coisas que\\ngostaria de comer e jogue-as na\\npanela!'
T[1222] = 'Dorothy: Claro, nao da pra esperar fazer\\nsopa como um profissional na primeira\\nvez, entao comece com algo simples.'
T[1223] = 'Dorothy: Voce pode tentar ferver\\nalgumas batatas ou milho em um pouco\\nde agua salgada, por exemplo.'
T[1224] = 'Dorothy: Tambem pode comprar misturas\\nde curry ou ensopado prontas que so\\nadicionar aos vegetais cozidos.'
T[1225] = 'Dorothy: Como permitem fazer algo\\nsaboroso sem muito trabalho, por que\\nnao usar uma pra fazer um ensopado?'
T[1226] = 'Dorothy: Adicione os vegetais a panela\\ne aqueca ate comecar a ferver.\\nDepois abaixe o fogo.'
T[1227] = 'Dorothy: So precisa cozinhar os vegetais\\nem fogo baixo ate ficarem prontos,\\nretirando a espuma do topo.'
T[1228] = 'Dorothy: O melhor jeito de saber se os\\nvegetais estao prontos e tirar um dos\\npedacos maiores e prova-lo.'
T[1229] = 'Dorothy: Quando os vegetais ficarem\\nprontos, adicione seu tempero favorito\\ne esta pronto!'
T[1230] = DOR_BYE
# Part 5
T[1231] = dor_part(5); T[1232] = DOR_HELLO
T[1233] = 'Dorothy: Esta semana na Cooking Life,\\nvamos explorar mais a fundo o\\nmundo do corte.'
T[1234] = 'Dorothy: Sabia que pode usar muitas das\\nfrutas e vegetais da Heartflame Island\\npra fazer suco?'
T[1235] = 'Dorothy: Ha varias formas de fazer suco,\\nmas hoje vamos usar um\\nliquidificador.'
T[1236] = 'Dorothy: Ele deixa voce aproveitar o\\nsabor puro das frutas e vegetais, e e\\nbem saudavel tambem. Eu recomendo.'
T[1237] = 'Dorothy: Antes de por os ingredientes\\nno liquidificador, corte-os em\\npedacos de tamanho apropriado.'
T[1238] = 'Dorothy: Isso vale para outros tipos de\\npreparo tambem.'
T[1239] = 'Dorothy: Voce pode usar acucar, mel,\\nleite ou iogurte pra dar sabor.'
T[1240] = 'Dorothy: Adicione ervas ou fatias de\\nfruta como enfeite pra deixar ainda\\nmais bonito.'
T[1241] = 'Dorothy: Alias, a couve e uma das poucas\\ncoisas que se cultiva no inverno, e e\\nbem saudavel pra voce.'
T[1242] = 'Dorothy: Mas muita gente nao gosta do\\ngosto ou cheiro dela, entao tente\\nmistura-la com outros sucos.'
T[1243] = 'Dorothy: Na verdade, estou procurando\\num jeito de tornar o suco de couve\\nainda mais facil de beber.'
T[1244] = 'Dorothy: Acho que vai achar que fazer\\nsuco e um passatempo divertido e\\nfascinante. Experimente!'
T[1245] = DOR_BYE
# Part 6
T[1246] = dor_part(6); T[1247] = DOR_HELLO
T[1248] = 'Dorothy: Falamos de ferver vegetais\\npra fazer ensopado um tempo atras.\\nSeu ensopado ficou bom?'
T[1249] = 'Dorothy: Desta vez, vamos fazer algo\\num pouco mais avancado e\\npreparar nossos proprios temperos.'
T[1250] = 'Dorothy: A culinaria japonesa em geral\\nusa coisas como acucar, miso e molho\\nde soja pra temperar.'
T[1251] = 'Dorothy: A comida ocidental costuma\\nusar sal, pimenta e vinho.'
T[1252] = 'Dorothy: Em ambos os casos, a chave pra\\nfazer algo saboroso e comecar com\\num bom caldo.'
T[1253] = 'Dorothy: Ha muitos tipos de caldo na\\nculinaria japonesa: alga, peixe ou\\ncogumelos shiitake...'
T[1254] = 'Dorothy: Na culinaria ocidental, muitas\\nvezes se faz caldo com ossos de frango\\nou boi com ervas e vegetais.'
T[1255] = 'Dorothy: Mas quem e iniciante ou nao\\ntem muito tempo faz melhor usando\\ncaldo instantaneo.'
T[1256] = 'Dorothy: Ha uma frase simples pra ajudar\\na lembrar a ordem de adicionar temperos\\nna culinaria japonesa.'
T[1257] = 'Dorothy: "Acucar, Sal, Vinagre, Soja\\ne Miso." Em outras palavras, adicione\\nnessa ordem.'
T[1258] = 'Dorothy: Mas no fim, desde que fique\\nsaboroso, nao importa muito que\\nordem voce use.'
T[1259] = 'Dorothy: cozinhar exige\\npratica. Nao da pra esperar que tudo\\nfique perfeito na primeira vez.'
T[1260] = 'Dorothy: Conforme faz os mesmos pratos\\nvarias vezes, vai aprender o que\\nfunciona melhor. Nao desanime com erros.'
T[1261] = DOR_BYE
# Part 7
T[1262] = dor_part(7); T[1263] = DOR_HELLO
T[1264] = 'Dorothy: Esta semana na Cooking Life,\\nvamos falar de grelhar.'
T[1265] = 'Dorothy: Grelhar e seu primo fritar\\nenvolvem cozinhar o alimento sobre\\ncalor direto numa grelha ou frigideira.'
T[1266] = 'Dorothy: Usar uma frigideira ou chapa\\nde ferro ajuda a distribuir o calor\\npor igual, pra dourar bem.'
T[1267] = 'Dorothy: A maioria dos ingredientes\\nfica otima so com uma pitada simples\\nde sal e pimenta.'
T[1268] = 'Dorothy: O tempo que voce grelha sua\\ncomida e voce quem decide, mas\\nbem passado e melhor que cru.'
T[1269] = 'Dorothy: Alimentos que podem ser comidos\\ncrus ou muito frescos so precisam de\\numa rapida passada na frigideira.'
T[1270] = 'Dorothy: Se quer garantir que a comida\\nfique bem cozida por dentro, cubra\\no alimento enquanto grelha.'
T[1271] = 'Dorothy: Tente grelhar voce mesmo. Acho\\nque vai achar facil e surpreendentemente\\ndesafiador ao mesmo tempo.'
T[1272] = DOR_BYE
# Part 8
T[1273] = dor_part(8); T[1274] = DOR_HELLO
T[1275] = 'Dorothy: Esta semana na Cooking Life,\\nvamos falar mais sobre\\ngrelhar.'
T[1276] = 'Dorothy: Na verdade, "assar" talvez seja\\no termo mais apropriado, ja que vamos\\ncozinhar sobre chama aberta.'
T[1277] = 'Dorothy: Cozinhar com fogo e a forma\\nmais antiga de cozinhar,\\nremontando a pre-historia.'
T[1278] = 'Dorothy: Ja viu um peixe num espeto\\nsendo assado sobre uma chama\\naberta?'
T[1279] = 'Dorothy: Esta e uma das formas mais\\nsaborosas de comer peixe.'
T[1280] = 'Dorothy: E claro, fazer o mesmo com\\ncarne se chama "churrasco" e tambem\\ne bem popular.'
T[1281] = 'Dorothy: Porem, como cria muita\\nfumaca, e melhor fazer ao ar\\nlivre.'
T[1282] = 'Dorothy: Se tiver a chance de ir\\nacampar, recomendo que tente fazer\\nchurrasco.'
T[1283] = 'Dorothy: Claro, se tem uma cozinha com\\nsistema de ventilacao de fumaca, pode\\nfazer churrasco quando quiser.'
T[1284] = DOR_BYE
# Part 9
T[1285] = dor_part(9); T[1286] = DOR_HELLO
T[1287] = 'Dorothy: Esta semana na Cooking Life,\\nvamos falar de assar.'
T[1288] = 'Dorothy: Ate quem cozinha bastante as\\nvezes diz que nao costuma assar\\nmuito.'
T[1289] = 'Dorothy: Mas se usar bem o forno, vai\\nver que um novo mundo de bolos,\\nbiscoitos e paes se abre pra voce.'
T[1290] = 'Dorothy: E realmente nao e dificil\\nde fazer.'
T[1291] = 'Dorothy: So precisa preparar os\\ningredientes, por no forno\\ne esperar!'
T[1292] = 'Dorothy: Claro, isso significa que a\\netapa de preparo e muito importante,\\nassim como a temperatura do forno.'
T[1293] = 'Dorothy: Ainda assim, se assistiu a\\nCooking Life esse tempo todo, deve\\nser facil pra voce.'
T[1294] = 'Dorothy: Seu forno ajusta a propria\\ntemperatura, entao so precisa por o\\nalimento na hora certa.'
T[1295] = 'Dorothy: Que tal assar um prato de carne\\nou peixe, junto com alguns vegetais\\npra acompanhar?'
T[1296] = DOR_BYE
# Part 10
T[1297] = '"Dorothy\'s Cooking Life"\\n                                Parte 10'; T[1298] = DOR_HELLO
T[1299] = 'Dorothy: Este e o ultimo episodio da\\nCooking Life, entao gostaria de tentar\\nassar um bolo especial.'
T[1300] = 'Dorothy: Como pode deixar a temperatura\\npor conta do forno, vamos nos\\nconcentrar em fazer o bolo crescer.'
T[1301] = 'Dorothy: Um bolo cresce quando as\\nbolhas de ar na massa se expandem no\\ncalor do forno.'
T[1302] = 'Dorothy: Voce quer misturar a massa sem\\nestourar todas essas bolhas, mas isso\\ne mais facil falar do que fazer.'
T[1303] = 'Dorothy: Levei um bom tempo ate meus\\nbolos crescerem direito.'
T[1304] = 'Dorothy: Se nao curte esse tipo de\\nexperiencia, nao tenha vergonha de\\ncomprar um bolo pronto na loja.'
T[1305] = 'Dorothy: Quando o bolo estiver pronto,\\ne hora de decora-lo.'
T[1306] = 'Dorothy: Pode usar cobertura, frutas da\\nestacao ou chantili pra dar um toque\\nespecial a sua criacao.'
T[1307] = 'Dorothy: Ou pode ate tentar usar nozes\\nou ervas pra um toque diferente.'
T[1308] = 'Dorothy: Obrigada a todos por assistir\\na Cooking Life esse tempo todo.'
T[1309] = 'Dorothy: Espero que continuem cozinhando\\ndaqui pra frente. So experimentem\\nsempre que tiverem um tempo livre.'
T[1310] = 'Dorothy: Se fizerem isso, tenho certeza\\nde que verao que cozinhar acrescentou\\nalgo novo e divertido a sua vida.'
T[1311] = 'Dorothy: Adeus a todos!\\nAproveitem sua Cooking Life!'
T[1312] = 'Sintonize semana que vem para uma\\nreprise de "Cooking Life com Dorothy\\nGremley"!'

# ============ Neo's Weather Report ============
T[1313] = '"Neo\'s Weather Report"'
T[1314] = 'Neo: Tenho noticias importantes! A\\nerupcao da Flame Mountain que previ\\nfoi evitada!'
T[1315] = 'Neo: Por algum motivo, nao consigo\\ndizer quem foi responsavel. Talvez\\ntenha sido alguma forca superior?'
T[1316] = 'Neo: Mas de qualquer modo, o futuro mais\\numa vez se estende a nossa frente.\\nVamos so ficar felizes. E agora...'
T[1317] = 'Neo: Neo, o incrivel vidente,\\ntraz pra voce...a previsao do tempo!'
T[1318] = '"Neo\'s Weather Report"'
T[1319] = 'Neo: Antes do tempo, tenho um anuncio\\na fazer. Decidi me mudar para a\\nHeartflame Island!!'
T[1320] = 'Neo: Por que, voce pergunta? Porque meus\\ninstrumentos me disseram que a Flame\\nMountain vai entrar em erupcao este ano!'
T[1321] = 'Neo: Decidi vir testemunhar esse\\nespetaculo do poder da terra com meus\\nproprios olhos. Pois bem...'
T[1322] = 'Neo: Neo, o incrivel vidente,\\ntraz pra voce...a previsao do tempo!'
T[1323] = '"Neo\'s Weather Report"'
T[1324] = 'Neo: Neo, o incrivel vidente,\\ntraz pra voce...a previsao do tempo!'
T[1326] = 'Neo: O tempo de amanha sera...\\nEnsolarado! Vamos ter tempo bom\\ndesde a manha!'
T[1327] = 'Neo: O tempo de amanha sera...\\nEnsolarado! Vamos ter tempo bom\\ndesde a manha!'
T[1328] = 'Neo: E as flores pela ilha estao\\ncomecando a soltar suas petalas,\\nentao confira!!'
T[1329] = 'Neo: O tempo de amanha sera...\\nEnsolarado! Vamos ter tempo bom\\ndesde a manha!'
T[1330] = 'Neo: E folhas de outono caindo tambem\\npodem ser vistas em alguns lugares,\\nentao confira!'
T[1331] = 'Neo: O tempo de amanha sera...\\nHmm... Chuva o dia todo!'
T[1332] = 'Neo: Hmm... Parece que vai nevar\\no dia todo amanha!'
T[1333] = 'Neo: Vejo uma nevasca pra amanha!\\nO tempo deve ser bem rigoroso!'
T[1334] = 'Neo: Esta vindo a mim! Consigo ver!\\nAmanha, uma grande tempestade vai\\natingir a Heartflame Island!'
T[1335] = 'Neo: Sim, sera um dia muito tempestuoso,\\ncom trovoes e raios!'
T[1336] = 'Neo: Aconselho que durma cedo e colha\\nseus cultivos de manha bem cedo ou\\nserao levados pelo vento!'
T[1337] = 'Neo: Sinto muito, mas simplesmente nao\\nconsigo ver nada. E como se nao\\ntivessemos futuro...'
T[1338] = 'Neo: So nos resta aceitar nosso destino\\ne tentar aproveitar ao maximo o tempo\\nque nos resta...'
T[1339] = 'Neo: Adeus, Heartflame Island!'
T[1340] = 'Neo: Uau! Esta perto! Todos os meus\\npoderes de previsao cientifica dizem\\nque a erupcao da Flame Mountain e ja!'
T[1341] = 'Neo: Se a Flame Mountain entrar em\\nerupcao, a Heartflame Island sera\\ncoberta por lava e cinza quentes!'
T[1342] = 'Neo: Mas decidi ficar aqui!\\nMeu destino e o do meu novo lar,\\na Heartflame Island, serao o mesmo!'
T[1343] = '"Neo\'s Weather Report"\\n         Se quiser me ajudar com a\\n         minha pesquisa, contate-me.'

# ============ Melancholy Woods ============
def mw_part(n):
    return '"Melancholy Woods"\\n                             Parte %d' % n
T[1344] = mw_part(1)
T[1345] = 'Naquela epoca, eu ainda era um ser\\nhumano.'
T[1346] = 'Eu vivia feliz com minha mae,\\nmeu pai, minha irma e meu irmao.'
T[1347] = 'Meu pai era um homem gentil muito\\nestimado por todos.'
T[1348] = 'E minha mae estava sempre sorrindo.\\nTinha um sorriso que iluminava o\\nlugar como um raio de sol.'
T[1349] = 'Meu irmao e minha irma mais velhos\\nme amavam e sempre brincavam comigo.'
T[1350] = 'As vezes brigavamos, mas sempre\\nfaziamos as pazes antes de dormir.'
T[1351] = 'Nossa casa era cheia de risadas.'
T[1352] = 'Essa e a ultima coisa que lembro\\nda epoca em que eu ainda era feliz.'
T[1354] = mw_part(2)
T[1355] = 'De repente nossa sorte mudou.'
T[1356] = 'Eu ainda era jovem na epoca e nao\\nhavia ninguem que explicasse\\nexatamente o que estava acontecendo.'
T[1357] = 'Mas eu sentia que o clima em casa\\nhavia mudado. Ainda me lembro\\ndisso.'
T[1358] = 'Meu pai raramente vinha pra casa.'
T[1359] = 'E minha mae parou de sorrir.'
T[1360] = 'Meu irmao e minha irma sempre\\ntorciam pra ver minha mae ou meu\\npai sorrir, mas nunca sorriam.'
T[1361] = 'Vivemos nesse clima tenso por\\nalgum tempo, ate que...'
T[1363] = mw_part(3)
T[1364] = 'A coisa que finalmente mudou tudo\\nfoi...'
T[1365] = 'A morte do meu pai.'
T[1366] = 'Nao lembro como ele estava\\nna hora da morte.'
T[1367] = 'Mas a expressao no rosto da minha\\nmae esta gravada na minha memoria.'
T[1368] = '"Soube que ele deixou a familia com\\nmuitas dividas."'
T[1369] = 'Ouvi os adultos dizerem isso no\\nfuneral do meu pai.'
T[1370] = 'Meu irmao me explicou o que isso\\nsignificava mais tarde naquela noite.'
T[1371] = 'Meu pai havia emprestado dinheiro a\\num amigo que estava cheio de dividas.'
T[1372] = 'Mas esse amigo desapareceu com o\\ndinheiro, deixando meu pai quase\\nsem nada.'
T[1373] = 'Como ele morreu?\\nNinguem nunca me contou de verdade.'
T[1375] = mw_part(4)
T[1376] = 'Eu nao conseguia imaginar o que\\niamos fazer sem meu pai.'
T[1377] = 'Mas logo a realidade de tudo\\nveio a tona.'
T[1378] = 'Pra pagar o dinheiro que meu pai\\nhavia emprestado pro amigo...'
T[1379] = 'Tivemos de vender a casa que\\namavamos.'
T[1380] = 'A casa tao cheia de lembrancas do\\nmeu pai e do tempo que passamos juntos.'
T[1381] = 'Essas foram as primeiras coisas que\\nperdi, mas nao as ultimas.'
T[1382] = 'Quando se e crianca, ha tantas\\ncoisas que fogem do seu\\ncontrole...'
T[1384] = mw_part(5)
T[1385] = 'Comecamos uma vida nova num\\napartamento velho e caindo aos pedacos...'
T[1386] = 'Minha mae trabalhava ainda mais\\nque meu pai pra nos sustentar.'
T[1387] = 'Ela trabalhava dia e noite em\\nqualquer servico que arranjasse.'
T[1388] = 'Mas nao tinha como ela aguentar\\naquilo por muito tempo.'
T[1389] = 'Por fim, ela desmaiou de exaustao.'
T[1390] = 'Meu irmao e minha irma comecaram a\\ntrabalhar meio periodo pra ajudar\\nnossa mae.'
T[1391] = 'Ela nao teve escolha senao deixar os\\nfilhos trabalharem pra compensar sua\\nincapacidade.'
T[1392] = 'Mas isso mergulhou minha mae ainda\\nmais na depressao.'
T[1393] = 'Tinhamos prazer em fazer qualquer\\ncoisa que fosse preciso, so pra ficar\\njuntos, mas...'
T[1395] = mw_part(6)
T[1396] = 'Era o aniversario da nossa mae.'
T[1397] = 'Tinhamos pouquissimo dinheiro, mas\\nconseguimos juntar um pouco pra\\ncomprar algo pra ela.'
T[1398] = 'Meu irmao, minha irma e eu saimos\\nescondidos e fomos as compras.'
T[1399] = 'Meu irmao comprou um bolinho que\\nminha mae gostava.'
T[1400] = 'E minha irma colheu umas flores\\nbonitas.'
T[1401] = 'E embora eu nao fosse muito artista,\\nfiz o meu melhor pra desenhar minha\\nmae pra dar a ela.'
T[1402] = 'Todos voltamos pra casa juntos.'
T[1403] = 'Mas nossa casa estava...'
T[1404] = 'Em chamas.'
T[1406] = mw_part(7)
T[1407] = 'Disseram que o incendio comecou\\nnum apartamento abaixo do nosso...'
T[1408] = 'O predio inteiro foi reduzido\\na cinzas.'
T[1409] = 'Alguem la disse que havia tentado\\najudar nossa mae a escapar.'
T[1410] = 'Mas disseram que ela recusou as\\ntentativas de resgate, e por isso\\nela morreu.'
T[1411] = 'Nao conseguiamos acreditar!'
T[1412] = 'Sera que nossa mae realmente quis se\\ndespedir dos proprios filhos pra sempre?'
T[1413] = 'Nos tres ficamos ali parados,\\nencarando os escombros fumegantes\\nque eram a nossa casa...'
T[1414] = 'Eu ainda era pequeno na epoca, mas\\nlembro do que percebi entao...'
T[1415] = 'Se voce nao mantem as pessoas que\\nama sempre por perto, nao consegue\\nprotege-las.'
T[1417] = mw_part(8)
T[1418] = 'Nao tinhamos parentes proximos,\\nentao falaram em nos colocar em\\nalgum tipo de orfanato.'
T[1419] = 'Mas meu irmao e minha irma\\ndeixaram claro que iam trabalhar\\nduro pra nos sustentar.'
T[1420] = 'Eu estava apavorado de perder\\nqualquer outra coisa na vida.'
T[1421] = 'Entao eu nao suportava ficar longe\\ndo meu irmao e da minha irma nem\\npor pouco tempo.'
T[1422] = 'Eles nao tinham muito tempo pra\\nlidar comigo, mas...'
T[1423] = 'Eles entendiam como eu me sentia e\\nfaziam o melhor pra me consolar.'
T[1424] = 'Eles viraram como um pai e uma\\nmae pra mim.'
T[1425] = 'Eu estava comecando a me ajustar a\\nessa nossa nova vida quando...'
T[1427] = mw_part(9)
T[1428] = 'Era Natal.'
T[1429] = 'Havia nevado na noite anterior,\\ntornando-o um lindo Natal branco.'
T[1430] = 'Meu irmao, minha irma e eu tinhamos\\nsaido.'
T[1431] = 'Meu irmao segurava minha mao\\ndireita e minha irma segurava a\\nesquerda.'
T[1432] = 'A cidade estava decorada com luzes\\nfestivas e todos nas ruas pareciam\\nde algum jeito alegres.'
T[1433] = 'Animado por esse clima, comecei a\\nsentir o espirito da\\nestacao.'
T[1434] = 'Meu irmao e minha irma estavam\\nobviamente felizes com essa mudanca\\nem mim.'
T[1435] = 'Jurei que faria algo pra retribuir\\nao meu irmao e a minha irma toda a\\nbondade que me mostraram.'
T[1436] = 'Fiz uma promessa a mim mesmo.\\nEu seria forte e os ajudaria como\\neles me ajudaram.'
T[1438] = '"Melancholy Woods"\\n                             Parte 10'
T[1439] = 'Estavamos voltando da nossa modesta\\ncomemoracao de Natal quando\\naconteceu.'
T[1440] = 'Nos tres caminhavamos sob a neve\\nque caia.'
T[1441] = 'Eu sentia que nao havia nada que nos\\ntres nao pudessemos fazer se\\nnos empenhassemos.'
T[1442] = 'Mas claro que isso era so uma ilusao.'
T[1443] = 'Antes que eu percebesse o que tinha\\nacontecido, eu estava sozinho.'
T[1444] = 'Era como se todos os sons do mundo\\ntivessem se apagado, me deixando\\nem silencio.'
T[1445] = 'De algum modo, eu havia soltado\\nas maos deles.'
T[1446] = 'E quando me virei pra procura-los,\\nvi a unica coisa que eu nunca\\nquis ver.'
T[1448] = '"Melancholy Woods"\\n                             Parte 11'
T[1449] = 'Eu tinha me adiantado do meu irmao\\ne irma? Ou eles tinham se adiantado?'
T[1450] = 'Nao lembro muito sobre aquela\\nnoite...'
T[1451] = 'Mas sei que so fui salvo pela mais\\nremota das chances.'
T[1452] = 'Um carro derrapou no gelo e subiu\\nna calcada, atingindo meu irmao\\ne minha irma.'
T[1453] = 'A neve parou de cair.'
T[1454] = 'Fiquei com eles e fiz tudo que pude\\npra nao perde-los, mas foi\\ntudo em vao.'
T[1455] = 'Nao consegui salva-los.'
T[1456] = 'Daquele momento em diante, foi como\\nse algo no meu cerebro\\nsimplesmente desligasse...'
T[1458] = '"Melancholy Woods"\\n                             Parte 12'
T[1459] = 'Meu coracao foi envolto em trevas.'
T[1460] = 'Eu havia fechado meu coracao.\\nTrancado-o nos bosques escuros\\ne melancolicos.'
T[1461] = 'Eu nunca mais deixaria que me\\nferissem.'
T[1462] = 'Muitas pessoas, medicos provavelmente,\\nme examinaram.'
T[1463] = 'Mas eu nao fazia ideia do que estavam\\ndizendo. Eu simplesmente nao ligava.'
T[1464] = 'Eu queria ser um robo.'
T[1465] = 'Assim eu poderia fazer com que\\napagassem essas memorias dolorosas.'
T[1467] = '"Melancholy Woods"\\n                             Parte 13'
T[1468] = 'Eu nao conseguia comer.'
T[1469] = 'Eu nao sabia se estava vivo ou morto.'
T[1470] = 'Passei dia apos dia assim num\\nlugar que suponho ser um hospital.'
T[1471] = 'Sempre que eu via ou ouvia algo...'
T[1472] = 'Lembrava de todas as coisas tristes\\nque haviam acontecido comigo.'
T[1473] = 'A unica coisa que eu podia fazer\\nera virar um robo.'
T[1474] = 'Eu nao veria, nem ouviria, nem\\nsentiria nada. E nao precisaria\\nlembrar.'
T[1476] = '"Melancholy Woods"\\n                             Parte 14'
T[1477] = 'Um dia, o medico me chamou do\\nmeu quarto.'
T[1478] = 'Fui levado pelo corredor do hospital\\nna minha cadeira de rodas.'
T[1479] = 'Por fim, chegamos a uma sala e fui\\nlevado pra dentro.'
T[1480] = 'So pra ver...'
T[1481] = 'Minha irma.'
T[1482] = 'Ela estava toda enfaixada, da\\ncabeca aos pes, mas estava viva.'
T[1483] = 'Quando minha irma me viu, sorriu\\ngentilmente e comecou a chorar\\nde alegria.'
T[1484] = 'Mas quanto a mim...'
T[1486] = '"Melancholy Woods"\\n                             Parte 15'
T[1487] = 'Meu irmao nao resistiu, mas\\nminha irma sobreviveu.'
T[1488] = 'Mas nem descobrir que minha irma\\nvivia conseguiu me fazer abrir\\nmeu coracao.'
T[1489] = 'Mesmo olhando pro rosto da minha irma,\\neu nao sentia nada, como um robo. O\\nmedico estava claramente decepcionado.'
T[1490] = 'Mas minha irma nao deixou minha\\nreacao afeta-la.'
T[1491] = 'Ela disse que era so natural,\\ndado tudo que eu havia passado.'
T[1492] = 'E gentilmente me aceitou como\\neu era.'
T[1494] = '"Melancholy Woods"\\n                             Parte 16'
T[1495] = 'Apesar da dor dos ferimentos...'
T[1496] = 'Minha irma arranjava tempo entre\\nsuas sessoes de reabilitacao...'
T[1497] = 'E passava o maximo de tempo que\\npodia comigo.'
T[1498] = 'Eu nao dizia nada e nenhum traco de\\nemocao aparecia no meu rosto.'
T[1499] = 'Quem nos visse poderia achar que\\nela falava com um robo.'
T[1500] = 'Mas minha irma nao se importava.\\nEla continuava falando comigo...'
T[1501] = 'E as vezes sentava ao meu lado\\ne me lia livros...'
T[1503] = '"Melancholy Woods"\\n                             Parte 17'
T[1504] = 'Minha irma sempre falava de coisas\\nsem importancia como o tempo, ou\\nde como as flores eram bonitas.'
T[1505] = 'Mas aquele dia foi diferente.'
T[1506] = 'Ela se desculpou comigo por me\\nfazer preocupar tanto.'
T[1507] = 'Naquele instante uma unica lagrima\\nescorreu pelo meu rosto.'
T[1508] = 'Eu estava feliz de ter minha irma\\nde volta.'
T[1509] = 'Mas eu sabia que algum dia teria\\nde perde-la de novo.'
T[1510] = 'Meu medo de perde-la me impedia\\nde voltar a realidade...'
T[1512] = '"Melancholy Woods"\\n                             Parte 18'
T[1513] = 'Talvez fosse porque minha irma era\\nmuito mais velha que eu, mas quando\\nnossos pais morreram...'
T[1514] = 'Ela parecia forte o bastante pra\\nlidar com quase tudo.'
T[1515] = 'E agora ela lidava comigo.\\nEla me aceitou como eu era.'
T[1516] = 'Eu nao consegui voltar a ser quem\\neu era antes, mas...'
T[1517] = 'Depois de um tempo comecei a achar\\nque via uma luz no fim do tunel.'
T[1518] = 'Ela ficava comigo o tempo todo,\\nme apoiando com sua forca\\ngentil.'
T[1520] = '"Melancholy Woods"\\n                             Parte 19'
T[1521] = 'No dia em que tive permissao de\\nsair do hospital pela primeira vez...'
T[1522] = 'Minha irma e eu demos nossa primeira\\ncaminhada em eras. Andamos pela cidade.'
T[1523] = 'Eu estava apavorado de sair...'
T[1524] = 'Mas minha irma caminhava ao meu\\nlado, segurando gentilmente minha mao.'
T[1525] = 'Nossa familia de cinco havia sido\\nreduzida a apenas dois.'
T[1526] = 'E um de nos era pouco mais que\\num robo...'
T[1527] = 'Mas minha irma seguia em frente,\\nnunca vacilando, nunca parando.'
T[1528] = 'Ela so seguia em frente...'
T[1530] = '"Melancholy Woods"\\n                     Episodio Final'
T[1531] = 'Naquele instante, um carro veio em\\nnossa direcao em alta velocidade.'
T[1532] = 'Fiquei paralisado, incapaz de\\nme mover.'
T[1533] = 'Mas minha irma pegou minha mao e\\nfacilmente nos tirou do caminho\\ndo carro.'
T[1534] = 'Ela me abracou, mesmo eu ficando\\nali paralisado.'
T[1535] = 'Ela disse que nenhum de nos podia\\nprometer nao morrer...'
T[1536] = 'Mas podiamos prometer dar o nosso\\nmelhor pra viver vidas longas e felizes.'
T[1537] = 'Ela disse que em vez de evitar fazer\\namigos por medo de perde-los...'
T[1538] = 'Deviamos trabalhar juntos pra\\naproveitar o tempo que tinhamos.'
T[1539] = 'E entao ela riu...'
T[1540] = '"Melancholy Woods"\\n                             Fim'
T[1541] = 'Sintonize semana que vem para uma\\nreprise de "Melancholy Woods."'

# ============ Miss Cute, Witch In Super Training ============
# Header built programmatically below via SUPER_HDR; only dialogue here.
SOLVE_OWN = 'Miss Cute: Vou resolver meu proprio\\nproblema com o poder da fofura!\\nHippity hoppity hee! Vou me ajudar!'
SOLVE_YOU = 'Miss Cute: Vou resolver seu\\nproblema com o poder da fofura!\\nHippity hoppity hoo! Vou te ajudar!'

T[1543] = 'Esta e a historia de Miss Cute,\\ndepois de ela crescer um pouco...'
T[1544] = SOLVE_YOU
T[1545] = 'Miss Cute: Consegui!'
T[1546] = "Miss Cute: Finalmente deixei 20 pessoas\\nfelizes!"
T[1547] = 'Miss Cute: Agora sou adulta!\\nEstou voltando pra casa.\\nMe espere, Papai'
T[1548] = '~Reino Magico~'
T[1549] = 'Miss Cute: Cheguei, papai!\\nOlha pra mim, toda crescida'
T[1550] = 'Miss Cute: Me elogie'
T[1551] = 'Miss Cute: E me de um dinheirinho'
T[1552] = 'Rei Bruxo: ..................'
T[1553] = 'Rei Bruxo: CUUUUUUTE!'
T[1554] = 'Miss Cute: Bem...\\nVoce esta bravo comigo, Papai??'
T[1557] = 'Rei Bruxo: CUUUUUUTE!\\nVoce acha mesmo que deixou 20\\npessoas felizes com seu poder?'
T[1558] = "Rei Bruxo: E so coincidencia!\\nUma enorme quantidade de sorte se\\nacumulou e resultou em "
T[1559] = 'MILAGRE'
T[1560] = ' de algo!'
T[1561] = "Rei Bruxo: Pelo modo como usou sua\\nmagia, nao posso te chamar de adulta!!"
T[1562] = 'Miss Cute: O-O-O QUE!\\nMe esforcei tanto, e voltei,\\nacreditando mesmo que tinha conseguido...'
T[1563] = 'Miss Cute: Isso e... severo demais!'
T[1564] = "Rei Bruxo: Escute Cute...\\nVoce sera totalmente responsavel\\npelo Reino Magico inteiro um dia..."
T[1565] = 'Rei Bruxo: Voce vai ter problemas\\nse nao aprender.'
T[1566] = 'Miss Cute: O-O que!\\nVoce me fez responsavel por tudo!'
T[1567] = 'Miss Cute: Se queria tanto,\\ndevia ter tido mais filhos espertos,\\num atras do outro, entao!'
T[1568] = 'Rei Bruxo: UGH, AGH... Minha amada\\nesposa no ceu... Cute disse coisas\\nterriveis. UGH, UGH...'
T[1569] = 'Miss Cute: ...............'
T[1572] = 'Rei Bruxo: *Tosse*... Enfim, ha muitas\\ncoisas que um herdeiro deve aprender,\\ncomo saber, educacao e etiqueta.'
T[1573] = "Rei Bruxo: O importante mesmo e poupar\\nos sentimentos dos outros. Se conseguir,\\nsua magia tambem vai mudar."
T[1574] = 'Rei Bruxo: Entao...\\nDecidi pedir ao Old Man pra te treinar.'
T[1575] = 'Miss Cute: Que Old Man?\\nEle mora no castelo?'
T[1576] = 'Rei Bruxo: Pedi pra ele vir so por\\nvoce. Deixe eu apresentar... Old Man.'
T[1577] = 'Old Man: Prazer em conhece-la, sou Old Man.'
T[1578] = 'Old Man: Nao vou pegar leve com voce,\\nmesmo sendo uma princesa.\\nPrepare-se.'
T[1579] = 'Miss Cute: Que isso?\\n"Old Man" e seu nome?'
T[1580] = 'Miss Cute: Mais importante,\\nnao quero esse Old Man rabugento\\nme treinando!'
T[1581] = 'Rei Bruxo: Nao seja egoista! Este Old Man\\ne conhecido como um educador soberbo.\\nE muito respeitado.'
T[1582] = 'Rei Bruxo: Dei a ele seu boletim.\\nVoce deve ouvi-lo e estudar muito\\npra virar uma adulta responsavel.'
T[1583] = 'Miss Cute: SEM CHANCE!!'
T[1586] = 'Miss Cute: Nao ligo, vou fugir!\\nNem tente me achar, Papai!!'
T[1587] = 'Rei Bruxo: Cute...!'
T[1588] = 'Old Man: Vou segui-la, Rei Bruxo.\\nPor favor nao se preocupe com ela...'
T[1589] = 'Rei Bruxo: Estou contando com voce.\\nEla nao percebe, mas Cute tem\\num poder magico muito forte.'
T[1590] = 'Rei Bruxo: Se um vilao a encontrar...'
T[1591] = 'Old Man: Entendi.\\nPode deixar comigo.\\nCom licenca...'
T[1592] = '~Mundo Humano~'
T[1593] = "Miss Cute: Hmm... Papai, nao gosto de voce.\\nTirano! Cara chato!"
T[1594] = 'Miss Cute: Tambem penso no meu futuro,\\nmas...'
T[1595] = 'Miss Cute: Acabei de virar adulta.\\nHa coisas que posso fazer e\\ncoisas que nao posso.'
T[1596] = 'Miss Cute: E ele trouxe a mamae a tona...'
T[1599] = 'Miss Cute: NOSSA!!\\nNao vou mais me deixar pra baixo...'
T[1600] = SOLVE_OWN
T[1601] = 'Old Man: NAAAAAAO!!'
T[1602] = 'Miss Cute: Uau, voce veio!'
T[1603] = 'Old Man: O que voce vai fazer pra lancar\\num feitico com uma atitude tao mole?\\nVoce e a '
T[1604] = 'Irresponsavel Miss Cute?'
T[1605] = 'Old Man: Pra lancar um feitico, voce precisa\\nvisualizar a consequencia antes.\\nNao aprendeu isso na escola?'
T[1606] = 'Miss Cute: ............'
T[1607] = 'Old Man: Ah cara!\\nSe voce volta no tempo quando\\nerra, nao vai crescer nada!'
T[1608] = 'Miss Cute: Voltar no tempo....?\\nEu...volto no tempo...a cada erro...?'
T[1609] = 'Miss Cute: Voce...\\nComo sabe o que nem eu mesma\\nsei?'
T[1610] = 'Old Man: ..............'
T[1613] = 'Miss Cute: Old Man...\\nVoce e...um vilao!?'
T[1614] = 'Old Man: ...Qualquer um pode ser bom ou mau\\ndependendo de com quem\\nesta lidando.'
T[1615] = 'Old Man: Descobrir a verdade e\\no que importa.'
T[1616] = 'Old Man: Voce deve descobrir a verdade\\nsozinha, Irresponsavel Miss Cute.'
T[1617] = 'Miss Cute: ............'
T[1618] = 'Miss Cute: O que vou fazer...?\\nNao sei...\\no que fazer...'
T[1619] = 'Miss Cute: Num momento como este...'
T[1620] = SOLVE_OWN
T[1621] = 'Miss Cute: ...Hm?'
T[1622] = 'Miss Cute: Nada aconteceu...\\nPOR QUE??'
T[1623] = 'Old Man: Eu cancelei sua magia.'
T[1624] = 'Old Man: Nao vou permitir que voce lance\\nfeiticos irresponsaveis sem ter\\nimagens claras da consequencia.'
T[1625] = 'Miss Cute: GRR...!'
T[1628] = 'Miss Cute: Ta bom entao...'
T[1629] = 'Miss Cute: Hippity hoppity hoo!\\nShiny Shinny Shine!'
T[1630] = 'Old Man: Aquele feitico...!'
T[1631] = 'Miss Cute: Posso usa-lo '
T[1632] = "porque sou adulta!\\n...Que o raio caia dos ceus!!"
T[1633] = 'Miss Cute: ............'
T[1634] = 'Miss Cute: Por que nada aconteceu?'
T[1635] = 'Old Man: Voce falou enquanto lancava\\num feitico. Voce nem sabe o conceito\\nbasico. Que patetico...'
T[1636] = 'Old Man: Alem disso, usou Magia de Trovao\\nsem descobrir a verdade sobre mim.\\nQue barbaro, nada de princesa.'
T[1637] = 'Old Man: A Tentativa de Assassina Miss Cute\\nprecisa de umas chibatadas duras.'
T[1638] = 'Miss Cute: Es...espera...'
T[1639] = 'Miss Cute: YAAAGH...\\nSeus olhos me assustam...'
T[1642] = 'Old Man: Abra Kadabra\\nGirando Girando~...'
T[1643] = 'Miss Cute: Q-que tipo de feitico e esse?'
T[1644] = 'Old Man: Prenda o alvo e puna-a!'
T[1645] = 'Miss Cute: AAG...AAAARGHHHHH!!'
T[1647] = 'Miss Cute: Ai!'
T[1650] = 'Old Man: Heh-Heh-Heh.\\nFoi escrito que\\numa crianca ma precisa de palmadas.'
T[1651] = 'Old Man: Fique assim por um tempo.\\nMoleca Miss Cute.'
T[1654] = 'Miss Cute: Me deixa em paz ja!'
T[1655] = 'Passante A: Uma garota esta sendo punida\\nali! O que ela fez?'
T[1656] = 'Passante B: Ai nao, coitada.\\nEla ainda e so uma crianca.'
T[1657] = 'Passante C: Tanto faz...\\nSua calcinha esta aparecendo.'
T[1658] = 'Miss Cute: ...Minha calcinha!'
T[1659] = 'Miss Cute: Voce e mau, Old Man...\\nQuando esta punindo alguem,\\nvoce nem considerou isso?'
T[1660] = 'Miss Cute: O que voce acha que e a\\ncalcinha de uma garota?'
T[1661] = 'Miss Cute: Tenho certeza de que um homem\\ncomo voce que nao entende o coracao\\nsensivel de uma garota deve ser do mal!'
T[1662] = 'Miss Cute: NOSSA... Nao vou te perdoar...!\\n*Choramingo*......'
T[1664] = 'Miss Cute: AI-AI! A corda foi cortada!\\nQuem fez isso...?'
T[1667] = 'Mulher Misteriosa: Nao acho boa ideia\\ncapturar uma adolescente e\\npuni-la num lugar como este.'
T[1668] = 'Old Man: Uau... Uau...\\nVoce e uma dama de corpo bonito...'
T[1669] = 'Mulher Misteriosa: Voce esta bem?'
T[1670] = 'Miss Cute: S-sim....'
T[1671] = 'Old Man: *TOSSE*....AGHHH, e so parte\\nda disciplina que esta garota deve\\naprender...'
T[1672] = 'Mulher Misteriosa: Essa e a desculpa\\ntipica de todos os homens abusivos...'
T[1673] = 'Old Man: ..............'
T[1674] = 'Mulher Misteriosa: Se ela aceita a\\ndisciplina, nao incomodo mais.\\nAdeus.'
T[1675] = 'Miss Cute: Espera...!'
T[1676] = 'Miss Cute: Eu te odeio, Old Man!!'
T[1677] = 'Old Man: Miss Cute...'
T[1678] = 'Old Man: Talvez eu tenha exagerado... um pouco.\\nEla estava chorando...'
T[1681] = 'Miss Cute: ...E ai, meu pai foi mau. Eu\\nfinalmente completei o que ele mandou.'
T[1682] = 'Miss Cute: Me esforcei, sabe?\\nMas ele chamou de coincidencia,\\nou milagre...'
T[1683] = 'Miss Cute: Nem sei o que fazer agora.\\nSe eu estudar muito,\\nvou virar uma boa adulta?'
T[1684] = 'Mulher Misteriosa: Nao... nao so isso,\\nmas voce precisa vivenciar coisas,'
T[1685] = '\\nenfrentar conflitos e supera-los,\\ne assim que crescemos.'
T[1686] = 'Mulher Misteriosa: Ate a dor que voce\\ncarrega no coracao vai virar forca\\num dia.'
T[1687] = 'Miss Cute: Sera que e verdade.\\nMas eu queria poder crescer\\nsem ter de me sentir triste.'
T[1688] = 'Mulher Misteriosa: ...Voce deve ter\\npassado por momentos dificeis.'
T[1689] = 'Miss Cute: ............'
T[1690] = 'Miss Cute: Senhora...voce e como minha mae.'
T[1691] = 'Mulher Misteriosa: S-senhora...!'
T[1692] = 'Miss Cute: Sera que uma mae e calorosa\\nassim...'
T[1695] = 'Old Man: Me desculpe!\\nNao sei onde Miss Cute esta!'
T[1696] = 'Rei Bruxo: O que voce acabou de dizer?'
T[1697] = 'Old Man: Tentei sentir a presenca dela,\\nmas nao consigo sentir nada.'
T[1698] = 'Old Man: E...e simplesmente\\nimpossivel...'
T[1699] = 'Rei Bruxo: ......Nao me diga...'
T[1700] = 'Rei Bruxo: Ela nao esta nas Trevas...?'
T[1701] = 'Old Man: ...............!!'
T[1702] = 'Old Man: T-trevas....\\nIsso explica tudo.'
T[1703] = 'Old Man: Pegaram ela enquanto eu estava\\nsentimental por um segundo...'
T[1704] = 'Old Man: AGH...a culpa e toda minha.'
T[1705] = 'Old Man: Rei Bruxo....\\nVou trazer ela de volta com certeza.\\nJuro pela minha vida!!'
T[1706] = 'Old Man: Com licenca!'
T[1709] = 'Miss Cute: Onde...estou...eu?'
T[1710] = 'Miss Cute: Nao consigo ver nada,\\nesta tudo escuro...'
T[1711] = 'Miss Cute: Mas e quente...'
T[1712] = 'Miss Cute: E confortavel...'
T[1713] = 'Miss Cute: Queria poder ficar assim\\npra sempre...'
T[1714] = 'Rainha das Trevas: Sim, minha menina.\\nVou te proteger.\\nNao deixo mais ninguem te machucar.'
T[1715] = 'Rainha das Trevas: Quando o mundo for\\ncoberto pelas trevas, todos vao dormir...'
T[1716] = 'Rainha das Trevas: Um mundo de sonhos\\nonde ninguem se machuca.\\nIsso e a paz...meu reino.'
T[1717] = 'Rainha das Trevas: Voce e tao fofa...'
T[1718] = 'Rainha das Trevas: Quero te comer...'
T[1719] = 'Rainha das Trevas: ...com seu enorme...'
T[1720] = 'Rainha das Trevas: poder magico...!'
T[1723] = 'Rei Bruxo: .......!?'
T[1724] = 'Rei Bruxo: Uma vasta forca sombria comecou\\na cobrir o reino inteiro...'
T[1725] = 'Rei Bruxo: Nao significa que...Cute...?'
T[1726] = '~Cidade Principal do Reino Magico~'
T[1727] = 'Homem: O que? Sinto sono de repente...'
T[1728] = 'Mulher: Por que o ceu esta tao escuro...?\\nZzzz...Zzzz...'
T[1729] = "Crianca: *SOB* Estou com medo!\\nZzzz...Zzzz..."
T[1730] = 'Rainha das Trevas: Heh-heh-heh...\\nAs trevas se espalham rapido.\\nVoce ve isso tambem?'
T[1731] = 'Miss Cute: ...........'
T[1732] = 'Rainha das Trevas: E perda de tempo te\\nperguntar. Voce e so uma boneca agora. So\\nouve a minha voz, nao e?'
T[1733] = 'Rainha das Trevas: Vamos terminar.\\nVou usar o poder que voce me deu pra\\ncobrir este Reino com trevas.'
T[1736] = 'Rainha das Trevas: Abra Kadabra\\nDeathcult Pitayahma~...'
T[1737] = 'Rainha das Trevas: O Grandes Trevas,\\ncubram o mundo. Que todos durmam!'
T[1738] = 'Rainha das Trevas: Heh-heh. Seu poder e\\ntao forte. Foi tao facil cobrir o\\nReino Magico com trevas.'
T[1739] = 'Old Man: Ja chega!'
T[1740] = 'Rainha das Trevas: Voce e... o Old Man,\\no abusivo do outro dia!'
T[1741] = 'Old Man: Voce deve devolver nossa Princesa!'
T[1742] = 'Old Man: Oh minha Pobre Princesa...\\nO que aconteceu...voce\\ne uma casca vazia?'
T[1743] = 'Old Man: A Irresponsavel Miss Cute\\ntinha encantos bem melhores.'
T[1744] = 'Old Man: A culpa e minha por nao ver\\na verdade dela, e deixar voce\\nfaze-la cair nas trevas...'
T[1745] = 'Old Man: Aqui, tome minha vida\\ne acorde agora, Princesa!'
T[1746] = 'Rainha das Trevas: O-O que?'
T[1747] = 'Miss Cute: ...........'
T[1750] = 'Miss Cute: Hmm... Quem?'
T[1751] = 'Miss Cute: Ainda nao e de manha, ne?\\nQuero dormir mais...'
T[1752] = 'Miss Cute: .......Zzzz.'
T[1753] = 'Miss Cute: Zzzz...Zzzz...'
T[1754] = 'Miss Cute: NOSSA! Fica quieto!!'
T[1755] = SOLVE_OWN
T[1756] = 'Miss Cute: ...Hein?'
T[1757] = 'Miss Cute: Ahhh! Estou me mexendo\\ndormindo. Sou sonambula!'
T[1758] = 'Miss Cute: Hein...!?'
T[1759] = 'Miss Cute: Foi...um sonho?'
T[1760] = 'Miss Cute: Minha magia nao funcionou...\\nQue pesadelo!\\nUgh... Lembro de algo ruim.'
T[1761] = 'Old Man: Visualize a consequencia na sua\\ncabeca antes de lancar feiticos.\\nNao aprendeu isso na escola?'
T[1762] = 'Miss Cute: Ugh! O Old Man!!'
T[1765] = 'Miss Cute: Onde estou...?'
T[1766] = 'Old Man: Voce finalmente acordou.\\nSenhorita Sonambula Cute...'
T[1767] = 'Miss Cute: Old Man?\\nPor que parece que esta morrendo?'
T[1768] = 'Rainha das Trevas: Ugh! Ela voltou!'
T[1769] = 'Miss Cute: Senhora?\\nVoce era a vila??'
T[1770] = 'Rainha das Trevas: Nao me chame de VELHA!!!'
T[1771] = 'Rainha das Trevas: Bem, nao importa.\\nAquele Old Man vai morrer logo.\\nAlem disso, seu poder magico agora e meu.'
T[1772] = 'Rainha das Trevas: Ate o Rei e impotente\\nnestas trevas profundas.\\nNinguem pode reverte-las.'
T[1773] = 'Miss Cute: Ai nao......'
T[1774] = 'Rainha das Trevas: Bwa-ha-ha...Mal posso\\nesperar este Reino dormir por completo.\\nTchau, pirralha!'
T[1775] = 'Miss Cute: Ela...se foi...'
T[1778] = 'Miss Cute: Papai! O que devo fazer?\\nA culpa e toda minha...'
T[1779] = 'Rei Bruxo: Se acalme, Cute.\\nMetade dos cidadaos adormeceu, mas\\npartes deste castelo ainda estao seguras.'
T[1780] = 'Rei Bruxo: Alem disso, nossa equipe medica\\nesta tentando salvar a vida do Old Man.'
T[1781] = 'Rei Bruxo: Ele pode nao se recuperar\\ntotalmente ainda, mas vai ficar bem.\\nSe recomponha.'
T[1782] = 'Rei Bruxo: E, sobre as trevas\\ncobrindo este Reino...'
T[1783] = 'Rei Bruxo: Como ela disse, nenhuma magia,\\nnem a minha vai funcionar.'
T[1784] = 'Rei Bruxo: Mas, Cute. Voce talvez consiga\\nfazer algo a respeito.'
T[1785] = 'Miss Cute: Mas, eu...'
T[1786] = 'Rei Bruxo: Sim, voce perdeu seu poder.\\nMas voce nao e afetada\\npelas trevas, ao que parece.'
T[1787] = 'Rei Bruxo: Pode ser porque\\nseu poder ainda esta funcionando.'
T[1788] = 'Rei Bruxo: Ate um pequeno fragmento de\\npoder no seu corpo pode ter energia\\nincrivel, se usado direito.'
T[1789] = 'Rei Bruxo: Se mandar esse poder contra\\nas trevas, voce pode atacar a Velha\\nporque ela faz parte delas.'
T[1790] = 'Rei Bruxo: Em outras palavras, se remover\\nas trevas, voce pode derrota-la e\\nrecuperar seu poder!'
T[1791] = 'Miss Cute: ...Entendi.'
T[1792] = 'Miss Cute: Vou tentar!'
T[1795] = SOLVE_YOU
T[1796] = 'Miss Cute: *Ofa*...*Ofa*...'
T[1797] = SOLVE_YOU
T[1798] = 'Miss Cute: *Ofa*...\\nNao consigo...'
T[1799] = 'Rei Bruxo: Sim, voce consegue!\\nVoce so tem de querer\\ncom todo o seu coracao!!'
T[1800] = 'Rei Bruxo: Nao confie na coincidencia ou\\nna natureza, mas na sua vontade forte;\\ne isso que e preciso.'
T[1801] = 'Miss Cute: Mas...'
T[1802] = 'Miss Cute: Ha coisas que nao tem\\njeito!'
T[1803] = 'Miss Cute: Ate minha mae....\\nEla era tao linda, gentil e esperta,\\nmas morreu tao jovem.'
T[1804] = 'Miss Cute: So temos de seguir a corrente\\nneste mundo, nao e mesmo?'
T[1805] = 'Rei Bruxo: Cu... Cute...'
T[1808] = 'Rei Bruxo: Entendo....\\nVoce esta seguindo a corrente,\\nera assim que se sentia.'
T[1809] = 'Miss Cute: ........'
T[1810] = 'Rei Bruxo: Me perdoe...Cute.\\nQuando sua mae morreu, fiquei triste\\ndemais pra pensar em como voce sentia.'
T[1811] = 'Rei Bruxo: Nao tinha como voce,\\numa garotinha, nao ter se ferido...'
T[1812] = 'Miss Cute: Pai...'
T[1813] = 'Rei Bruxo: Mas Cute....\\nE errado so seguir\\na corrente neste mundo.'
T[1814] = 'Rei Bruxo: Mesmo quando acha que nao ha\\nnada que possa fazer, deve se esforcar\\nmais. Devemos lutar por nossas vidas!'
T[1815] = 'Rei Bruxo: Sua mae lutou tao duro pra\\nprolongar a vida, '
T[1816] = '\\nporque queria permanecer nas suas\\nmemorias o maximo possivel.'
T[1817] = 'Miss Cute: Minha mae fez isso...?'
T[1818] = 'Rei Bruxo: Aqui, Cute.\\nVamos tentar de novo. Deseje pelo\\nfuturo de todos no Reino.'
T[1819] = 'Rei Bruxo: Se desejar com forca o\\nbastante, vai virar realidade!'
T[1820] = 'Miss Cute: OK!'
T[1823] = 'Miss Cute: Estou desejando pelo\\nfuturo de todos neste Reino...'
T[1824] = 'Miss Cute: Todos que me observaram\\ncom amor quando fui egoista...'
T[1825] = 'Miss Cute: O povo do castelo, meus amigos\\nque brincaram comigo quando fiquei so...'
T[1826] = 'Miss Cute: E o Old Man que deu a vida\\npra me salvar, e meu pai...'
T[1827] = 'Miss Cute: Vou lancar um feitico com meu\\ndesejo de que todos achem o futuro,\\ne que o futuro deles seja feliz!'
T[1828] = SOLVE_YOU
T[1829] = 'Miss Cute: KHAAH, por favor!\\nQue algo aconteca!'
T[1830] = 'Miss Cute: Nao quero que acabe assim!'
T[1831] = 'Miss Cute: Vou fazer algo acontecer,\\ncom certeza!!'
T[1832] = 'Mamae: Cute...'
T[1833] = 'Miss Cute: Essa voz... e voce, Mae?'
T[1834] = 'Mamae: Cute, so mais um pouco.\\nAqui, eu te ajudo.'
T[1835] = 'Miss Cute: Mamae!!!!!!'
T[1836] = 'Rei Bruxo: UAU!! E um MILAGRE...!!'
T[1839] = 'Rei Bruxo: Ai meu... Nao tinha certeza\\nse iamos conseguir, mas fico feliz que\\nsuperamos essa crise de algum jeito.'
T[1840] = 'Old Man: Sim. Aquela mulher nao pode\\nmais fazer nada,\\nja que a Princesa recuperou o poder.'
T[1841] = 'Rei Bruxo: Que bom saber.\\nEntao...e essa a verdade sobre Cute?'
T[1842] = 'Old Man: Infelizmente...e verdade.'
T[1843] = 'Rei Bruxo: Entao como trocamos nossos\\ncoracoes, e ate a consideracao dela\\npelos outros, '
T[1844] = '\\nque ela finalmente entendeu...'
T[1845] = 'Rei Bruxo: Ela nao lembra de nada\\nde nada?'
T[1846] = 'Old Man: Sim. O poder magico amplificado\\na chocou profundamente, e fez com que\\nela perdesse toda a memoria...'
T[1847] = 'Rei Bruxo: Ai nao!\\nSignifica que temos de comecar do zero\\ntudo de novo...'
T[1848] = 'Rei Bruxo: Misericordia... Ela estava\\nficando como uma herdeira de verdade\\nfinalmente...'
T[1849] = 'Rei Bruxo: GRRR....'
T[1850] = 'Old Man: R-Rei Bruxo, por favor fique\\ncomigo!'
T[1851] = 'Old Man: Rei Bruxo!!!!!!'
T[1852] = 'Volte para:  "Miss Cute,\\nBruxa em Super Treinamento"      Parte 1'
T[1853] = 'Fique ligado na reprise de\\n"Miss Cute, Bruxa em Treinamento"\\nsemana que vem neste horario!'

# ============ Menus / labels at end ============
T[1872] = 'Enviar flores.\\nVer status das flores.\\nOuvir explicacao.\\nPronto.'
T[1873] = 'Ver ou mudar envio.\\nVer status das flores.\\nOuvir explicacao.\\nAnular.'
T[1874] = 'Sobre envio.\\nSobre sementes.\\nSobre status das flores.\\nAnular.'
T[1876] = '  Previsao\\n  Jardim de Ervas\\n  Cooking Life\\n  Drama\\n  Anime\\n  World Ranch\\n  Anular'
T[1877] = 'Comprar gado.\\nVender gado.\\nOuvir explicacao.\\nPronto.'
# 1878 Jersey/Holstein -> keep (proper breeds, fit) NOT translated
T[1879] = 'Ranch: E isso que voce quer?\\n'
T[1880] = 'Ranch: '
T[1881] = "KG\\nVoce nao vera este animal de novo.\\nTem certeza que quer vende-lo?"
T[1882] = 'Sobre gado.\\nSobre envio.\\nSobre pintinhos.\\nSobre ranks de gado.\\nAnular.'
T[1883] = 'Sobre gado.\\nSobre envio.\\nSobre pintinhos.\\nSobre ranks de gado.\\nSobre '
T[1884] = ' gado.\\nAnular.'
T[1885] = 'Desafio aumentou!\\n'
T[1886] = 'Desafio aumentou!\\n'
T[1887] = 'Amor aumentou!\\n'
T[1888] = 'Inteligencia aumentou!\\n'
T[1889] = 'Cozinha aumentou!\\n'
T[1890] = 'Criatividade aumentou!\\n'
T[1891] = 'Humor aumentou!\\n'
# 1892 Life,1893 Forte,1894 Chocobi,1895 Cocoa,1896 Yogi -> proper names, keep
# 1897-1911 Cow N / Sheep N / Chicken N -> short labels, keep EN (briefing says keep)
# 1912 Yogi -> keep

# ============ "To be continued" divider banners ============
# EN literal: \n\n\n-------------------------------\n\n\n\n----------------------------To be continued
# Replace trailing "To be continued" (15) with "Continua" (8) -> shorter, fits c=81
TBC_INDICES = [603, 783, 799, 831, 846, 862, 878, 894,  # Final Z (some)
               1353, 1362, 1374, 1383, 1394, 1405, 1416, 1426, 1437,
               1447, 1457, 1466, 1475, 1485, 1493, 1502, 1511, 1519, 1529]
TBC_PT = '\\n\\n\\n-------------------------------\\n\\n\\n\\n----------------------------Continua'
for _i in TBC_INDICES:
    T[_i] = TBC_PT

# ============ Super Training headers (build with padding to fit chars) ============
# Will be filled in apply step using actual chars from decoded file.
SUPER_TITLE = '"Miss Cute, Bruxa em Super Treinamento"'

# parts mapping: idx -> tail label
SUPER_HDR = {
    1542: 'Parte 1', 1556: 'Parte 2', 1571: 'Parte 3', 1585: 'Parte 4',
    1598: 'Parte 5', 1612: 'Parte 6', 1627: 'Parte 7', 1641: 'Parte 8',
    1653: 'Parte 9', 1666: 'Parte 10', 1680: 'Parte 11', 1694: 'Parte 12',
    1708: 'Parte 13', 1722: 'Parte 14', 1735: 'Parte 15', 1749: 'Parte 16',
    1764: 'Parte 17', 1777: 'Parte 18', 1794: 'Parte 19', 1807: 'Parte 20',
    1822: 'Parte 21', 1838: 'Episodio Final',
}

# ============ FIXUPS: concise PT for blocks still English (override all) ============
FIX = {}
# Pink Mask shop dialogue (33-48)
FIX[33] = 'Pink Mask: Oh! Um cliente? Saudacoes.\\nSou representante da Pink\\nMask Incorporated.'
FIX[34] = 'Pink Mask: Sinto muito, mas nao estou\\naberto pra negocios agora.\\nPoderia voltar mais tarde, por favor?'
FIX[35] = 'Pink Mask: Oh! Um cliente? Saudacoes.\\nSou representante da Pink\\nMask Incorporated.'
FIX[36] = 'Pink Mask: Sinto muito, mas nao estou\\naberto pra negocios agora.\\nPoderia voltar mais tarde, por favor?'
FIX[37] = 'Pink Mask: E uma ilha bem pequena,\\nnao e? Minhas perspectivas de\\nvenda nao parecem promissoras.'
FIX[38] = 'Pink Mask: E uma ilha bem pequena,\\nnao e? Minhas perspectivas de\\nvenda nao parecem promissoras.'
FIX[39] = 'Pink Mask: Ah, entendo.\\nE entao, o que posso te oferecer?'
FIX[41] = 'I?\\nIsso vai ser '
FIX[42] = 'KG.\\nTudo certo assim?'
FIX[43] = 'Pink Mask: Muito obrigado.\\nVou enviar o '
FIX[45] = 'Pink Mask: Sinto muito, mas voce\\nnao parece ter dinheiro suficiente.\\nFique a vontade pra voltar.'
FIX[46] = 'Pink Mask: Mudou de ideia?\\nMuito bem. Volte sempre.'
FIX[47] = 'Pink Mask: Mudou de ideia?\\nMuito bem. Volte sempre.'
FIX[48] = 'Pink Mask: Zzzz....\\nHm... Hm... Hm...'
FIX[77] = 'L\\nTotal '

# Final Z Rangers dialogue
FIX[833] = 'Chefe (radio): Saquei...\\nEntao o Blue nao ajudou...'
FIX[861] = "Super Pink: Nao tem graca...\\nSob..."
FIX[880] = 'Super Pink: Os aliens voltaram\\nas formas verdadeiras...'
FIX[882] = "Super Green: Pink!\\nAinda to gaga por voce!"
FIX[892] = "Grandpa: Desculpe... Me\\nperdoe, por favor..."
FIX[908] = "Pink: Que bom que conheci voces."

# Miss Cute Training - need lines (shorter)
def _need(n):
    return 'Deixar mais %d felizes\\nantes de virar uma\\nbruxa de verdade!' % n
FIX[919] = 'Deixar 20 felizes\\nantes de virar uma\\nbruxa de verdade!'
FIX[932] = _need(19); FIX[947] = _need(18); FIX[959] = _need(17)
FIX[936] = "*: Nao consigo decidir\\nentre eles. Suspiro..."
FIX[961] = "*: Ugh... Engordei muito\\nultimamente. Nao fecho nem\\no ziper da saia..."
FIX[964] = '*: Uau! Minha saia ficou\\nmaior! Agora serve direitinho!\\nObrigada, Miss Cute!'
FIX[978] = '*: Mas agora minha pele esta\\nroxa e manchada... Pareco um\\nmonstro! Garota nenhuma vai me querer...'
FIX[988] = '*: O que? Meus bracos se\\nmovem rapidissimo!'
FIX[1000] = "*: Ai meu... Deixei meu precioso\\nmachado cair no lago. E agora?"
FIX[1005] = '*: Claro, o machado que cai era\\numa antiguidade unica de ouro\\nmacico, nao um trambolho desses...'
FIX[1017] = 'Crianca: Olha mamae! Aquele menino\\ncaido tem um galo na cabeca\\nde uns cinco centimetros!'
FIX[1018] = "Mae: Vamos, querida. Nao e\\neducado ficar encarando."
FIX[1038] = "*: Suspiro... Mamae me castigou hoje\\npor nao comer as cenouras. Queria\\npoder, mas simplesmente nao da!"
FIX[1050] = "*: Suspiro. Nao quero correr\\nnaquela prova amanha. Talvez eu\\nfinja estar doente em casa..."
FIX[1077] = '*: Ei! Bem melhor agora!\\nObrigado, Miss Cute!'
FIX[1086] = '*: Suspiro... Por que sou tao\\nburro? Queria ser esperto em\\nalgo. Qualquer coisa...'
FIX[1089] = '*: Espera! Acho que meu\\ncerebro ficou mais rapido!'
FIX[1099] = '*: Suspiro... Por que o Buster\\nfoi atropelado por aquele carro?'
FIX[1105] = '*: Eh, Buster...\\nAi nao, e um cao zumbi!\\nUgh...'
FIX[1117] = "*: Ei! Estes oculos grudaram\\nna cabeca! Nao saem! Socorro!"
FIX[1148] = "*: Suspiro... Minha coluna doi...\\nNao e bom envelhecer..."
FIX[1153] = '*: Agora minha cabeca doi!\\nEsqueci da coluna, mas...\\nAi! Chamem uma ambulancia!'
FIX[1164] = 'Miss Cute: Aaah! E eu me\\nesforcei tanto!'
FIX[1169] = 'O novo "Miss Cute, Bruxa em\\nSuper Treino" vai ao ar semana\\nque vem aqui. Nao perca!'
FIX[1170] = 'A reprise de "Miss Cute, Bruxa\\nem Super Treino" vai ao ar\\nsemana que vem aqui. Nao perca!'

# Dorothy overflows (concise)
FIX[1174] = "Dorothy: Aposto que muitos quase\\nnao mexem na cozinha. Talvez alguns\\nnunca tenham cozinhado."
FIX[1177] = 'Dorothy: Use essa agua pra fazer\\numa xicara relaxante de cha...'
FIX[1195] = 'Dorothy: Voce nem imagina quantas\\ndonas de casa cozinham pra\\naliviar o estresse... Alias...'
FIX[1203] = "Dorothy: Imagino que alguns fizeram\\numa salada apos verem o\\nprograma passado."
FIX[1205] = 'Dorothy: Mas deixar terra neles\\narruina um prato delicioso.'
FIX[1212] = "Dorothy: Nao vai gostar do que fez\\nse a cozinha virar uma bagunca\\ndepois."
FIX[1219] = 'Dorothy: Isso e por agua e caldo\\nnuma panela, juntar os ingredientes\\ne cozinhar em fogo baixo.'
FIX[1220] = 'Dorothy: Da pra fazer sopa ou\\nensopado com quase qualquer\\ningrediente.'
FIX[1223] = 'Dorothy: Tente ferver umas\\nbatatas ou milho num pouco de\\nagua salgada, por exemplo.'
FIX[1239] = 'Dorothy: Use acucar, mel, leite\\nou iogurte pra dar sabor.'
FIX[1240] = 'Dorothy: Ponha ervas ou fatias\\nde fruta de enfeite pra ficar\\nmais bonito.'
FIX[1250] = 'Dorothy: A culinaria japonesa usa\\ncoisas como acucar, miso e molho\\nde soja pra temperar.'
FIX[1251] = 'Dorothy: A comida ocidental usa\\nmuito sal, pimenta e vinho.'
FIX[1265] = 'Dorothy: Grelhar e seu primo fritar\\nsao cozinhar a comida em calor\\ndireto na grelha ou frigideira.'
FIX[1268] = 'Dorothy: O tempo de grelha e voce\\nquem decide, mas bem passado\\ne melhor que cru.'
FIX[1271] = 'Dorothy: Tente grelhar voce mesmo.\\nVai achar facil e surpreendentemente\\ndesafiador ao mesmo tempo.'
FIX[1277] = 'Dorothy: Cozinhar com fogo e a\\nforma mais antiga, vinda\\nda pre-historia.'
FIX[1290] = "Dorothy: E nao e nada dificil\\nde fazer."
FIX[1299] = "Dorothy: E o ultimo episodio da\\nCooking Life, entao quero tentar\\nassar um bolo especial."
FIX[1302] = 'Dorothy: Misture a massa sem\\nestourar todas essas bolhas, mas\\nisso e mais facil falar que fazer.'
FIX[1305] = "Dorothy: Com o bolo pronto, e\\nhora de decora-lo."
FIX[1308] = 'Dorothy: Obrigada a todos por\\nverem a Cooking Life ate aqui.'
FIX[1310] = "Dorothy: Se fizer, vai ver que\\ncozinhar trouxe algo novo e\\ndivertido pra sua vida."
FIX[1311] = 'Dorothy: Tchau a todos!\\nCurtam sua Cooking Life!'
FIX[1312] = 'Sintonize semana que vem a\\nreprise de "Cooking Life com\\nDorothy Gremley"!'

# Neo overflows
FIX[1315] = "Neo: Por algum motivo, nao sei\\nquem foi o responsavel. Talvez\\numa forca superior?"
FIX[1320] = 'Neo: Por que? Porque meus\\ninstrumentos disseram que a Flame\\nMountain vai explodir este ano!'
FIX[1330] = 'Neo: E folhas de outono caindo\\ntambem podem ser vistas em\\nalguns lugares, confira!'
FIX[1334] = "Neo: Esta vindo! Consigo ver!\\nAmanha, uma grande tempestade\\nvai atingir a Heartflame Island!"
FIX[1337] = "Neo: Sinto muito, mas nao consigo\\nver nada. E como se nao\\ntivessemos futuro..."
FIX[1341] = 'Neo: Se a Flame Mountain explodir,\\na Heartflame Island sera coberta\\nde lava e cinza quentes!'

# Melancholy Woods overflows
FIX[1345] = 'Naquela epoca, eu ainda era\\nhumano.'
FIX[1346] = 'Vivia feliz com minha mae,\\npai, irma e irmao.'
FIX[1349] = 'Meu irmao e irma mais velhos\\nme amavam e sempre brincavam comigo.'
FIX[1350] = 'As vezes brigavamos, mas sempre\\nfaziamos as pazes antes de dormir.'
FIX[1355] = 'De repente a sorte mudou.'
FIX[1356] = 'Eu era jovem na epoca e nao\\nhavia quem explicasse o que\\nestava acontecendo.'
FIX[1358] = 'Meu pai mal vinha pra casa.'
FIX[1365] = 'A morte do meu pai.'
FIX[1367] = 'Mas a expressao no rosto da\\nminha mae ficou na memoria.'
FIX[1368] = '"Soube que ele deixou a familia\\ncom muitas dividas."'
FIX[1370] = 'Meu irmao me explicou o que\\nera mais tarde naquela noite.'
FIX[1371] = 'Meu pai emprestou dinheiro a\\num amigo cheio de dividas.'
FIX[1373] = 'Como ele morreu?\\nNinguem nunca me contou.'
FIX[1385] = 'Comecamos vida nova num\\napartamento velho e caindo...'
FIX[1386] = 'Minha mae trabalhava mais que\\nmeu pai pra nos sustentar.'
FIX[1387] = 'Trabalhava dia e noite em\\nqualquer servico que achava.'
FIX[1390] = 'Meu irmao e irma comecaram a\\ntrabalhar meio periodo pra ajudar.'
FIX[1391] = 'Nao teve escolha senao deixar\\nos filhos trabalharem pra suprir\\nsua incapacidade.'
FIX[1393] = 'Tinhamos prazer em fazer o que\\nfosse preciso, so pra ficar\\njuntos, mas...'
FIX[1396] = 'Era aniversario da mamae.'
FIX[1397] = 'Tinhamos pouco dinheiro, mas\\njuntamos um pouco pra comprar\\nalgo pra ela.'
FIX[1398] = 'Eu, meu irmao e irma saimos\\nescondidos pra comprar.'
FIX[1402] = 'Voltamos pra casa juntos.'
FIX[1403] = 'Mas nossa casa estava...'
FIX[1404] = 'Em fogo.'
FIX[1407] = 'Disseram que o fogo comecou\\nnum apartamento abaixo...'
FIX[1411] = 'Nao conseguiamos crer!'
FIX[1412] = 'Sera que a mamae quis se\\ndespedir dos filhos pra sempre?'
FIX[1420] = 'Eu tinha pavor de perder mais\\nalgo na vida.'
FIX[1421] = "Entao nao suportava ficar longe\\ndo meu irmao e irma nem por\\npouco tempo."
FIX[1425] = 'Eu comecava a me ajustar a\\nessa vida nova quando...'
FIX[1430] = 'Eu, meu irmao e irma tinhamos\\nsaido.'
FIX[1434] = 'Meu irmao e irma estavam bem\\nfelizes com essa mudanca em mim.'
FIX[1443] = 'Antes que eu percebesse,\\neu estava sozinho.'
FIX[1445] = 'De algum modo, soltei as\\nmaos deles.'
FIX[1455] = 'Nao consegui salva-los.'
FIX[1456] = 'Daquele momento, foi como se\\nalgo no meu cerebro simplesmente\\ndesligasse...'
FIX[1459] = 'Meu coracao foi tomado de trevas.'
FIX[1460] = 'Fechei meu coracao. Tranquei-o\\nnos bosques escuros e\\nmelancolicos.'
FIX[1462] = 'Muita gente, medicos talvez,\\nme examinou.'
FIX[1463] = 'Mas eu nao sabia o que diziam.\\nEu so nao ligava.'
FIX[1465] = 'Assim eu poderia mandar apagar\\nessas memorias dolorosas.'
FIX[1468] = 'Eu nao comia.'
FIX[1472] = 'Lembrava de todas as coisas\\ntristes que me aconteceram.'
FIX[1478] = 'Me levaram pelo corredor do\\nhospital na cadeira de rodas.'
FIX[1481] = 'Minha irma.'
FIX[1483] = 'Ao me ver, minha irma sorriu\\ngentil e chorou de\\nalegria.'
FIX[1484] = 'Mas quanto a mim...'
FIX[1489] = "Mesmo olhando o rosto da minha\\nirma, eu nada sentia, como um robo.\\nO medico ficou decepcionado."
FIX[1492] = 'E gentilmente me aceitou\\ncomo eu era.'
FIX[1496] = 'Minha irma arranjava tempo\\nentre as sessoes de reabilitacao...'
FIX[1497] = 'E passava o maximo de tempo\\nque podia comigo.'
FIX[1498] = 'Eu nada dizia e nenhum traco de\\nemocao surgia no meu rosto.'
FIX[1505] = 'Mas aquele dia foi diferente.'
FIX[1506] = 'Ela se desculpou por me fazer\\npreocupar tanto.'
FIX[1507] = 'Nesse instante uma lagrima\\nescorreu pelo meu rosto.'
FIX[1508] = 'Eu estava feliz de ter minha\\nirma de volta.'
FIX[1513] = 'Talvez por minha irma ser bem\\nmais velha que eu, quando\\nnossos pais morreram...'
FIX[1516] = 'Nao voltei a ser quem eu\\nera antes, mas...'
FIX[1521] = 'No dia em que me deixaram sair\\ndo hospital pela primeira vez...'
FIX[1522] = 'Eu e minha irma demos a primeira\\ncaminhada em eras. Andamos pela cidade.'
FIX[1524] = 'Mas minha irma andava ao meu\\nlado, segurando minha mao.'
FIX[1525] = 'Nossa familia de cinco virou\\napenas dois.'
FIX[1527] = 'Mas minha irma seguia em frente,\\nsem vacilar, sem parar.'
FIX[1528] = 'Ela so seguia em frente...'
FIX[1531] = 'Nesse instante, um carro veio\\nem alta velocidade pra cima.'
FIX[1532] = 'Travei, sem conseguir mexer.'
FIX[1534] = 'Ela me abracou, mesmo eu\\nparalisado ali.'
FIX[1536] = 'Mas podiamos prometer dar o\\nnosso melhor pra viver muito\\ne feliz.'
FIX[1538] = 'Deviamos juntos aproveitar o\\ntempo que tinhamos.'
FIX[1541] = 'Sintonize semana que vem a\\nreprise de "Melancholy Woods."'

# Miss Cute Super Training overflows
FIX[1543] = 'E a historia de Miss Cute,\\ndepois de crescer um pouco...'
FIX[1546] = "Miss Cute: Finalmente deixei 20\\npessoas felizes!"
FIX[1547] = 'Miss Cute: Agora sou adulta!\\nEstou indo pra casa.\\nMe espere, Papai'
FIX[1549] = 'Miss Cute: Cheguei, papai!\\nOlha pra mim, crescida'
FIX[1554] = 'Miss Cute: Bem...\\nEsta bravo comigo, Papai??'
FIX[1574] = 'Rei Bruxo: Entao...\\nPedi ao Old Man pra te treinar.'
FIX[1577] = "Old Man: Prazer, sou o Old Man."
FIX[1583] = 'Miss Cute: NEM PENSAR!!'
FIX[1588] = "Old Man: Vou segui-la, Rei Bruxo.\\nNao se preocupe com ela..."
FIX[1593] = "Miss Cute: Hmm... Papai, nao gosto\\nde voce. Tirano! Chato!"
FIX[1596] = 'Miss Cute: E ele falou da mamae...'
FIX[1599] = "Miss Cute: NOSSA!!\\nNao vou mais me abater..."
FIX[1602] = 'Miss Cute: Uau, voce veio!'
FIX[1614] = "Old Man: ...Todos podem ser bons ou\\nmaus dependendo de com quem\\nestao lidando."
FIX[1622] = 'Miss Cute: Nada aconteceu...\\nPOR QUE??'
FIX[1624] = "Old Man: Nao vou deixar voce lancar\\nfeiticos irresponsaveis sem ter\\nimagens claras da consequencia."
FIX[1628] = 'Miss Cute: Ta bom entao...'
FIX[1630] = 'Old Man: Aquele feitico...!'
FIX[1637] = 'Old Man: A Tentativa de Assassina\\nMiss Cute precisa de chibatadas.'
FIX[1639] = 'Miss Cute: YAAAGH...\\nSeus olhos me assustam...'
FIX[1650] = 'Old Man: Heh-Heh-Heh.\\nEsta escrito que crianca ma\\nprecisa de palmada.'
FIX[1656] = 'Passante B: Ai nao, coitada.\\nE so uma criancinha.'
FIX[1657] = 'Passante C: Tanto faz...\\nSua calcinha esta a mostra.'
FIX[1658] = 'Miss Cute: ...Minha calcinha!'
FIX[1660] = "Miss Cute: O que voce acha que\\ne a calcinha de uma garota?"
FIX[1661] = "Miss Cute: Tenho certeza que um\\nhomem que nao entende o coracao\\nsensivel de uma garota e do mal!"
FIX[1662] = "Miss Cute: NOSSA... Nao te perdoo...!\\n*Choramingo*......"
FIX[1664] = 'Miss Cute: AI-AI! A corda foi\\ncortada! Quem fez isso...?'
FIX[1668] = 'Old Man: Uau... Uau...\\nVoce tem um corpo bonito...'
FIX[1671] = 'Old Man: *TOSSE*....AGHHH, e so\\nparte da disciplina que esta\\ngarota deve aprender...'
FIX[1672] = 'Mulher Misteriosa: E a desculpa\\ntipica de todo homem abusivo...'
FIX[1678] = 'Old Man: Talvez eu tenha exagerado...\\num pouco. Ela chorava...'
FIX[1688] = 'Mulher Misteriosa: ...Voce passou\\npor momentos dificeis.'
FIX[1690] = "Miss Cute: Senhora...e como minha mae."
FIX[1696] = 'Rei Bruxo: O que voce disse?'
FIX[1697] = "Old Man: Tentei sentir a presenca\\ndela, mas nao sinto nada."
FIX[1703] = 'Old Man: Pegaram ela enquanto eu\\nfiquei sentimental por um segundo...'
FIX[1704] = "Old Man: AGH...a culpa e minha."
FIX[1705] = 'Old Man: Rei Bruxo....\\nVou traze-la de volta.\\nJuro pela minha vida!!'
FIX[1710] = "Miss Cute: Nao vejo nada,\\nesta tudo escuro..."
FIX[1714] = 'Rainha das Trevas: Sim, minha menina.\\nVou te proteger. Nao deixo mais\\nninguem te machucar.'
FIX[1715] = 'Rainha das Trevas: Quando o mundo for\\ncoberto por trevas, todos dormirao...'
FIX[1716] = "Rainha das Trevas: Um mundo de sonhos\\nsem ninguem ferido. E a paz\\nverdadeira...meu reino."
FIX[1719] = 'Rainha das Trevas: ...com seu enorme...'
FIX[1720] = 'Rainha das Trevas: poder magico...!'
FIX[1725] = "Rei Bruxo: Nao quer dizer...Cute...?"
FIX[1726] = '~Cidade do Reino Magico~'
FIX[1728] = 'Mulher: Por que o ceu esta escuro?\\nZzzz...Zzzz...'
FIX[1729] = "Crianca: *SOB* To com medo!\\nZzzz...Zzzz..."
FIX[1741] = 'Old Man: Devolva nossa Princesa!'
FIX[1742] = 'Old Man: Oh minha Pobre Princesa...\\nO que houve...voce e\\numa casca vazia?'
FIX[1743] = 'Old Man: A Irresponsavel Miss Cute\\ntinha encantos bem melhores.'
FIX[1745] = 'Old Man: Aqui, tome minha vida\\ne acorde agora, Princesa!'
FIX[1766] = "Old Man: Enfim acordou.\\nMiss Sonambula Cute..."
FIX[1770] = 'Rainha das Trevas: Nao me chame\\nde VELHA!!!'
FIX[1771] = "Rainha das Trevas: Bem, tanto faz.\\nO Old Man morre logo. Alem disso,\\nseu poder magico agora e meu."
FIX[1772] = 'Rainha das Trevas: Ate o Rei e\\nimpotente nessas trevas.\\nNinguem pode reverte-las.'
FIX[1774] = "Rainha das Trevas: Bwa-ha-ha...Mal\\nespero o Reino dormir todo.\\nTchau, pirralha!"
FIX[1778] = "Miss Cute: Papai! O que eu faco?\\nA culpa e toda minha..."
FIX[1780] = "Rei Bruxo: Alem disso, nossa equipe\\nmedica tenta salvar o Old Man."
FIX[1783] = "Rei Bruxo: Como ela disse, magia\\nnenhuma, nem a minha vai funcionar."
FIX[1799] = 'Rei Bruxo: Sim, voce consegue!\\nSo precisa querer com todo\\no coracao!!'
FIX[1800] = "Rei Bruxo: Nao confie na sorte ou\\nna natureza, mas na sua vontade\\nforte; e isso que importa."
FIX[1803] = 'Miss Cute: Ate minha mae....\\nEra tao linda, gentil e esperta,\\nmas morreu tao jovem.'
FIX[1808] = "Rei Bruxo: Entendo....\\nVoce esta seguindo a corrente,\\nera assim que se sentia."
FIX[1810] = "Rei Bruxo: Me perdoe...Cute.\\nQuando sua mae morreu, fiquei triste\\ndemais pra ver como se sentia."
FIX[1817] = 'Miss Cute: Minha mae fez isso...?'
FIX[1827] = "Miss Cute: Vou lancar um feitico com\\nmeu desejo de que todos achem o\\nfuturo, e que seja um futuro feliz!"
FIX[1831] = "Miss Cute: Vou fazer algo acontecer,\\ncom certeza!!"
FIX[1839] = "Rei Bruxo: Ai meu... Nao sabia se\\niamos conseguir, mas que bom que\\nsuperamos essa crise de algum jeito."
FIX[1840] = 'Old Man: Sim. Aquela mulher nao\\npode mais nada, ja que a\\nPrincesa recuperou o poder.'
FIX[1846] = 'Old Man: Sim. O poder magico\\namplificado a chocou muito, e fez\\nela perder toda a memoria...'
FIX[1847] = 'Rei Bruxo: Ai nao!\\nEntao temos de comecar do\\nzero tudo de novo...'
FIX[1848] = 'Rei Bruxo: Misericordia... Ela ia\\nvirando uma herdeira de verdade...'
FIX[1850] = 'Old Man: R-Rei Bruxo, por favor\\nfique comigo!'
FIX[1853] = 'Fique ligado na reprise de\\n"Miss Cute, Bruxa em Treino"\\nsemana que vem aqui!'

# Menus
FIX[1872] = 'Enviar flores.\\nVer status das flores.\\nOuvir info.\\nPronto.'
FIX[1874] = 'Sobre envio.\\nSobre sementes.\\nSobre status.\\nAnular.'

# ============ FIX2: second-round tighter fits (override) ============
FIX2 = {}
FIX2[37] = 'Pink Mask: E uma ilha bem pequena,\\nne? Minhas vendas nao parecem\\npromissoras.'
FIX2[38] = 'Pink Mask: E uma ilha bem pequena,\\nne? Minhas vendas nao parecem\\npromissoras.'
FIX2[39] = 'Pink Mask: Ah, entendo.\\nE entao, o que te ofereco?'
FIX2[833] = 'Chefe (radio): Saquei...\\nO Blue nao ajudou...'
FIX2[880] = 'Super Pink: Os aliens voltaram\\nas formas reais...'
FIX2[892] = 'Grandpa: Desculpe... Me\\nperdoe...'
FIX2[908] = "Pink: Que bom conhecer voces."
FIX2[936] = "*: Nao consigo escolher\\nentre eles. Suspiro..."
FIX2[1018] = "Mae: Vamos, querida.\\nNao e educado encarar."
FIX2[1086] = '*: Suspiro... Por que sou tao\\nburro? Queria ser bom em\\nalgo. Qualquer coisa...'
FIX2[1099] = '*: Suspiro... Por que o Buster\\nfoi atropelado pelo carro?'
FIX2[1251] = 'Dorothy: A comida ocidental usa\\nsal, pimenta e vinho.'
FIX2[1330] = 'Neo: E folhas de outono caindo\\ntambem em alguns lugares,\\nconfira!'
FIX2[1334] = "Neo: Esta vindo! Eu vejo!\\nAmanha, uma grande tempestade\\natinge a Heartflame Island!"
FIX2[1350] = 'As vezes brigavamos, mas sempre\\nfaziamos as pazes antes de deitar.'
FIX2[1365] = 'A morte do meu pai'
FIX2[1368] = '"Soube que ele deixou a familia\\ncheia de dividas."'
FIX2[1370] = 'Meu irmao me explicou o que\\nera naquela noite.'
FIX2[1385] = 'Comecamos vida nova num\\napartamento velho...'
FIX2[1387] = 'Trabalhava dia e noite em\\nqualquer servico que tinha.'
FIX2[1391] = 'Nao teve escolha senao deixar\\nos filhos trabalharem pela\\nsua incapacidade.'
FIX2[1403] = 'Mas nossa casa...'
FIX2[1404] = 'Fogo.'
FIX2[1455] = 'Nao pude salva-los.'
FIX2[1456] = 'Daquele momento, foi como se\\nalgo no meu cerebro so\\ndesligasse...'
FIX2[1481] = 'A irma.'
FIX2[1484] = 'Mas eu...'
FIX2[1492] = 'E gentilmente me aceitou\\ncomo eu sou.'
FIX2[1496] = 'Minha irma arranjava tempo\\nentre as sessoes de reabil...'
FIX2[1497] = 'E passava o maximo de tempo\\nque dava comigo.'
FIX2[1498] = 'Eu nada dizia e nenhuma\\nemocao surgia no meu rosto.'
FIX2[1505] = 'Mas aquele dia foi diferente'
FIX2[1507] = 'Nesse instante uma lagrima\\ncorreu pelo meu rosto.'
FIX2[1508] = 'Eu estava feliz de ter a\\nirma de volta.'
FIX2[1521] = 'No dia em que me deixaram sair\\ndo hospital a primeira vez...'
FIX2[1522] = 'Eu e a irma demos a primeira\\ncaminhada em eras. Pela cidade.'
FIX2[1528] = 'Ela so seguia...'
FIX2[1531] = 'Nesse instante, um carro veio\\nveloz pra cima de nos.'
FIX2[1532] = 'Travei, sem me mexer.'
FIX2[1536] = 'Mas podiamos prometer dar o\\nmelhor pra viver muito e feliz.'
FIX2[1546] = "Miss Cute: Enfim deixei 20\\npessoas felizes!"
FIX2[1583] = 'Miss Cute: NEM PENSAR!'
FIX2[1592] = '~Mundo dos Humanos~'  # fits? len 19 > 13. handle below
FIX2[1602] = 'Miss Cute: Uau, voce veio'
FIX2[1614] = "Old Man: ...Todos podem ser bons ou\\nmaus conforme com quem\\nestao lidando."
FIX2[1622] = 'Miss Cute: Nada aconteceu...\\nPOR QUE?'
FIX2[1628] = 'Miss Cute: Ta bom...'
FIX2[1630] = 'Old Man: Esse feitico...!'
FIX2[1637] = 'Old Man: A Tentativa de Assassina\\nMiss Cute precisa de chibata.'
FIX2[1638] = 'Miss Cute: E...espera...'
FIX2[1639] = 'Miss Cute: YAAAGH...\\nSeus olhos assustam...'
FIX2[1657] = 'Passante C: Tanto faz...\\nSua calcinha aparece.'
FIX2[1658] = 'Miss Cute: ...Calcinha!'
FIX2[1660] = "Miss Cute: O que voce acha que\\ne a calcinha de uma menina?"
FIX2[1664] = 'Miss Cute: AI-AI! Cortaram a\\ncorda! Quem fez isso...?'
FIX2[1669] = 'Mulher Misteriosa: Voce ta bem?'
FIX2[1671] = 'Old Man: *TOSSE*....AGHHH, e so\\nparte da disciplina que ela\\ndeve aprender...'
FIX2[1675] = 'Miss Cute: Espera!'
FIX2[1676] = 'Miss Cute: Te odeio, Old Man!!'
FIX2[1678] = 'Old Man: Talvez eu tenha exagerado\\num pouco. Ela chorava...'
FIX2[1688] = 'Mulher Misteriosa: ...Voce passou\\nperrengue.'
FIX2[1703] = 'Old Man: Pegaram ela enquanto eu\\nfiquei sentimental um segundo...'
FIX2[1709] = 'Miss Cute: Onde...estou?'
FIX2[1712] = "Miss Cute: E confortavel.."
FIX2[1714] = 'Rainha das Trevas: Sim, menina.\\nVou te proteger. Ninguem mais\\nvai te machucar.'
FIX2[1716] = "Rainha das Trevas: Um mundo de sonho\\nsem ninguem ferido. E a paz\\nreal...meu reino."
FIX2[1717] = 'Rainha das Trevas: Voce e fofa...'
FIX2[1719] = 'Rainha das Trevas: ...com seu...'
FIX2[1720] = 'Rainha das Trevas: poder...!'
FIX2[1728] = 'Mulher: Por que o ceu ta escuro?\\nZzzz...Zzzz...'
FIX2[1729] = "Crianca: *SOB* Medo!\\nZzzz...Zzzz..."
FIX2[1736] = 'Rainha das Trevas: Abra Kadabra\\nDeathcult Pitaya~...'
FIX2[1742] = 'Old Man: Oh Pobre Princesa...\\nO que houve...e uma\\ncasca vazia?'
FIX2[1743] = 'Old Man: A Irresponsavel Miss Cute\\ntinha encantos melhores.'
FIX2[1745] = 'Old Man: Aqui, tome minha vida\\ne acorde, Princesa!'
FIX2[1746] = 'Rainha das Trevas: O-Que?'
FIX2[1750] = 'Miss Cute: Hmm... Quem?'  # 22 ok? len 22 == c22 fits
FIX2[1754] = 'Miss Cute: Quieto!!'
FIX2[1756] = 'Miss Cute: ...Hein?'  # len 19 == 18? handle
FIX2[1758] = 'Miss Cute: Hein..!?'
FIX2[1768] = 'Rainha das Trevas: Ela voltou!'
FIX2[1770] = 'Rainha das Trevas: Nao me chame\\nde VELHA!'
FIX2[1773] = 'Miss Cute: Ai nao....'
FIX2[1783] = "Rei Bruxo: Como ela disse, magia\\nnenhuma, nem a minha funciona."
FIX2[1785] = 'Miss Cute: Mas, eu..'
FIX2[1808] = "Rei Bruxo: Entendo....\\nVoce segue a corrente,\\nera assim que se sentia."
FIX2[1817] = 'Miss Cute: Mae fez isso...?'
FIX2[1831] = "Miss Cute: Vou fazer algo acontecer\\ncom certeza!"
FIX2[1850] = 'Old Man: R-Rei Bruxo, fique\\ncomigo, por favor!'
FIX2[1890] = 'Criatividade subiu!\\n'

# ============ FIX3: final precise fits ============
FIX3 = {
 936: '*: Nao consigo escolher.\\nSuspiro...',
 1086: '*: Suspiro... Por que sou\\ntao burro? Queria ser bom\\nem algo...',
 1350: 'As vezes brigavamos, mas\\nfaziamos as pazes antes de deitar.',
 1368: '"Soube que deixou a familia\\ncheia de dividas."',
 1387: 'Trabalhava dia e noite em\\nqualquer servico.',
 1492: 'E gentilmente me aceitou\\nassim.',
 1505: 'Mas esse dia foi diferente.',
 1507: 'Nesse instante uma lagrima\\ncorreu.',
 1508: 'Feliz de ter a irma\\nde volta.',
 1583: 'Miss Cute: NAO!',
 1592: 'Mundo Humano~',
 1622: 'Miss Cute: Nada aconteceu...\\nE AI?',
 1630: 'Old Man: Esse feitico..',
 1638: 'Miss Cute: E..espera...',
 1639: 'Miss Cute: YAAAGH...\\nSeus olhos assustam',
 1660: 'Miss Cute: O que voce acha\\nque e a calcinha dela?',
 1669: 'Mulher Misteriosa: Ta bem?',
 1712: 'Miss Cute: Confortavel..',
 1750: 'Miss Cute: Hmm...Quem?',
 1756: 'Miss Cute: Hein?',
 1770: 'Rainha das Trevas:\\nNao sou VELHA!',
 1817: 'Miss Cute: Mae fez isso?',
 1850: 'Old Man: R-Rei Bruxo,\\nfique comigo!',
 644: 'Chefe: Ah..',
}

# ----- Apply -----
B = re.compile(r'^\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
TOK = re.compile(r'<[0-9a-fA-F]{2}>')

# Generic padded headers: idx -> (title, label). Rebuilt to fit chars.
PADDED_HDR = {}
def _reg(idxlabels, title):
    for idx, label in idxlabels.items():
        PADDED_HDR[idx] = (title, label)

# Miss Cute Training
_reg({916:'Parte 1',929:'Parte 2',944:'Parte 3',956:'Parte 4',968:'Parte 5',
      980:'Parte 6',995:'Parte 7',1007:'Parte 8',1020:'Parte 9',1033:'Parte 10',
      1045:'Parte 11',1057:'Parte 12',1069:'Parte 13',1081:'Parte 14',1094:'Parte 15',
      1107:'Parte 16',1119:'Parte 17',1131:'Parte 18',1143:'Parte 19',1155:'Parte 20'},
     '"Miss Cute, Bruxa em Treino"')
# Final Z Rangers
_reg({604:'Parte 2',784:'Parte 13',800:'Parte 14',832:'Parte 16',847:'Parte 17',
      863:'Parte 18',879:'Parte 19',895:'Parte Final',914:'Fim'},
     '"Final Z Rangers"')
# Melancholy Woods
_reg({1344:'Parte 1',1354:'Parte 2',1363:'Parte 3',1375:'Parte 4',1384:'Parte 5',
      1395:'Parte 6',1406:'Parte 7',1417:'Parte 8',1427:'Parte 9',1438:'Parte 10',
      1448:'Parte 11',1458:'Parte 12',1467:'Parte 13',1476:'Parte 14',1486:'Parte 15',
      1494:'Parte 16',1503:'Parte 17',1512:'Parte 18',1520:'Parte 19',
      1530:'Ep. Final',1540:'Fim'},
     '"Melancholy Woods"')
# Dorothy Cooking Life
_reg({1171:'Parte 1',1185:'Parte 2',1200:'Parte 3',1216:'Parte 4',1231:'Parte 5',
      1246:'Parte 6',1262:'Parte 7',1273:'Parte 8',1285:'Parte 9',1297:'Parte 10'},
     '"Dorothy\'s Cooking Life"')

def build_padded(title, label, chars):
    avail = chars - len(title) - 1 - len(label)
    if avail < 1:
        # cannot fit even with one space -> drop spaces, put single space
        spaces = max(0, chars - len(title) - 1 - len(label))
    else:
        spaces = avail
    return title + '\\n' + (' ' * spaces) + label

def build_super_hdr(label, chars):
    # title + \n + (spaces) + label, total visible len <= chars; \n counts as 1
    base = SUPER_TITLE  # len = 39
    # remaining for spaces+label after title and \n
    avail = chars - len(base) - 1 - len(label)
    if avail < 1:
        # too long; reduce title? title is fixed proper-ish; fall back: fewer spaces, maybe 1
        # If avail<1 we cannot fit; reduce spaces to 1 and accept (still must be <=chars)
        spaces = 1
        # if even that overflows, we will skip in validation and keep EN
    else:
        # mimic right alignment: keep modest indentation
        spaces = avail
    return base + '\\n' + (' ' * spaces) + label

# Safe shortening substitutions (applied only when overflowing).
# Order matters; each is a (search, replace) on the raw literal (with \\n etc).
SUBS = [
    ('Voce se surpreenderia com\\nquantas', 'Voce nao imagina quantas'),
    ('voce ', 'vc '), ('Voce ', 'Vc '),
    ('porque ', 'pq '), ('Porque ', 'Pq '),
    ('tambem', 'tb'),
    ('alguem', 'alguem'),
    ('  ', ' '),
    ('!\\n', '!\\n'),
]
ABBR = [
    ('voce', 'vc'), ('Voce', 'Vc'),
    ('tambem', 'tb'),
    ('porque', 'pq'), ('Porque', 'Pq'),
    ('para ', 'pra '), ('Para ', 'Pra '),
    ('esta ', 'ta '), ('Esta ', 'Ta '),
    ('estao', 'tao'),
    ('precisa', 'precisa'),
]

def shorten(cand, chars):
    # Safe-only: collapse accidental double spaces. No word abbreviations
    # (those are handled with proper concise translations in T).
    cur = cand
    while '  ' in cur and len(t2t(cur)) > chars:
        cur = cur.replace('  ', ' ', 1)
    return cur

def load_bjson():
    import json, glob
    bj = {}
    for path in ['tools/_b1.json','tools/_b2.json','tools/_b3.json','tools/_b4.json','tools/_b5.json']:
        try:
            d = json.load(open(path, encoding='utf-8'))
        except FileNotFoundError:
            continue
        for k, v in d.items():
            # convert real newlines to literal backslash-n used by the SCP file
            bj[int(k)] = v.replace('\n', '\\n')
    return bj

def main():
    raw = open(PATH_TR, encoding='utf-8').read()
    blocks = list(B.finditer(raw))
    meta = {int(m.group(1)): int(m.group(3)) for m in blocks}

    # Recover prior subagent translations (_b*.json) - these take priority.
    BJSON = load_bjson()
    for idx, v in BJSON.items():
        T[idx] = v  # prior translations override; later header/builder logic only touches header idxs

    # build super headers now that we have chars
    for idx, label in SUPER_HDR.items():
        if idx in meta:
            T[idx] = build_super_hdr(label, meta[idx])
    # build generic padded headers
    for idx, (title, label) in PADDED_HDR.items():
        if idx in meta:
            T[idx] = build_padded(title, label, meta[idx])
    # FIXUPS override everything (highest priority)
    for idx, v in FIX.items():
        T[idx] = v
    for idx, v in FIX2.items():
        T[idx] = v
    for idx, v in FIX3.items():
        T[idx] = v

    applied = 0
    skipped = []
    out_parts = []
    last = 0
    for m in blocks:
        idx = int(m.group(1)); chars = int(m.group(3))
        text_start = m.start(4); text_end = m.end(4)
        out_parts.append(raw[last:text_start])
        cur = m.group(4)
        # current text without trailing newline(s) belonging to block sep
        cur_body = cur.rstrip('\n')
        trailing = cur[len(cur_body):]
        if idx in T:
            cand = T[idx]
            if len(t2t(cand)) > chars:
                cand = shorten(cand, chars)
            rl = len(t2t(cand))
            ok = True
            reason = ''
            if rl > chars:
                ok = False; reason = 'overflow %d>%d' % (rl, chars)
            if TOK.search(cand):
                ok = False; reason = 'token'
            for ch in cand:
                if ord(ch) > 0x7e:
                    ok = False; reason = 'nonascii ' + hex(ord(ch)); break
            if ok:
                out_parts.append(cand + trailing)
                applied += 1
            else:
                skipped.append((idx, chars, reason, cand[:50]))
                out_parts.append(cur)
        else:
            out_parts.append(cur)
        last = text_end
    out_parts.append(raw[last:])
    open(PATH_TR, 'w', encoding='utf-8', newline='').write(''.join(out_parts))
    print('applied:', applied, 'skipped:', len(skipped))
    for s in skipped:
        print('  SKIP', s)

if __name__ == '__main__':
    main()
