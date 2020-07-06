import pygame as pg
from Corak.dicio import *
import random

class Tile(pg.sprite.Sprite):
    def __init__(self, type, size, Line, Colum, offsets, sides, len):

        pg.sprite.Sprite.__init__(self)
        self.type = type

        self.image = pg.Surface([size, size])
        temp3 = 1
        if "0" in type:
            self.image = pg.Surface([size, size], pg.SRCALPHA)
            tileset = pg.image.load("../Sprites/deco.png").convert_alpha()

            if "U" not in sides and "LRD" in sides:
                temp = random.choice([2, 3, 9, 9, 9])
                if temp != 9:
                    temp3 = 2
                    temp2 = self.image
                    self.image = pg.Surface([size, size*2], pg.SRCALPHA)
                    self.image.blit(temp2, (0, 0))
                    self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], size, size*2))
            if "D" not in sides: #grass
                for position in tilemapdeco:
                    if "D" in position[0]:
                        temp = random.choice([1, 1, 1, 1])
                        if temp != 9: self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
            if "L" not in sides: #wall grass
                temp = random.choice([6])
                if temp != 9: self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], size, size))
            if "R" not in sides: #wall grass
                temp = random.choice([7])
                if temp != 9: self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], size, size))

            if "U" not in sides: #wall grass
                temp = random.choice([8, 8, 8, 8])
                if temp != 9: self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], size, size))

            if "U" not in sides: #wall grass
                temp = random.choice([0, 1, 9, 9])
                if temp != 9: self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], size, size))
            if "U" not in sides and "D" in sides: #grass
                temp = random.choice([4, 5, 9, 9, 9])
                if temp != 9:
                    temp3 = 2
                    temp2 = self.image
                    self.image = pg.Surface([size, size*2], pg.SRCALPHA)
                    self.image.blit(temp2, (0, 0))
                    self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], size, size*2))


            self.image = pg.transform.scale(self.image, ([size, size*temp3]))
        if "1" in type:
            tileset = pg.image.load("../Sprites/tileset.png").convert_alpha()
            for position in tilemap:
                if sides == position[0]:
                    self.image = pg.Surface([size, size])
                    self.image.fill(KEY)
                    self.image.set_colorkey(KEY)
                    self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
        elif "2" in type:
            tileset = pg.image.load("../Sprites/tileset.png").convert_alpha()
            for position in tilemap:
                if sides[0] == position[0]:
                    self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
        elif "3" in type: self.image.fill(YELLOW)
        elif "4" in type: self.image.fill(RED)
        elif ("L" or "R" or "U" or "D" or "S") in type: self.image.fill(CUSTOM2)
        self.image = pg.transform.scale(self.image, ([size, size*temp3]))

        self.at = [Colum, Line]
        self.rect = self.image.get_rect()
        self.rect.x = size * Colum
        self.rect.y = size * Line
        if "2" in type:
            self.rect.x += offsets[0]
            self.rect.y += offsets[1]
        if "9" in type:
            self.image = pg.Surface((len[0]*size, len[1]*size))
            self.rect = self.image.get_rect()
            self.rect.x = size * 0 + offsets[0]
            self.rect.y = size * 0 + offsets[1]

        if "8" in type:
            self.image = pg.Surface([size, size])
            self.image.fill(CUSTOM2)
            self.rect = self.image.get_rect()
            self.rect.x = size * Colum
            self.rect.y = size * Line

def mapread (sala):
    tiles_base_group = pg.sprite.Group()
    tiles_deco_group = pg.sprite.Group()
    tiles_breakable = pg.sprite.Group()
    background2 = pg.sprite.Group()

    temp = ""
    for Line in sala:
        for Colum in Line:
            temp += Colum
            temp += "  "
        temp += "\n"

    size = getSize(sala)
    offsets = getOffset(sala, size, "sala")
    print(sala)
    for Line in range(len(sala)):
        for Colum in range(len(sala[0])):
            sides = ""
            try:
                if sala[Line][Colum + L] != "1": sides += "L"
            except: pass
            try:
                if sala[Line][Colum + R] != "1": sides += "R"
            except: pass
            try:
                if Line > 0:
                    if sala[Line + U][Colum] != "1": sides += "U"
            except:pass
            try:
                if Colum > 0:
                    if sala[Line + D][Colum] != "1": sides += "D"
            except: pass
            #if sala[Line][Colum] == "2": sides = "Breakable"
            #if len(sides) < 1: sides = "X"

            tile = Tile(sala[Line][Colum], size, Line, Colum, offsets, sides, (len(sala[0]), len(sala)))
            if "0" in sala[Line][Colum]:

                temp = Tile("8", size, Line, Colum, offsets, sides, (len(sala[0]), len(sala)))
                tiles_base_group.add(temp)
                tiles_deco_group.add(tile)
            elif "1" in sala[Line][Colum]:
                tiles_base_group.add(tile)
            elif "2" in sala[Line][Colum]:

                temp = Tile("8", size, Line, Colum, offsets, sides, (len(sala[0]), len(sala)))
                tiles_base_group.add(temp)
                tiles_breakable.add(tile)
        #print(tiles, ".", tiles.has_internal(tile.at[0]))
    #print(len(sala), "x", len(sala[0]))

    tiles_deco = Tile("9", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))
    tiles_base = Tile("9", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))
    tiles_deco.image.fill(KEY)
    tiles_deco.image.set_colorkey(KEY)
    tiles_base.image.fill(KEY)
    tiles_base.image.set_colorkey(KEY)

    for i in tiles_base_group: tiles_base.image.blit(i.image, i.rect)
    for i in tiles_deco_group: tiles_deco.image.blit(i.image, i.rect)


    print("lines in list:", len(sala))
    print("colums in list:", len(sala[0]))
    '''
    print("list:", sala)
    print(temp)
    print("size:", size)
    '''
    background_colour = Tile("9", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))
    return tiles_breakable, background_colour, tiles_deco, tiles_base