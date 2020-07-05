import random
from Game.Corak.dicio import salas
class keep():
    def __init__(S, sala, at):
        S.sala = sala
        S.at = at
        S.type = 1
        keeper.append(S)

'''
    def maphall (Do):
        if Do[2] = "goTo": 
            '''

def insert(level, sala):
    print(sala)
    try:
        Lmod, Rmod, Umod, Dmod = 1, 1, 1, 1
        if "L" in sala: Lmod *= 2
        if "R" in sala: Rmod *= 2
        if "U" in sala: Umod *= 2
        if "D" in sala: Dmod *= 2
        if "_hall" in sala:
            Umod, Dmod, Rmod, Lmod = 6, 6, 6, 6
        while True:
            y = random.randint(0 + Umod, len(level) - 1 - Dmod)
            x = random.randint(0 + Lmod, len(level[0]) - 1 - Rmod)
            if "_hall" not in sala:
                if "X" not in (level[y][x] or level[y+1][x] or level[y][x+1] or level[y-1][x] or level[y][x-1]):
                    if "_key1" in sala:
                        excDistance = 5
                        maxDistance = 16
                        if x <= keeper[0].at[0] or y - 2 <= keeper[0].at[1]: excDistance = 100
                    elif "_key2" in sala:
                        excDistance = 5
                        maxDistance = 16
                        if x + 2 >= keeper[0].at[0] or y + 1 >= keeper[0].at[1]: excDistance = 100
                    elif "_strt" in sala:
                        excDistance = 5
                        maxDistance = 16
                        if  x <= keeper[0].at[0] or y + 2 >= keeper[0].at[1]: excDistance = 100
                    count = 0
                    if excDistance < 100:
                        while x + count != keeper[0].at[0]:
                            if x > keeper[0].at[0]: count -= 1
                            if x < keeper[0].at[0]: count += 1
                        if count < 0: count *= -1
                        finalcount, count = count, 0
                        while y + count != keeper[0].at[1]:
                            if y > keeper[0].at[1]: count -= 1
                            if y < keeper[0].at[1]: count += 1
                        if count < 0: count *= -1
                        finalcount += count
                        if finalcount > excDistance:
                            if finalcount < maxDistance:
                                print(finalcount,"<\n \n \n \n \n \n \n \n \n \n \n \n ")
                                break
            else: break
        print(sala, x, y, "\n")
        keep(sala, [x, y])

        return [x, y]
    except:
        print(x, y, sala)
        for b in level: print(b)
def pathFinder(level, sala,  at):
    x, y, changeX, changeY = at[0], at[1], 0, 0
    currentX = keeper[0].at[0]
    currentY = keeper[0].at[1]
    link = "x"
    for b in level:
        print(b)
    if "L" in sala: x -= 1
    if "R" in sala: x += 1
    if "U" in sala: y -= 1
    if "D" in sala: y += 1
    while currentX + changeX != x or currentY + changeY != y:
        if currentX + changeX < x: changeX += 1
        elif currentX + changeX > x: changeX -= 1
        if currentY + changeY < y: link = "D"
        elif currentY + changeY > y: link = "U"

        level[currentY + changeY][currentX + changeX] = getLinkExc(level, currentY + changeY, currentX + changeX, ["_", link])
        #if "X" not in level[currentY + changeY][currentX + changeX]:
            #changeX -= 1 if changeX > 0 else -1
        level[currentY + changeY][currentX + changeX] += "mod"

        if currentY + changeY < y: changeY += 1
        elif currentY + changeY > y: changeY -= 1
        if currentX + changeX < x: link = "R"
        elif currentX + changeX > x: link = "L"

        level[currentY + changeY][currentX + changeX] = getLinkExc(level, currentY + changeY, currentX + changeX, ["_", link])
        #if "X" not in level[currentY + changeY][currentX + changeX]:
            #changeY -= 1 if changeY > 0 else -1

        level[currentY + changeY][currentX + changeX] += "mod"

        print("currentX", currentX)
        print("currentY", currentY)
        print(x)
        print(y)
        print(level[y][x])

    print(sala, at)
    return level
