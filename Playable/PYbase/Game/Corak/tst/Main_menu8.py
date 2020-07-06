from Game.Corak.mapread4 import *
from Game.Corak.dicio import *
from Game.Corak.Worldgen3 import hall
print()
'classes'
class Corak(pygame.sprite.Sprite):
    def __init__(S):
        S.image = pygame.Surface([size, size])
        S.image.fill(BLACK)
        S.rect = S.image.get_rect()
        S.at = [0, 11]
        S.pos = [size * S.at[0] + offsets[0], size * S.at[1] + offsets[1]]
        S.Do = []
        S.turn = True
        S.jump = False
        S.air = False
        S.focus = False
        S.grab = False
        S.actualmap = hall([0, 0, "get pos"])
        S.sala = sala

    def CheckLevel(S, at):
        if -1 >= at[0]:
            print("levelleft")
            maphall([-1, ])
        elif len(S.sala[0]) == at[0]:
            print("levelright")
        elif -1 >= at[1]:
            print("levelup")
        elif len(S.sala) == at[1]:
            print("leveldown")
        else: S.checkMap(at)
    def checkMap(S, at):
        S.cantGo = []
        if S.focus: distance = 2
        else: distance = 1
        for i in range(1, distance+1):
            try:
                if S.sala[at[1]][at[0] + i] in "12":
                    S.cantGo.extend(["R", i * "R"])
            except: pass
            try:
                if at[0] - 1 >= 0:
                    if S.sala[at[1]][at[0] - i] in "12":
                        S.cantGo.extend(["L", i * "L"])
            except:
                pass
            try:
                if S.sala[at[1] + 1][at[0]] in "123":
                    S.cantGo.append("D")
            except: pass
            try:
                if at[1] - 1 >= 0:
                    if S.sala[at[1] - i][at[0]] in "123":
                        S.cantGo.extend(["U", i * "U"])
            except: pass
        S.update([0, 0, "Move"])
    def checkMove(S):
        S.air = True
        if "D" in S.cantGo:
            S.air = False

        if S.turn:
            if S.air and not S.grab:
                S.cantGo.append("U")

        if not S.turn:
            if not any([S.jump, S.grab]) and S.air:
                S.Do = [0, 1, "D"]
                S.jump = True
                S.Move(S.Do)

            if S.jump:
                S.jump = False

            S.turn = True
            S.update([0, 0, "Move"])
    def Move(S, Do):
        alltrue = True
        for direction in S.cantGo:
            if direction in Do[2]:
                alltrue = False
                if S.air and direction in "LR": S.grab = True, print("grab")
                if S.focus and direction in "LRU":
                    S.focus = False
                    alltrue = True

        if alltrue:
            if Do[1] == -1: S.jump = True, print("jump")
            if S.focus : Do[0] *= 2
            if S.focus : Do[1] *= 2
            S.focus = False
            S.grab = False

            S.at[0] = S.at[0] + Do[0]
            S.at[1] = S.at[1] + Do[1]
            S.pos[0] = size * S.at[0] + offsets[0]
            S.pos[1] = size * S.at[1] + offsets[1]
        S.turn = False
        S.CheckLevel(S.at)
    def Focus(S):
        if S.grab: S.grab = False
        if not (S.focus or S.air):
            S.focus = True
        S.turn = False
        S.checkMap(S.at)
    def Hit(S, direction, at):
        try:
            if str(S.sala[at[1]][at[0] + direction]) in "2":
                S.sala[at[1]] = S.sala[at[1]][:at[0]+direction:] + "0" + S.sala[at[1]][-(len(S.sala[at[1]])-1 - (direction + at[0]))::]
                for tile in tile_breakable:
                    if tile.at == [at[0] + direction, at[1]]:
                        tile_breakable.remove(tile)
                if S.focus:
                    S.focus = False
                if S.grab: S.grab = False
        except:
            pass
        print("hit")
        S.turn = False
        S.update([0, 0, "Map"])
    def update(S, Do):
        if Do[2] in "LRUD": S.Move(Do)
        if Do[2] in "H": S.Hit(Do[0], S.at)
        if Do[2] in "X": S.Focus()
        if Do[2] in "Move": S.checkMove()
        if Do[2] in "Map": S.checkMap(S.at)

