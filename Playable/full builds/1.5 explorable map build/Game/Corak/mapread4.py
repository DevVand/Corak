import pygame as pg
from Game.Corak.dicio import *
import random

class Tile(pg.sprite.Sprite):
    def __init__(self, type, size, Line, Colum, offsets, sides, len):

        pg.sprite.Sprite.__init__(self)
        self.type = type
        self.image = pg.Surface([size, size])
        temp3 = 1
        if "0" in type:
            self.image = pg.Surface([size, size], pg.SRCALPHA)
            tileset = pg.image.load("../Sprites/tilesets/deco.png").convert_alpha()
            if "LR" in sides: # deco
                for position in tilemapdeco:
                    if "LR d" in position[0]:
                        temp = random.choice([1, 9])
                        if temp != 9:
                            self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
                            temp = random.choice([1, 9])
                            if temp != 9:
                                self.image = pg.transform.flip(self.image, True, False)
            if "D" in sides: # deco
                for position in tilemapdeco:
                    if "D d" in position[0]:
                        temp = random.choice([1, 9, 9, 9])
                        if temp != 9:
                            self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
                            temp = random.choice([1, 9])
                            if temp != 9:
                                self.image = pg.transform.flip(self.image, True, False)
            if "U" in sides: # deco
                for position in tilemapdeco:
                    if "U d" in position[0]:
                        temp = random.choice([1, 9, 9, 9])
                        if temp != 9:
                            self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
                            temp = random.choice([1, 9])
                            if temp != 9:
                                self.image = pg.transform.flip(self.image, True, False)
                        break
            if "U" in sides and all(i not in sides for i in "LRD"): # deco
                for position in tilemapdeco:
                    if "U2 d" in position[0]:
                        temp = random.choice([3, 9, 9, 9])
                        if temp != 9:
                            temp3 = 2
                            temp2 = self.image
                            self.image = pg.Surface([size, size*2], pg.SRCALPHA)
                            self.image.blit(temp2, (0, 0))
                            self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size*2))
                            temp = random.choice([1, 9])
                            if temp != 9:
                                self.image = pg.transform.flip(self.image, True, False)
            if "U" in sides and "D" not in sides: # deco
                for position in tilemapdeco:
                    if "U2 g" in position[0]:
                        temp = random.choice([4, 5, 9, 9, 9])
                        if temp != 9:
                            temp3 = 2
                            temp2 = self.image
                            self.image = pg.Surface([size, size*2], pg.SRCALPHA)
                            self.image.blit(temp2, (0, 0))
                            self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size*2))
                            temp = random.choice([1, 9])
                            if temp != 9:
                                self.image = pg.transform.flip(self.image, True, False)


            if "D" in sides: # grass
                for position in tilemapdeco:
                    if "D g" in position[0]:
                        self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
            if "U" in sides: # grass
                for position in tilemapdeco:
                    if "U g" in position[0]:
                        self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
            if "L" in sides: # grass
                for position in tilemapdeco:
                    if "L g" in position[0]:
                        self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
            if "R" in sides: # grass
                for position in tilemapdeco:
                    if "R g" in position[0]:
                        self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))

            self.image = pg.transform.scale(self.image, ([size, size*temp3]))
        if "1" in type:
            tileset = pg.image.load("../Sprites/tilesets/tileset.png").convert_alpha()
            for position in tilemap:
                if sides == position[0]:
                    self.image = pg.Surface([size, size], pg.SRCALPHA)
                    self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
        elif "2" in type:
            tileset = pg.image.load("../Sprites/tilesets/tileset.png").convert_alpha()
            for position in tilemap:
                if "Breakable" in position[0]:
                    self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], size, size))
        elif "3" in type: self.image.fill(YELLOW)
        elif "4" in type: self.image.fill(KEY)

        self.image = pg.transform.scale(self.image, ([size, size*temp3]))
        self.at = [Colum, Line]
        self.rect = self.image.get_rect()
        self.rect.x = size * Colum
        self.rect.y = size * Line
        if "2" in type:
            self.rect.x += offsets[0]
            self.rect.y += offsets[1]
        if "8" in type:
            self.image = pg.Surface([size, size], pg.SRCALPHA)
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = size * Colum
            self.rect.y = size * Line
        if "9" in type:
            if "99" in type:
                self.image = pg.Surface((len[0]*size, len[1]*size))
            else: self.image = pg.Surface((len[0] * size, len[1] * size), pg.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.x = size * 0 + offsets[0]
            self.rect.y = size * 0 + offsets[1]

def generatenew (size, offsets, tiles_base):
    temp = Tile("9", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))

    return temp

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
    for Line in range(len(sala)):
        for Colum in range(len(sala[0])):
            sides = ""
            if "1" in sala[Line][Colum]:
                try: # L
                    if Colum > 0:
                        if sala[Line][Colum + L] not in "1T": sides += "L"
                except: pass
                try: # R
                    if len(sala[0]) > Colum + R:
                        if sala[Line][Colum + R] not in "1T": sides += "R"
                except: pass
                try: # U
                    if Line > 0:
                        if sala[Line + U][Colum] not in "1T": sides += "U"
                except: pass
                try: # D
                    if len(sala) > Line + D:
                        if sala[Line + D][Colum] not in "1T": sides += "D"
                except: pass
            elif "0" in sala[Line][Colum]:
                try: # L
                    if Colum > 0:
                        if sala[Line][Colum + L] == "1": sides += "L"
                except: pass
                try: # R
                    if len(sala[0]) > Colum + R:
                        if sala[Line][Colum + R] == "1": sides += "R"
                except: pass
                try: # U
                    if Line > 0:
                        if sala[Line + U][Colum] == "1": sides += "U"
                except: pass
                try: # D
                    if len(sala) > Line + D:
                        if sala[Line + D][Colum] == "1": sides += "D"
                except: pass
            else:
                try: # L
                    if Colum > 0:
                        if sala[Line][Colum + L] != "1": sides += "L"
                except: pass
                try: # R
                    if len(sala[0]) > Colum + R:
                        if sala[Line][Colum + R] != "1": sides += "R"
                except: pass
                try: # U
                    if Line > 0:
                        if sala[Line + U][Colum] != "1": sides += "U"
                except: pass
                try: # D
                    if len(sala) > Line + D:
                        if sala[Line + D][Colum] != "1": sides += "D"
                except: pass
            tile = Tile(sala[Line][Colum], size, Line, Colum, offsets, sides, (len(sala[0]), len(sala)))
            if "0" in sala[Line][Colum]:
                tiles_deco_group.add(tile)
            elif "1" in sala[Line][Colum]:
                tiles_base_group.add(tile)
            elif "2" in sala[Line][Colum]:
                tiles_breakable.add(tile)

        #print(tiles, ".", tiles.has_internal(tile.at[0]))
    #print(len(sala), "x", len(sala[0]))
    tiles_base = Tile("9", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))
    tiles_draw = Tile("99", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))

    for i in tiles_base_group: tiles_base.image.blit(i.image, i.rect)
    for i in tiles_deco_group: tiles_base.image.blit(i.image, i.rect)

    print("lines in list:", len(sala))
    print("colums in list:", len(sala[0]))
    '''
    print("list:", sala)
    print(temp)
    print("size:", size)
    '''
    background_colour = Tile("9", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))
    return tiles_breakable, background_colour, tiles_draw, tiles_base