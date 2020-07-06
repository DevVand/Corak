import random

def searchfor(link, exception, salas):
    accepted = []
    alltrue = True
    print(">link letters: ", link, "\n>exception letters:",  exception, "\n")

    for sala in salas:
        for excLetter in exception:
            if excLetter in sala:
                alltrue = False
                print(sala, "-", excLetter, "E")
        for linkLetter in link:
            if linkLetter not in sala:
                alltrue = False
                print(sala, "-", linkLetter, "L")

        if alltrue:
            print(sala, "<-----+")
            accepted.append(sala)
        alltrue = True

    print("accepted list:\n", accepted)
    return accepted[random.randint(0, len(accepted)-1)]


maplist = open("maplist.txt", 'r')
salas = []
while True:
    actualmap = maplist.readline()
    if actualmap == '':
        break
    else:
        salas.append(actualmap[:-1])
print("step1: rooms \n", salas, "\n")
maplist.close

'''
level = [["", "", "", ""],
         ["", "", "", ""],
         ["", "", "", ""],
         ["", "", "", ""]]
print(level)
'''


level = []
print("step2: map size ")
x = int(input("X > "))
y = int(input("Y > "))

print("\nstep3: map space ")

for a in range(y):

    level.insert(0, [])
    for b in range(x):

        level[0].append("")
    print(level[a])


print("\nstep4: map generation ")
link = []
exception = []
for andar in range(len(level)):
    for sala in range(len(level[andar])):
        if "X" not in level[andar][sala]:

            if sala == 0:
                exception.append("L")
            if sala == len(level[andar])-1:
                exception.append("R")
            if andar == 0:
                exception.append("U")
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

            level[andar][sala] = searchfor(link, exception, salas)
            print("", level[andar][sala], " <--------------------")

            exception = []
            link = []

print("\nstep5: map finished ")
print(len(level[0]), "x", len(level))
for andar in level:
    print(andar)