class Spriter(pg.sprite.Sprite):
    def __init__(s, type, size, frames):
        pg.sprite.Sprite.__init__(s)
        s.frames = frames
        s.frame = 0
        s.Fullimage = pg.image.load(type)
        s.rx, s.ry = s.Fullimage.get_size()
        #s.Fullimage = pg.transform.scale2x(s.Fullimage)
        s.Fullimage = pg.transform.scale(s.Fullimage, (s.rx * upscale, s.ry * upscale))
        s.Fullimage_region = (s.ry* 1, 0, s.ry*1, s.rx)

        s.rx, s.ry = s.Fullimage.get_size()

        s.image = pg.Surface((s.rx / s.frames, s.ry), pg.SRCALPHA)
        s.image.blit(s.Fullimage, (0, 0), ((s.frame) * s.rx/s.frames, 0, s.rx, s.ry))

        s.rect = s.image.get_rect(center=(middle))

        #screen.blit(Fullimage, (0, 0), area=Fullimage_region)
    def setFrame(s, to):
        s.frame = to
        if s.frame >= s.frames: s.frame = 0
        s.image.fill(CLEAR)
        s.image.blit(s.Fullimage, (0, 0), ((s.frame) * s.rx/s.frames, 0, s.rx, s.ry))
    def update(s, pos):
        s.rect.x = pos[0]
        s.rect.y = pos[1]

class Surfaces(pg.sprite.Sprite):
    def __init__(s, type, colour, size, at):
        pg.sprite.Sprite.__init__(s)

        s.image = pg.Surface(size)
        s.image.fill(colour)
        s.rect = s.image.get_rect()
        s.rect.x = at[0]
        s.rect.y = at[1]
        Surfaces.Do(s, type)
    def Do(s, type):
        if "fade" in type:
            s.image.set_alpha(0)

class mapTile(pg.sprite.Sprite):
    def __init__(self, name, size, andar1, sala1):
        pg.sprite.Sprite.__init__(self)
        self.type = 0
        self.image = pg.Surface([size, size])
        self.image.fill(BLACK)
        self.at = [sala1, andar1]
        self.rect = self.image.get_rect()
        self.rect.x = self.at[0]
        self.rect.y = self.at[1]
        alltiles.append(self)
        'draw'
        if "room" in name: self.image.fill(BLUE)
        if "_hall" in name: self.image.fill(RED)
        if "_strt" in name: self.image.fill(YELLOW)
        if "_key" in name: self.image.fill(RED)
        if "mod" in name: self.image.fill(GRAY)
        if "_enter" in name: self.image.fill(GREEN)
        if "_end" in name: self.image.fill(YELLOW)
        if "-strt" in name: self.image.fill([GRAY[0] + 50, GRAY[1], GRAY[2]])
        if "-key1" in name: self.image.fill([GRAY[0] + 100, GRAY[1], GRAY[2]])
        if "-key2" in name: self.image.fill([GRAY[0] + 100, GRAY[1], GRAY[2] + 50])
        if "-end" in name: self.image.fill([GRAY[0] + 100, GRAY[1] - 50, GRAY[2] + 100])

class Tile(pygame.sprite.Sprite):
    def __init__(self, type, size, Line, Colum, offsets):
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
        elif ("L" or "R" or "U" or "D") in type:
            if "0" in type:
                self.image.fill(WHITE)
        self.at = [Colum, Line]

        self.rect = self.image.get_rect()
        self.rect.x = size * Colum + offsets[0]
        self.rect.y = size * Line + offsets[1]

