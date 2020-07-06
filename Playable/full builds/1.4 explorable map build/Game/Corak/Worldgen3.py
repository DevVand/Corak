import random
from Game.Corak.dicio import salas, U, R, L, D, mapSize
class keep():
    def __init__(S, sala, at):
        S.sala = sala
        S.at = at
        S.type = 1
        keeper.append(S)

def hall(Do, obj):
    out = 0
    if Do[2] == "clear": clearall()
    if Do[2] == "strt": out = strt()
    if "get_pos" in Do[2]: out = get_pos(Do, obj)
    return out

def get_pos(Do, level):
    if "strt" in Do[2]:
        out = keeper[1].at
        print(out)
        corak = keep("at", out)

    if "change_room" in Do[2]:
        corak.at[0] += Do[0]
        corak.at[1] += Do[1]
        out = corak

    return out
def clearall():
    while len(keeper) > 0: del keeper[0]

def insert(level, sala):
    Lmod = Rmod = Umod = Dmod = counter = 1
    if "L" in sala: Lmod *= 2
    if "R" in sala: Rmod *= 2
    if "U" in sala: Umod *= 2
    if "D" in sala: Dmod *= 2
    if "_hall" in sala: Umod = Dmod = Rmod = Lmod = 7
    while True:
        if counter == 200: return [0, 0, 0, 0]
        counter += 1
        y = random.randint(0 + Umod, len(level) - 1 - Dmod)
        x = random.randint(0 + Lmod, len(level[0]) - 1 - Rmod)
        if "_hall" not in sala:
            if "X" not in (level[y][x] or level[y+1][x] or level[y][x+1] or level[y-1][x] or level[y][x-1]):
                if "_key1" in sala:
                    excDistance = 6
                    maxDistance = 16
                    if x <= keeper[0].at[0] or y - 2 <= keeper[0].at[1]: excDistance = 100
                elif "_key2" in sala:
                    excDistance = 6
                    maxDistance = 16
                    if x + 2 >= keeper[0].at[0] or y + 1 >= keeper[0].at[1]: excDistance = 100
                elif "_strt" in sala:
                    excDistance = 6
                    maxDistance = 16
                    if x <= keeper[0].at[0] or y + 2 >= keeper[0].at[1]: excDistance = 100
                elif "_end" in sala:
                    excDistance = 6
                    maxDistance = 16
                    if x >= keeper[0].at[0] or y <= keeper[0].at[1]: excDistance = 100
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
                            break

        else: break
    if "_hall" in sala:
        level[y + U][x] = level[y][x + R] = level[y + D][x] = level[y][x + L] = "X"
    keep(sala, [x, y])
    return [x, y]
def pathFinder(level, sala, x, y):
    try:
        changeX, changeY, count = keeper[0].at[0], keeper[0].at[1], 0
        if "L" in sala: x += L
        elif "R" in sala: x += R
        elif "U" in sala: y += U
        elif "D" in sala: y += D
        mod = [[0, 0], [0, -1], [1, 0], [-1, 0], [0, 1]]
        changeX += mod[len(keeper)-1][0]
        changeY += mod[len(keeper)-1][1]
        level[changeY][changeX] = ' '


        while changeX != x or changeY != y:
            'caso o mapa demore para gerar'
            if count == 500: return [0, 0, 0, 0]
            if count == 100:
                for temp2 in range(len(level)):
                    for temp3 in range(len(level[temp2])):
                        if "mod-" + sala[-4:] in level[temp2][temp3]:  level[temp2][temp3] = "000"
                changeX, changeY = keeper[0].at[0], keeper[0].at[1]
            if count == (50 or 450):
                for b in range(1, 5):
                    temp = [keeper[0].at[0], keeper[0].at[1]]
                    for temp2 in range(len(level)):
                        for temp3 in range(len(level[temp2])):
                            if "mod-" + sala[-4:] in level[temp2][temp3]:
                                if abs(temp[0]-x) + abs(temp[1]-y) > abs(temp3-x) + abs(temp2-y):
                                    temp = [temp3, temp2]
                    changeX = temp[0]
                    changeY = temp[1]
                    if temp[0] > len(level[0]) or temp[1] > len(level): return [0, 0, 0, 0]
                    level[changeX][changeX] = '000'
            if count == 20:
                temp = [keeper[0].at[0]*5, keeper[0].at[1]*5]
                for temp2 in range(len(level)):
                    for temp3 in range(len(level[temp2])):
                        if "mod-" + sala[-4:] in level[temp2][temp3]:
                            if abs(temp[0]-x) + abs(temp[1]-y) > abs(temp3-x) + abs(temp2-y):
                                temp = [temp3, temp2]
                changeX = temp[0]
                changeY = temp[1]
                if temp[0] > len(level[0]) or temp[1] > len(level): return [0, 0, 0, 0]
                level[changeX][changeX] = '000'

            try: level[changeY][changeX]
            except: return [0, 0, 0, 0]

            goTo = [[1, 0, "R"], [-1, 0, "L"], [0, 1, "D"], [0, -1, "U"]]
            pref, temp, temp2 = [], [], []
            temp += goTo
            link = ["X"]

            for xy in temp:
                try:
                    if "X" in level[changeY + xy[1]][changeX + xy[0]]:
                        goTo.remove(xy)
                    elif xy[2] not in level[changeY][changeX]:
                        goTo.remove(xy)
                    elif abs(changeX-x) + abs(changeY-y) > abs((xy[0] + changeX)-x) + abs((xy[1] + changeY) - y):
                        pref.append(xy)
                        link += xy[2]
                except: goTo.remove(xy)

            for direction in link:
                alltrue = False
                for xy in goTo:
                    if direction in xy[2]:
                        alltrue = True
                if not alltrue: temp2.append(direction)

            if len(pref) > 0: goTo = random.choice(pref)
            elif len(goTo) > 0:
                goTo = random.choice(goTo)
                if len(temp2) > 0:
                    link = random.choice(temp2)
            else:
                level[changeY][changeX] = ''
                goTo = [0, 0]

            changeX += goTo[0]
            changeY += goTo[1]

            if changeX == x and changeY == y: level[changeY][changeX] = "LRUDhallX_entr"
            else: level[changeY][changeX] = getLinkExc(level, changeY, changeX, ["_", link])
            if "X" in level[changeY][changeX] and "_" not in level[changeY][changeX]: level[changeY][changeX] += "mod-" + sala[-4:]
            count += 1
        return level
    except: pass
