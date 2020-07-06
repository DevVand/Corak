import random

def searchfor(link, exception, salas):
    ready = []

    alltrue = True

    for sala in salas:
        print(sala)
        for excLetter in exception:
            if excLetter in sala:
                alltrue = False
                print(sala, excLetter, "exception")
        for linkLetter in link:
            if linkLetter not in sala:
                alltrue = False
                print(sala, linkLetter, "link")
        if alltrue:
            ready.append(sala)
        alltrue = True
    print(ready)

    return ready[random.randint(0, len(ready)-1)]


salas = ([],[])
salas[0].append("Rstrt")
salas[0].append("Lend")
salas[0].append("LRcorridor")
salas[0].append("UDcorridor")
salas[0].append("LDturn")
salas[0].append("LUturn")
salas[0].append("RDturn")
salas[0].append("RUturn")
salas[0].append("Lroom")
salas[0].append("Rroom")
salas[0].append("Uroom")
salas[0].append("Droom")
salas[0].append("Blank")
salas[0].append("LUD3way")
salas[0].append("RUD3way")
salas[0].append("LUR3way")
salas[0].append("LDR3way")
salas[0].append("LRUDhall")

for sala in range(len(salas[0])):
    salas[1].append(sala)

'''
arquivo = open("strt", 'r')
arquivo.readline()
arquivo.close
'''

level = (["", "", ""],
         ["", "", ""],
         ["", "", ""])


link = []
exception = []
for andar in range(len(level)):
    for sala in range(len(level[andar])):

        if sala == 0:
            exception.append("L")
        if sala == 2:
            exception.append("R")
        if sala >= 1:
            if "R" in level[andar][sala-1]:
                link.append("L")
            else:
                exception.append("L")
        if andar >= 1:
            if "D" in level[andar-1][sala]:
                link.append("U")
            else:
                exception.append("U")
        if andar == 0:
            exception.append("U")
        if andar == 2:
            exception.append("D")

        level[andar][sala] = searchfor(link, exception, salas[0])
        exception = []
        link = []
print(level)