def getLinkExc(level, andar, sala, mod):
    link = []
    exception = []
    if "X" not in level[andar][sala]:
        if sala == 0: exception.append("L")
        if sala == len(level[andar]) - 1: exception.append("R")
        if andar == 0: exception.append("U")
        if andar == len(level) - 1: exception.append("D")
        if sala > 0:
            # se a sala anterior linkar à direita
            if "R" in level[andar][sala - 1]: link.append("L")
            elif "X" in level[andar][sala - 1]: exception.append("L")
        if sala < len(level[andar]) - 1:
            # se a próxima sala linkar à esquerda
            if "L" in level[andar][sala + 1]: link.append("R")
            elif "X" in level[andar][sala + 1]: exception.append("R")
        if andar > 0:
            # se a sala acima linkar abaixo
            if "D" in level[andar - 1][sala]: link.append("U")
            elif "X" in level[andar - 1][sala]: exception.append("U")
        if andar < len(level) - 1:
            # se a sala baixo linkar acima
            if "U" in level[andar + 1][sala]: link.append("D")
            elif "X" in level[andar + 1][sala]: exception.append("D")
        if "_" in mod:
            exception.append("Blank")
            exception.append("room")
            for tolink in mod[1]: link.append(tolink)
        #print(">link letters: ", link, "\n>exception letters:", exception, "\n")
        try:
            level[andar][sala] = searchfor(link, exception, salas)

        except:
            for b in level: print(b)
            print(andar, sala)
    return level[andar][sala]
def searchfor(link, exception, salas):
    accepted = []
    alltrue = True
    #print(">link letters: ", link, "\n>exception letters:",  exception, "\n")
    for sala in salas:
        for excLetter in exception:
            if excLetter in sala:
                alltrue = False
                #print(sala, "-", excLetter, "E")
        for linkLetter in link:
            if linkLetter not in sala:
                alltrue = False
                #print(sala, "-", linkLetter, "L")
        if alltrue:
            #print(sala, "<-----+")
            accepted.append(sala)
        alltrue = True
    temp2 = accepted[random.randint(0, len(accepted)-1)]
    accepted = accepted[random.randint(0, len(accepted) - 1)]
    if "hall" not in temp2: accepted = temp2
    #print("accepted list:\n", accepted)
    return accepted
def fixer(level, andar, sala):
    try:
        link = []
        alltrue = True
        if "L" in level[andar][sala]:
            if sala > 0:
                if "R" in level[andar][sala - 1]:
                    link += "L"
                    alltrue = False
        if "R" in level[andar][sala]:
            if sala < len(level[andar]) - 1:
                if "L" in level[andar][sala + 1]:
                    link += "R"
                    alltrue = False
        if "U" in level[andar][sala]:
            if andar > 0:
                if "D" in level[andar - 1][sala]:
                    link += "U"
                    alltrue = False
        if "D" in level[andar][sala]:
            if andar < len(level) - 1:
                if "U" in level[andar + 1][sala]:
                    link += "D"
                    alltrue = False
        if not alltrue:
            level[andar][sala] = ""
            level[andar][sala] = getLinkExc(level, andar, sala, link)
        return level[andar][sala]
    except:
        for b in level: print(b)
        print(andar, sala)
def strt():
    level = []
    print("step1: map size")
    x = 16
    y = 16

    #x = int(input("X > "))
    #y = int(input("Y > "))

    print("\nstep2: map space")
    for temp in range(y):
        level.insert(0, [])
        for temp2 in range(x):
            level[0].append("")
        print(level[temp])

    print("\nstep3: main inputs")
    temp = []
    for sala in open("../../Salas/tokeeplist.txt", 'r'):
        if "_strt" in sala:
            temp.append(sala[:-1])
            times = 1
        if "_hall" in sala:
            temp.append(sala[:-1])
            times = 1
        if "_key1" in sala:
            temp.append(sala[:-1])
            times = 1
        if "_key2" in sala:
            temp.append(sala[:-1])
            times = 1
        if "x" in sala:
            for special in range(times):
                special = random.choice(temp)
                at = insert(level, special)
                level[at[1]][at[0]] = special
                if "_hall" not in special: level = pathFinder(level, special, [at[0], at[1]])
                temp = []

    print("\nstep4: path finding")
    for andar in level:
        print(andar)

    print("\nstep5: map generation")
    for temp2 in range(2):
        for andar in range(len(level)):
            for sala in range(len(level[andar])):
                if temp2 == 1: level[andar][sala] = getLinkExc(level, andar, sala, "")
                if temp2 == 2: level[andar][sala] = fixer(level, andar, sala)
            #print(">sala", sala + 1, "andar", andar + 1, ":", level[andar][sala])
        for andar in level:
            print(andar)

    print(len(level[0]), "x", len(level))


    print("\nstep6: map finished")
    for sala in range(len(keeper)):
        print(keeper[sala].sala, "at", keeper[sala].at)
    return level

keeper = []

level = strt()