def getLinkExc(level, andar, sala, mod):
    link = []
    exception = []
    if "X" not in level[andar][sala]:
        if sala == 0: exception.append("L")
        if sala == len(level[andar]) - 1: exception.append("R")
        if andar == 0: exception.append("U")
        if andar == len(level) - 1: exception.append("D")

        # se a sala anterior linkar à direita
        if sala > 0:
            if "R" in level[andar][sala - 1]: link.append("L")
            elif "X" in level[andar][sala - 1]: exception.append("L")

        # se a próxima sala linkar à esquerda
        if sala < len(level[andar]) - 1:
            if "L" in level[andar][sala + 1]: link.append("R")
            elif "X" in level[andar][sala + 1]: exception.append("R")

        # se a sala acima linkar abaixo
        if andar > 0:
            if "D" in level[andar - 1][sala]:
                link.append("U")
            elif "X" in level[andar - 1][sala]:
                exception.append("U")

        # se a sala baixo linkar acima
        if andar < len(level) - 1:
            if "U" in level[andar + 1][sala]: link.append("D")
            elif "X" in level[andar + 1][sala]: exception.append("D")

        if "_" in mod:
            exception.append("Blank")
            exception.append("room")
            for tolink in mod[1]: link.append(tolink)
        try:
            return searchfor(link, exception, salas)

        except: pass
        return level[andar][sala]

    else: return level[andar][sala]
def searchfor(link, exception, salas):
    accepted = []
    alltrue = True
    for sala in salas:
        for excLetter in exception:
            if excLetter in sala:
                alltrue = False
        for linkLetter in link:
            if linkLetter not in sala:
                alltrue = False
        if alltrue:
            accepted.append(sala)
        alltrue = True

    temp2 = accepted[random.randint(0, len(accepted)-1)]
    accepted = accepted[random.randint(0, len(accepted) - 1)]
    if "hall" not in temp2: accepted = temp2
    return accepted
def fixer(level):
    for andar in range(len(level)):
        for sala in range(len(level[andar])):
            try:
                alltrue = False
                while not alltrue:
                    modC, modL = 0, 0
                    alltrue = True
                    if alltrue:
                        if "L" in level[andar][sala]:
                            if sala > 0:
                                if "R" not in level[andar][sala - 1]:
                                    modC = L
                                    alltrue = False
                    if alltrue:
                        if "R" in level[andar][sala]:
                            if sala < len(level[andar]) - 1:
                                if "L" not in level[andar][sala + 1]:
                                    modC = R
                                    alltrue = False
                    if alltrue:
                        if "U" in level[andar][sala]:
                            if andar > 0:
                                if "D" not in level[andar - 1][sala]:
                                    modL = U
                                    alltrue = False
                    if alltrue:
                        if "D" in level[andar][sala]:
                            if andar < len(level) + 1:
                                if "U" not in level[andar + 1][sala]:
                                    modL = D
                                    alltrue = False
                    if not alltrue:
                        level[andar + modL][sala + modC] = ""
                        level[andar + modL][sala + modC] = getLinkExc(level, andar + modL, sala + modC, " ")
                        if "-" in level[andar][sala]: level[andar + modL][sala + modC] += level[andar][sala[4::]]

            except: pass
    try:
        if "_hall" not in level[keeper[0].at[1]][keeper[0].at[0]] or\
           "strt" not in level[keeper[1].at[1]][keeper[1].at[0]] or \
           "key1" not in level[keeper[2].at[1]][keeper[2].at[0]] or\
           "key2" not in level[keeper[3].at[1]][keeper[3].at[0]] or\
           "end." not in level[keeper[4].at[1]][keeper[4].at[0]]:
            return [0, 0, 0, 0]
        else: return level
    except: return [0, 0, 0, 0]

def strt():
    clearall()
    while True:
        level = []
        x, y = mapSize[0], mapSize[1]
        for temp in range(y):
            level.insert(0, [])
            for temp2 in range(x):
                level[0].append("")

        temp = []
        for sala in open("../Salas/tokeeplist.txt", 'r'):
            if "_" in sala:
                temp.append(sala[:-1])
                times = 1
            if "x" in sala:
                for temp4 in range(times):
                    temp4 = random.choice(temp)
                    at = insert(level, temp4)
                    if len(at) == 4:
                        level = [0, 0, 0, 0]
                        break
                    level[at[1]][at[0]] = temp4

                    if "_hall" not in temp4: level = pathFinder(level, temp4, at[0], at[1])
                    if len(level) == 4: break
                    temp = []
            if len(level) == 4: break
        if len(level) == 4: break

        for andar in range(len(level)):
            for sala in range(len(level[andar])):
                level[andar][sala] = getLinkExc(level, andar, sala, "")


        level = fixer(level)

        #level = fixer(level)
        break
    for i in level: print(i)

    return level
keeper = []
at = []

'''

counter = 0

while True:
    strt()
    counter += 1
    print(counter)
    '''