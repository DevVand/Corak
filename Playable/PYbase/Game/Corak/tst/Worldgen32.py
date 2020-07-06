import random
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
    Lmod, Rmod, Umod, Dmod = 0, 0, 0, 0
    print(sala)
    if "L" in sala: Lmod = 1
    if "R" in sala: Rmod = 1
    if "U" in sala: Umod = 1
    if "D" in sala: Dmod = 1
    if "_hall" in sala:
        Umod, Dmod, Rmod, Lmod = 6, 6, 4, 4
    while True:
        y = random.randint(0 + Umod, len(level) - 1 - Dmod)
        x = random.randint(0 + Lmod, len(level[0]) - 1 - Rmod)
        if "_hall" not in sala:
            if "_key1" in sala:
                excDistance = 6
                maxDistance = 10
                if x <= keeper[0].at[0] or y - 2 <= keeper[0].at[1]: excDistance = 100
            elif "_key2" in sala:
                excDistance = 4
                maxDistance = 10
                if x + 3 >= keeper[0].at[0] or y + 3 >= keeper[0].at[1]: excDistance = 100
            elif "_strt" in sala:
                excDistance = 5
                maxDistance = 10
                if y >= keeper[0].at[1] or x - keeper[0].at[0] not in range(-1, 1): excDistance = 100
            count = 0
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
                if finalcount < maxDistance: break
        else: break

    print(sala, x, y, "\n \n")
    level[y][x] = sala
    keep(sala, [x, y])
  #  level = pathfinder(level, at[x, y])
    print(sala,"\n \n")
    return level

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

    #print("accepted list:\n", accepted)
    return accepted[random.randint(0, len(accepted)-1)]

salas = []
for sala in open("../../Salas/maplist.txt", 'r'): salas.append(sala[:-1])

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

print("\nstep4: main inputs ")
temp = []
keeper = []
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

            temp.remove(special)
            level = insert(level, special)
        temp = []
for andar in level:
    print(andar)

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

            level[andar][sala] = searchfor(link, exception, salas)
            #print(">sala", sala + 1, "andar", andar + 1, ":", level[andar][sala])

            exception = []
            link = []

print("\nstep5: map finished ")
print(len(level[0]), "x", len(level))
for andar in level:
    print(andar)
for sala in range(len(keeper)):
    print(keeper[sala].sala, "at", keeper[sala].at)
