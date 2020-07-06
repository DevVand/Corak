import pygame
from Corak.dicio import *
import random

class Tile(pygame.sprite.Sprite):
    def __init__(self, type, size, Line, Colum, offsets, sides, len):

        pygame.sprite.Sprite.__init__(self)
        self.type = type

        self.image = pygame.Surface([16, 16])
        temp3 = 1
        if "0" in type:
            self.image = pygame.Surface([16, 16])
            tileset = pygame.image.load("../Sprites/deco.png").convert_alpha()
            self.image.fill(CUSTOM2)
            if "D" not in sides: #grass
                for position in tilemapdeco:
                    if "D" in position[0]:
                        temp = random.choice([1, 1, 1, 9])
                        if temp != 9: self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], 16, 16)), pygame.SRCALPHA
            if "L" not in sides: #wall grass
                temp = random.choice([6])
                if temp != 9: self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], 16, 16)), pygame.SRCALPHA
            if "R" not in sides: #wall grass
                temp = random.choice([7])
                if temp != 9: self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], 16, 16)), pygame.SRCALPHA
            if "U" not in sides: #ceiling grass
                for position in tilemapdeco:
                    if "U" in position[0]:
                        temp = random.choice([1, 9])
                        if temp != 9: self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], 16, 16)), pygame.SRCALPHA

            if "U" not in sides and "D" in sides:
                temp = random.choice([4, 5, 9, 9, 9])
                if temp != 9:
                    temp3 = 2
                    temp2 = self.image
                    self.image = pygame.Surface([16, 32])
                    self.image.blit(temp2, (0, 0)), pygame.SRCALPHA
                    self.image.blit(tileset, (0, 0), (tilemapdeco[temp][1][1], tilemapdeco[temp][1][0], 16, 32)), pygame.SRCALPHA
            self.image = pygame.transform.scale(self.image, ([size, size*temp3]))
            print("scaled to", size, size*temp3, temp3 )
        if "1" in type:
            for position in tilemap:
                if sides == position[0]:
                    tileset = pygame.image.load("../Sprites/tileset.png").convert_alpha()
                    self.image = pygame.Surface([16, 16])
                    self.image.fill(KEY)
                    self.image.set_colorkey(KEY)
                    self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], 16, 16)), pygame.SRCALPHA
        elif "2" in type:
            for position in tilemap:
                if sides[0] == position[0]:
                    tileset = pygame.image.load("../Sprites/tileset.png").convert_alpha()
                    self.image.blit(tileset, (0, 0), (position[1][1], position[1][0], 16, 16)), pygame.SRCALPHA
        elif "3" in type: self.image.fill(YELLOW)
        elif "4" in type: self.image.fill(RED)
        elif ("L" or "R" or "U" or "D" or "S") in type: self.image.fill(CUSTOM2)
        self.image = pygame.transform.scale(self.image, ([size, size*temp3]))


        self.at = [Colum, Line]
        self.rect = self.image.get_rect()
        self.rect.x = size * Colum + offsets[0]
        self.rect.y = size * Line + offsets[1]

        if "9" in type:
            self.image = pygame.Surface((len[0]*size, len[1]*size))

            self.image.fill(YELLOW)
            self.rect = self.image.get_rect()
            self.rect.x = size * 0 + offsets[0]
            self.rect.y = size * 0 + offsets[1]

def mapread (sala):
    tiles = pygame.sprite.Group()
    tiles_deco = pygame.sprite.Group()
    tiles_breakable = pygame.sprite.Group()

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
            if sala[Line][Colum] == "2": sides = "Breakable"

            tile = Tile(sala[Line][Colum], size, Line, Colum, offsets, sides, (len(sala[0]), len(sala)))
            if "0" in sala[Line][Colum]: tiles_deco.add(tile)
            elif "1" in sala[Line][Colum]: tiles.add(tile)
            elif "2" in sala[Line][Colum]: tiles_breakable.add(tile)
        #print(tiles, ".", tiles.has_internal(tile.at[0]))
    for sprite in tiles:
        if sprite.at[0] == 1 and sprite.at[1] == 2: print(sprite, sprite.at)
    #print(len(sala), "x", len(sala[0]))


    print("lines in list:", len(sala))
    print("colums in list:", len(sala[0]))
    '''
    print("list:", sala)
    print(temp)
    print("size:", size)
    '''
    background_colour = Tile("9", size, 0, 0, offsets, 0, (len(sala[0]), len(sala)))
    return tiles, tiles_breakable, tiles_deco, background_colour