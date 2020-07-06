mode30 = False
mode500 = False
#phisycs = False
mode = True

ScreenX = 272
ScreenY = 272
ScreenXY = [ScreenX, ScreenY]

middlex, middley, = ScreenX/2, ScreenY/2
middle = [middlex, middley]

upscale = 3

FScreenX = ScreenX * upscale
FScreenY = ScreenY * upscale
FScreenXY = [FScreenX, FScreenY]

Fmiddlex, Fmiddley, = FScreenX/2, FScreenY/2
Fmiddle = [Fmiddlex, Fmiddley]

mapSizeX, mapSizeY = 16, 16
mapSize = [mapSizeX, mapSizeY]


FPS = 60
if mode30:
    FPS = 30
if mode500:
    FPS = 1000


U = L = -1
D = R = 1

'colours'
CLEAR = (0, 0, 0, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CUSTOM = (102, 101, 111)
CUSTOM2 = (50, 0, 25)
#KEY = (1, 255, 1)
#KEY = (184, 103, 95)

KEY = (255, 255, 254)
CRED = (184, 103, 95)

i = 16
tilemap = [["LU", [0, 0]],
           ["RU", [0, i*2]],
           ["LD", [i*2, 0]],
           ["RD", [i*2, i*2]],
           ["L", [i, 0]],
           ["R", [i, i*2]],
           ["U", [0, i]],
           ["D", [i*2, i]],
           ["LR", [i, i*3]],
           ["UD", [0, i*5]],
           ["LRU", [0, i*3]],
           ["LRD", [i*2, i*3]],
           ["LUD", [0, i*4]],
           ["RUD", [0, i*6]],
           ["LRUD", [i, i]],
           ["Breakable", [i, i*4]],
           ]
tilemapdeco = [["U deco", [0, i]],       #0 chain 1
               ["U deco", [0, 0]],       #1 chain 2
               ["U2 deco",[0, i*2]],        #2
               ["U2 deco",[0, i*3]],        #3
               ["X",      [i, 0]],      #4
               ["D deco", [i*2, i]],    #5
               ["LR deco",[i*2, 0]],    #6
               ["U2 grass",[i*3, 0]],       #7 grass 1
               ["U2 grass",[i*3, i]],       #8 grass 2
               ["L grass", [i*5, 0]],    #9 grass
               ["R grass", [i*5, i]],    #10 grass
               ["U grass", [i*5, i*2]],  #11 grass
               ["D grass", [i*5, i*3]],  #12 grass
               ]

'''
if phisycs:
    max_speed = 5
    acceleration = .2
    friction = 1.2
    gravity = 5

    if mode30:
        max_speed *= 2
        acceleration *= 2
        gravity *= 2
'''


salas = []
for sala in open("../Salas/maplist.txt", 'r'): salas.append(sala[:-1])

def way(direction):
    def Xdir(direction):
        at = 0
        for letter in direction:
            if "L" in letter: at += -1
            if "R" in letter: at += 1
            print(at)
        return at
    def Ydir(direction):
        at = 0
        for letter in direction:
            if "U" in letter: at += -1
            if "D" in letter: at += 1
            print(at)
        return at

    if (("U" or "D") and ("R" or "L")) in direction:
        return [Xdir(direction)][Ydir(direction)]
    elif ("L" or "R") in direction:
        return Xdir(direction)
    elif ("U" or "D") in direction:
        return Ydir(direction)
def getSize(sala):
    '''
    if ScreenX >= ScreenY:
        if len(sala[0]) > len(sala):
            size = int(ScreenX / len(sala[0]))
        else:
            size = int(ScreenY / len(sala))
    else:
        if len(sala) > len(sala[0]):
            size = int(ScreenY / len(sala))
        else:
            size = int(ScreenX / len(sala[0]))
            '''
    return 16
def getOffset(obj, size, type):
    if "sala" in type:
        offsetX = int((ScreenX / 2) - ((len(obj[0]) * size) / 2))
        offsetY = int((ScreenY / 2) - ((len(obj) * size) / 2))

        #offsetX = 0
        #offsetY = 0
        offsets = [offsetX, offsetY]
    else:
        offsetX = obj[0] / 2
        offsetY = obj[1] / 2
        offsets = [offsetX, offsetY]
    return offsets
def openSala(salaTXT):
    sala = []
    temp2 = "normal"
    read = False
    if "_" in salaTXT:
        temp2 = salaTXT[-5:]
        salaTXT = salaTXT[:-5]
    if "mod" in salaTXT:
        temp2 = salaTXT[-8:]
        salaTXT = salaTXT[:-8]
    salaTXT += ".txt"

    temp = open(salaTXT, 'r')
    while True:
        tiles = temp.readline()
        if read:
            if "X" in tiles:
                temp.close

                print(sala)
                for i in range(len(sala)):
                    sala[i] = sala[i].replace(" ", "")

                    sala[i] = sala[i].replace(".", "0")
                    print(i)
                return sala
            sala.append(tiles[:-1])
        if temp2 in tiles:
            read = True
