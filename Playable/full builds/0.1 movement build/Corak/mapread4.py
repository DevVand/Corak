import pygame
from Corak.dicio import *
class Tile(pygame.sprite.Sprite):
    def __init__(self, type, size, Line, Colum, offsets ):
        pygame.sprite.Sprite.__init__(self)
        self.type = 0
        self.image = pygame.Surface([size, size])
        if "0" in type:
            self.image.fill(WHITE)
        elif "1" in type:
            self.type = 1
            self.image.fill(BLACK)
        elif "2" in type:
            self.type = 2
            self.image.fill(GREEN)
        elif "3" in type:
            self.image.fill(YELLOW)
        elif "4" in type:
            self.image.fill(RED)
        self.at = [Colum, Line]

        self.rect = self.image.get_rect()
        self.rect.x = size * Colum + offsets[0]
        self.rect.y = size * Line + offsets[1]



def mapread (sala):
    tiles = pygame.sprite.Group()

    print("lines in list:", len(sala))
    print("colums in list:", len(sala[0]))
    print("list:", sala)

    temp = ""
    for Line in sala:
        for Colum in Line:
            temp += Colum
            temp += "  "
        temp += "\n"

    print(temp)

    size = getSize(sala)

    print("size:", size)

    offsets = getOffset(sala, size)

    for Line in range(len(sala)):
        for Colum in range(len(sala[0])):
            tile = Tile(sala[Line][Colum], size, Line, Colum, offsets)
            tiles.add(tile)
            print(tile.at[0])
        print(tiles, ".", tiles.has_internal(tile.at[0]))
    for sprite in tiles:
        if sprite.at[0] == 1 and sprite.at[1] == 2: print(sprite, sprite.at)
    print(len(sala), "x", len(sala[0]))
    return tiles