def strt_menu():
    'variable init'
    fade = 0
    click = False
    temp = 255
    temp2 = 1
    clickset = 0

    while True:
        ''
        clock.tick(FPS)
        if clickset == 1: clickset = 0
        pointer.update(pg.mouse.get_pos())
        pg.display.set_caption(str(round(clock.get_fps())))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                elif event.button == 3:
                    print(1)
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
                    clickset = 1

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    pg.quit()
                if event.key == pg.K_b:
                    Spriter.Frame(menu_strt, 1)
        for button in menu:
            if pg.sprite.collide_rect(pointer, button):
                if click:
                    button.setFrame(2)
                    fade = True
                elif clickset == 1:
                    clickset = 2
                    fade = True
                else:
                    button.setFrame(1)
            else:
                button.setFrame(0)
        'draw'
        screen.fill(CUSTOM)
        menu.draw(screen)
        screen.blit(pointer.Fullimage, pointer.rect)
        screeneffects.draw(screen)
        if not fade:
            if temp >= 0:
                temp -= 4
                fader.image.set_alpha(temp)
        if fade:
            if clickset == 2:
                temp += 10
                if temp >= 255:
                    clickset = 0
            else:
                if temp >= 50:
                    fade = False
                else:
                    temp += 8

            fader.image.set_alpha(temp)
        if temp >= 200 and clickset == 2:
            worldgen()
        pg.display.update()

def worldgen():
    def view(actual):
        level = hall([0, 0, "strt"])
        if len(level) == 4:
            return actual

        hall([0, 0, "clear"])
        mapview = pg.sprite.Group()
        while len(alltiles) > 0: del alltiles[0]

        'draw'
        for andar in range(len(level)):
            for sala in range(len(level[andar])):
                if "UDcorridor" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27)]
                        mapview.add(tile)
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27 + (9 * 2))]
                        mapview.add(tile)
                if "LRcorridor" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * temp))]
                        mapview.add(tile)
                if "LDturn" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + 9, sala * 27 + (9 * 2))
                    mapview.add(tile)
                    tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27),
                            mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * 2))]
                    mapview.add(tile)
                if "RDturn" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + 9, sala * 27)
                    mapview.add(tile)
                    tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27),
                            mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * 2))]
                    mapview.add(tile)
                if "RUturn" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27)]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * 2))
                    mapview.add(tile)
                    for temp in range(1, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * temp))]
                        mapview.add(tile)
                if "LUturn" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27 + (9 * 2))]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27)
                    mapview.add(tile)
                    for temp in range(0, 2):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * temp))]
                        mapview.add(tile)
                if "Uroom" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27 + (9 * 2))]
                        mapview.add(tile)
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27)]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + 9)
                    mapview.add(tile)
                if "Droom" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27 + (9 * 2))]
                        mapview.add(tile)
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27)]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27 + 9)
                    mapview.add(tile)
                if "Rroom" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + 9, sala * 27)
                    mapview.add(tile)
                if "Lroom" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + 9, sala * 27 + (9 * 2))
                    mapview.add(tile)
                if "hall" in level[andar][sala]:
                    tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27)
                    mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * 2))
                    mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27)
                    mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * 2))
                    mapview.add(tile)
                if "LUD3" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27 + (9 * 2))]
                        mapview.add(tile)
                        tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27)
                        mapview.add(tile)
                        tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27)
                        mapview.add(tile)
                if "RUD3" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp), sala * 27)]
                        mapview.add(tile)
                        tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * 2))
                        mapview.add(tile)
                        tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * 2))
                        mapview.add(tile)
                if "LRD3" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27)
                    mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * 2))
                    mapview.add(tile)
                if "LRU3" in level[andar][sala]:
                    for temp in range(0, 3):
                        tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * temp))]
                        mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27 + (9 * 2))
                    mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27 + (9 * 2), sala * 27 + (9 * 2))
                    mapview.add(tile)
                    tile = mapTile(level[andar][sala], 9, andar * 27, sala * 27)
                    mapview.add(tile)
                if "Blank" in level[andar][sala]:
                    for temp in range(0, 3):
                        for temp2 in range(0, 3):
                            tile = [mapTile(level[andar][sala], 9, andar * 27 + (9 * temp2), sala * 27 + (9 * temp))]
                            mapview.add(tile)

        return mapview
    def init():
        fade = True
        mapgen = True
        temp = 255
        tiles = pg.sprite.Group()
        clickset = 0
        while True:
            ''
            clock.tick(FPS)
            pointer.update(pg.mouse.get_pos())
            pg.display.set_caption(str(round(clock.get_fps())))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        tiles = view(tiles)
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        fade = False
                        clickset = 1
            ''
            if fade:
              temp -= 2

            if mapgen:
                tiles = view(tiles)

            fader.image.set_alpha(temp)
            if temp <= 0:
                mapgen = False
                if temp <= -60:
                    fade = False

            if not fade or clickset == 1:
                temp += 2
                if temp >= 255:
                  strt_mapread()

            'draw'
            screen.fill(WHITE)
            tiles.draw(screen)
            screen.blit(pointer.Fullimage, pointer.rect)
            screeneffects.draw(screen)
            # pg.draw.rect(screen, BLACK, [int(b), c, 10, 10])

            pg.display.flip()


        pg.quit()
    init()

