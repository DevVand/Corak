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
salas[0].append("RstrtX")
salas[0].append("LendX")
salas[0].append("LRcorridorX")
salas[0].append("UDcorridorX")
salas[0].append("LDturnX")
salas[0].append("LUturnX")
salas[0].append("RDturnX")
salas[0].append("RUturnX")
salas[0].append("LroomX")
salas[0].append("RroomX")
salas[0].append("UroomX")
salas[0].append("DroomX")
salas[0].append("BlankX")
salas[0].append("LUD3wayX")
salas[0].append("RUD3wayX")
salas[0].append("LRU3wayX")
salas[0].append("LRD3wayX")
salas[0].append("LRUDhallX")

for sala in range(len(salas[0])):
    salas[1].append(sala)

'''
arquivo = open("strt", 'r')
arquivo.readline()
arquivo.close
level = (["", "", ""],
         ["", "", ""],
         ["", "", ""])


level = (["", "", "", "", ""],
         ["", "", "", "", ""],
         ["", "", "", "", ""],
         ["", "", "", "", ""],
         ["", "", "", "", ""])
'''

level = (["", "", "", "", "", ""],
         ["", "", "", "", "", ""])

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
                if "R" in level[andar][sala-1]:
                    link.append("L")
                else:
                    exception.append("L")
            if sala < len(level[andar])-1:
                if "L" in level[andar][sala+1]:
                    link.append("R")
            if andar > 0:
                if "D" in level[andar-1][sala]:
                    link.append("U")
                else:
                    exception.append("U")
            if andar < len(level)-1:
                if "U" in level[andar+1][sala]:
                    link.append("D")

            level[andar][sala] = searchfor(link, exception, salas[0])
            print(">", level[andar][sala], "<")
            exception = []
            link = []

print(level[0])
print(level[1])


print(len(level[0]), "", len(level))


