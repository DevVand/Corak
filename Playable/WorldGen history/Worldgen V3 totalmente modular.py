import random

def searchfor(link, exception, salas):
    ready = []
    alltrue = True
    print(link, "\n",  exception)

    for sala in salas:
        for excLetter in exception:
            if excLetter in sala:
                alltrue = False
                print(sala, excLetter, "E")
        for linkLetter in link:
            if linkLetter not in sala:
                alltrue = False
                print(sala, linkLetter, "L")
        if alltrue:
            print(sala, "<-----+")
            ready.append(sala)

        alltrue = True
    print(ready)

    return ready[random.randint(0, len(ready)-1)]


maplist = open("maplist.txt", 'r')

salas = []
while True:
    actualmap = maplist.readline()
    if actualmap == '':
        break
    else:
        salas.append(actualmap[:-1])
print(salas)
maplist.close

'''
level = [["", "", "", ""],
         ["", "", "", ""],
         ["", "", "", ""],
         ["", "", "", ""]]

print(level)
'''
level = []
x = int(input("X >"))
y = int(input("Y >"))

for a in range(y):
    level.insert(0, [])
    for b in range(x):
        level[0].append("")
print(level)




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
                elif "X" in level[andar][sala+1]:
                    exception.append("R")
            if andar > 0:
                if "D" in level[andar-1][sala]:
                    link.append("U")
                else:
                    exception.append("U")
            if andar < len(level)-1:
                if "U" in level[andar+1][sala]:
                    link.append("D")
                elif "X" in level[andar+1][sala]:
                    exception.append("D")

            level[andar][sala] = searchfor(link, exception, salas)
            print("----------->", level[andar][sala], "<-----------")
            exception = []
            link = []

for andar in level:
    print(andar)
print(len(level[0]), "", len(level))