def strt_mapread():
    txt = "LRUDX.txt"
    sala = openSala(txt)
    tiles = mapread(sala)
    tile_breakable = pygame.sprite.Group()
    global size, offsets
    size = getSize(sala)
    offsets = getOffset(sala, size, "sala")
    player1 = Corak()
    player1.update([0, 0, "Map"])

    for tile in tiles:
        if tile.type == 2:
            tile_breakable.add(tile)
            tiles.remove(tile)

    while True:
        clock.tick(FPS)
        pygame.display.set_caption(str(round(clock.get_fps())))
        pointer.update(pg.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    input("continue")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.Do = [0, -1, "U"]

                elif event.key == pygame.K_a:
                    player1.Do = [-1, 0, "L"]
                elif event.key == pygame.K_d:
                    player1.Do = [1, 0, "R"]
                elif event.key == pygame.K_s:
                    player1.Do = [0, 0, "X"]
                elif event.key == pygame.K_z:
                    player1.Do = [-1, 0, "H"]
                elif event.key == pygame.K_x:
                    player1.Do = [1, 0, "H"]
                elif event.key == pygame.K_UP:
                    player1.Do = [0, -1, "U"]
                elif event.key == pygame.K_LEFT:
                    player1.Do = [-1, 0, "L"]
                elif event.key == pygame.K_RIGHT:
                    player1.Do = [1, 0, "R"]
                elif event.key == pygame.K_DOWN:
                    player1.Do = [0, 0, "X"]
                elif event.key == pygame.K_r:
                    while len(tile_breakable) > 0: del tile_breakable[0]

                    tiles = mapread(sala)
                    tile_breakable = pygame.sprite.Group()
                    break
                elif event.key == pygame.K_SPACE:
                    player1.focus = True
                    player1.cantGo = ["x"]
                    break
                else:
                    player1.Do = [0, 0, "Z"]
                player1.update(player1.Do)
        print(player1.at)
        for a in sala: print(a)

        'draw'
        screen.fill(WHITE)
        tiles.draw(screen)
        tile_breakable.draw(screen)
        screen.blit(pointer.Fullimage, pointer.rect)
        pygame.draw.rect(screen, BLUE, [player1.pos[0], player1.pos[1], size, size])
        pygame.display.flip()
    pygame.quit()

def mapread(sala):
    tiles = pygame.sprite.Group()

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
            tile = Tile(sala[Line][Colum], size, Line, Colum, offsets)
            tiles.add(tile)
    '''
    print("lines in list:", len(sala))
    print("colums in list:", len(sala[0]))
    print("list:", sala)
    print(temp)
    print("size:", size)
    '''
    return tiles

alltiles = []

'display setting'
screen = pg.display.set_mode((ScreenX, ScreenY), 0)
clock = pg.time.Clock()
pg.mouse.set_visible(False)
screen.fill(BLACK)

'sprite setting'
menu = pg.sprite.Group()
menu_strt = Spriter("menu.png", (26, 12), 3)
menu.add(menu_strt)

fader = Surfaces("fade", BLACK, ScreenXY, (0, 0))
screeneffects = pg.sprite.Group()
screeneffects.add(fader)
pointer = Spriter("pointer.png", (26, 12), 1)

allSprites = pg.sprite.Group()
allSprites.add(menu, pointer)

global level, sala, tile_breakable, click
click = False
strt_menu()
