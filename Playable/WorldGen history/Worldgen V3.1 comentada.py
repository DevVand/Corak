import random
#random é uma série de comandos para gerar ou escolher coisas aleatórias
#ele será usado para escolher uma sala aleatória

#deixe para ler as funções para o final
def searchfor(link, exception, salas):
    #lista de salas aceitas
    accepted = []
    #booleana para avaliar (true, mas se só uma coisa falhar, false)
    alltrue = True
    print(">link letters: ", link, "\n>exception letters:",  exception, "\n")

    for sala in salas:
        for excLetter in exception:
            if excLetter in sala:
                #se existir uma letra proibida (exception), false
                alltrue = False
                print(sala, "-", excLetter, "E")
        for linkLetter in link:
            if linkLetter not in sala:
                # se não existir uma letra obrigatória (link), false
                alltrue = False
                print(sala, "-", linkLetter, "L")

        if alltrue:
            # se não existir nenhum erro
            print(sala, "<-----+")
            accepted.append(sala)
        #reset de variáveis
        alltrue = True

    print("accepted list:\n", accepted)
    #ao final, retorna alguma sala na lista de salas aceitas
    #usando um "random.randint" para escolher um número aleatório no index da lista
    return accepted[random.randint(0, len(accepted)-1)]


#importa a lista de salas
maplist = open("maplist.txt", 'r')
#e coloca todas as salas numa lista em formato de String (texto)
salas = []
while True:
    actualmap = maplist.readline()
    if actualmap == '':
        break
    else:
        #todo arquivo .txt cria um "\n" ao pular uma linha
        #essa parte serve para tirar esse "\n"
        salas.append(actualmap[:-1])
print("step1: rooms \n", salas, "\n")
maplist.close

'''
#aqui uma versão da matriz do mapa, que guarda todas as salas
#essa é uma 4x4, cada espaço é uma String
#logo, cada espaço vai ser substituído pelo nome de uma sala

#não entenda só como uma matriz, ou vetor de duas dimensões
#mas, observando os "[]"
#é uma lista[] (mapa)
#guardando várias listas[] (andares)
#que guardam Strings"" (salas)
#[[""]]
level = [["", "", "", ""],
         ["", "", "", ""],
         ["", "", "", ""],
         ["", "", "", ""]]
print(level)
'''

#aqui o mesmo mapa, porém você escolhe as dimensões dele ao rodar o código
#sem a nescessidade de redigitar tudo como a versão acima
level = []
print("step2: map size ")
x = int(input("X > "))
y = int(input("Y > "))

print("\nstep3: map space ")
#X são as salas e Y os andares
for a in range(y):
    #aqui ele insere uma lista[] (os andares)
    level.insert(0, [])
    for b in range(x):
        #e aqui, várias Strings"" (sala) na lista[] (andar) que acabou de criar
        level[0].append("")
    print(level[a])


print("\nstep4: map generation ")
#aqui o programa vai colocar aleatóriamente as salas no mapa
#porém cada sala tem suas regras
#IMPORTANTE: os nomes das salas são explicados no final

#link são letras que uma sala DEVE ter para ser válida
#exception são letras que uma sala NÃO DEVE ter para ser válida
link = []
exception = []
for andar in range(len(level)):
    for sala in range(len(level[andar])):
        #toda sala possuí um X
        #então, se na sala atual existir um X (uma sala já está lá)
        #o programa não checa as regras e passa pra próxima sala
        if "X" not in level[andar][sala]:

            #se estiver no canto esquerdo
            if sala == 0:
                exception.append("L")
            # se estiver no canto direito
            if sala == len(level[andar])-1:
                exception.append("R")
            # se estiver no topo
            if andar == 0:
                exception.append("U")
            # se estiver na base
            if andar == len(level)-1:
                exception.append("D")


            if sala > 0:
                # se a sala anterior linkar à direita
                if "R" in level[andar][sala-1]:
                    link.append("L")
                else:
                    exception.append("L")
            if sala < len(level[andar])-1:
                # se a próxima sala linkar à esquerda
                if "L" in level[andar][sala+1]:
                    link.append("R")
                elif "X" in level[andar][sala+1]:
                    exception.append("R")
            if andar > 0:
                # se a sala acima linkar abaixo
                if "D" in level[andar-1][sala]:
                    link.append("U")
                else:
                    exception.append("U")
            if andar < len(level)-1:
                # se a sala baixo linkar acima
                if "U" in level[andar+1][sala]:
                    link.append("D")
                elif "X" in level[andar+1][sala]:
                    exception.append("D")

            print("\n>sala", sala+1, "andar", andar+1)

            #manda os links, exceções, e a lista de salas para a análise
            #e retorna com uma sala
            level[andar][sala] = searchfor(link, exception, salas)
            print("", level[andar][sala], " <--------------------")
            #reset de variáveis e o loop continua
            exception = []
            link = []

print("\nstep5: map finished ")
print(len(level[0]), "x", len(level))
for andar in level:
    print(andar)

'''
sobre o nome das salas:
UDcorridorX
RUturnX
UroomX
BlankX
LUD3wayX
os nomes seguem um padrão:
DIREÇÃOnomeX

a direção diz onde essa sala tem uma porta
LroomX tem uma porta à esquerda (Left)
UDcorridar tem uma abertura em cima e em baixo (Up, Down)

o nome diz a categoria da sala
corridor: só duas portas retas (cima/baixo ou esquerda/direita)
turn: salas que mudam de direção (da esquerda pra baixo, da direita pra cima)
room: salas únicas, com só uma porta
Blank: salas vazias
3way: salas com 3 portas
hall: salas que se ligam em todos os lados (LRUD)
'''