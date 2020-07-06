mode30 = False
phisycs = False

ScreenX = 500
ScreenY = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (150, 150, 150)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

FPS = 60

if phisycs:
    max_speed = 5
    acceleration = .2
    friction = 1.2

    gravity = 5

    if mode30:
        if phisycs:
            max_speed *= 2
            acceleration *= 2

            gravity *= 2

if mode30:
    FPS = 30

def getSize (sala):
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
    return size

def getOffset (sala, size):
    offsetX = int((ScreenX / 2) - ((len(sala[0]) * size) / 2))
    offsetY = int((ScreenY / 2) - ((len(sala) * size) / 2))
    offsets = [offsetX, offsetY]
    return offsets

def openSala (salaTXT):
    sala = []

    temp = open(salaTXT, 'r')
    while True:
        tiles = temp.readline()
        if "X" in tiles:
            break
        sala.append(tiles[:-1])
    temp.close
    return sala
