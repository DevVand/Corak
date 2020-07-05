import pygame as pg
from Game.Corak.dicio import *
from Game.Corak.Worldgen3 import hall
from Game.Corak.mapcr import printmap
from Game.Corak.mapread4 import mapread
class Corak(pg.sprite.Sprite):
    def __init__(S):
        S.image = pg.Surface([size, size])
        S.image.fill(BLACK)
        S.rect = S.image.get_rect()
        S.at = [1, 11]
        S.pos = [size * S.at[0] + offsets[0], size * S.at[1] + offsets[1]]
        S.Do = []
        S.turn = True
        S.jump = False
        S.air = False
        S.focus = False
        S.grab = False
    def get_at(S, Do):
        print("do", Do)
        try:
            for y in range(len(sala)):
                for x in range(len(sala[0])):
                   if Do in sala[y][x]: S.at = [x, y]
        except:
            print("at")
            print(y)
            print(x)
            print("len", len(sala))
            print("len", len(sala[0]))
            print(sala)
            print(Do)

        S.checkMap()
        S.Move([0, 0, ""])
    def checkMap(S):
        S.cantGo = []
        if S.focus: distance = 2
        else: distance = 1
        for i in range(1, distance+1):
            try:
                if sala[S.at[1]][S.at[0] + i] in "12":
                    S.cantGo.extend(["R", i * "R"])
            except: pass
            try:
                if S.at[0] - 1 >= 0:
                    if sala[S.at[1]][S.at[0] - i] in "12":
                        S.cantGo.extend(["L", i * "L"])
            except:
                pass
            try:
                if sala[S.at[1] + 1][S.at[0]] in "123":
                    S.cantGo.append("D")
            except: pass
            try:
                if S.at[1] - 1 >= 0:
                    if sala[S.at[1] - i][S.at[0]] in "123":
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
                S.checkMap()
            if S.jump:
                S.jump = False
            S.turn = True
            S.update([0, 0, "Move"])
    def Move(S, Do):
        alltrue = True
        for direction in S.cantGo:
            if direction in Do[2]:
                alltrue = False
                if S.air and direction in "LR": S.grab = True
                if S.focus and direction in "LRU":
                    S.focus = False
                    alltrue = True

        if alltrue:
            if Do[1] == -1: S.jump = True
            if S.focus : Do[0] *= 2
            if S.focus : Do[1] *= 2
            S.focus = False
            S.grab = False

            S.at[0] = S.at[0] + Do[0]
            S.at[1] = S.at[1] + Do[1]
            S.rect.x = size * S.at[0] + offsets[0]
            S.rect.y = size * S.at[1] + offsets[1]
            S.rect.x = S.rect.x
            S.rect.y = S.rect.y
        S.turn = False
    def Focus(S):
        if S.grab: S.grab = False
        if not (S.focus or S.air):
            S.focus = True
        S.turn = False
        S.checkMap()
    def Hit(S, direction, at):
        try:
            if str(sala[at[1]][at[0] + direction]) in "2":
                sala[at[1]] = sala[at[1]][:at[0]+direction:] + "0" + sala[at[1]][-(len(sala[at[1]])-1 - (direction + at[0]))::]
                for tile in tile_breakable:
                    if tile.at == [at[0] + direction, at[1]]:
                        tile_breakable.remove(tile)
                if S.focus:
                    S.focus = False
                    print("focus")
                if S.grab: S.grab = False
        except: pass
        S.turn = False
        S.update([0, 0, "Map"])
    def update(S, Do):
        if Do[2] in "LRUD": S.Move(Do)
        if Do[2] in "H": S.Hit(Do[0], S.at)
        if Do[2] in "X": S.Focus()
        if Do[2] in "Move": S.checkMove()
        if Do[2] in "Map": S.checkMap()
        if "get_at" in Do[2]: S.get_at(Do[0])

class Spriter(pg.sprite.Sprite):
    def __init__(s, type, frames, pos):
        pg.sprite.Sprite.__init__(s)
        s.frames = frames
        s.frame = 0
        s.type = type[:-4]
        temp = "../Sprites/"+type

        #upscale all images
        s.Fullimage = pg.image.load(temp)

        s.rx, s.ry = s.Fullimage.get_size()
        s.Fullimage = pg.transform.scale(s.Fullimage, (s.rx * upscale, s.ry * upscale))
        s.rx, s.ry = s.Fullimage.get_size()

        s.image = pg.Surface((s.rx / s.frames, s.ry), pg.SRCALPHA)
        s.image.blit(s.Fullimage, (0, 0), (s.frame * s.rx/s.frames, 0, s.rx, s.ry))

        s.rect = s.image.get_rect()

        s.rect = pg.Rect(s.rect.x, s.rect.y, s.rx/s.frames, s.ry)

        s.offsetx, s.offsety = getOffset([s.rx/s.frames, s.ry], 0, "Sprite")
        s.update(pos)

        #screen.blit(Fullimage, (0, 0), area=Fullimage_region)
    def setFrame(s, to):
        s.frame = to
        if s.frame >= s.frames: s.frame = 0
        s.image.fill(CLEAR)
        s.image.blit(s.Fullimage, (0, 0), ((s.frame) * s.rx/s.frames, 0, s.rx, s.ry))
    def update(s, pos):
        s.rect.x = pos[0] - s.offsetx
        s.rect.y = pos[1] - s.offsety

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

        if "fade" in type:
            s.image.set_alpha(0)

def changeRoom(map_at, level):
    #print("changeroom")
    txt = "../Salas/" + level[map_at[1]][map_at[0]]

    #print("txt", txt)
    sala = openSala(txt)

    #print("sala", sala)
    tiles, background = mapread(sala)

    #print("tiles", tiles)
    tile_breakable = pg.sprite.Group()

    size = getSize(sala)

   # print("size", size)
    offsets = getOffset(sala, size, "sala")
    for tile in tiles:
        if tile.type == 2:
            tile_breakable.add(tile)
            tiles.remove(tile)
    return sala, offsets, size, tiles, tile_breakable, background

def CheckLevel(mapAt):
    temp7 = False
    come_from = ""
    if player1.at[0] < 0:
        mapAt[0] += L
        come_from = "R"
        temp7 = True
    elif player1.at[0] >= len(sala[0]):
        mapAt[0] += R
        come_from = "L"
        temp7 = True
    elif player1.at[1] < 0:
        mapAt[1] += U
        come_from = "D"
        temp7 = True
    elif player1.at[1] >= len(sala):
        mapAt[1] += D
        come_from = "U"
        temp7 = True
    else: player1.checkMap()
    return mapAt, temp7, come_from


    screeneffects.draw(screen)
    screen.blit(pointer.image, pointer.rect)
'display setting'
screen = pg.display.set_mode((ScreenX, ScreenY), 0)
clock = pg.time.Clock()
pg.mouse.set_visible(False)
screen.fill(BLACK)

'sprite setting'
menu = pg.sprite.Group()
menu_strt = Spriter("menu/start.png", 3, (middlex, middley - 105))
menu_opt = Spriter("menu/options.png", 3, middle)
menu_quit = Spriter("menu/exit.png", 3, (middlex, middley + 105))
menu.add(menu_strt, menu_opt, menu_quit)

fader = Surfaces("fade", BLACK, ScreenXY, (0, 0))

fader2 = Surfaces("fade", BLACK, ScreenXY, (0, 0))
screeneffects = pg.sprite.Group()
screeneffects.add(fader)
#pointer = Spriter("pointer.png", 1, (0, 0))

pointer = Spriter("menu/pointer.png", 1, (0, 0))

pointerLight = Spriter("spotlight2.png", 1, (0, 0))

playerLight = Spriter("spotlight2.png", 1, (0, 0))

allSprites = pg.sprite.Group()
allSprites.add(menu, pointer)
RGB = [101, 100, 111]
'var'
global sala
click = False
fade_count = 255
temp2 = False
temp4 = ""
temp5 = False
temp6 = 1
intro2 = False
clickset = 0
intro = True
out = False
menu_area = True
mapgen_area = False
play_area = False
fade = False
level = []
alltiles = []
level = []

while True:
    ''
    clock.tick(FPS)
    pg.display.set_caption(str(round(clock.get_fps())))

    if menu_area:
        if intro:
            fade_count -= 5
            if fade_count <= 0: intro = False
            fader.image.set_alpha(fade_count)
        if out:
            fade_count += 15
            if fade_count >= 400:
                out = False
                menu_area = False
                mapgen_area = True
                intro = True
                temp3 = False
                if temp2: pg.quit()
            fader.image.set_alpha(fade_count)
        fade = False

        if clickset == 1: clickset = 0
        'inputs'
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
        for button in menu:
            if pg.sprite.collide_rect_ratio(0.7)(pointer, button):
                if click:
                    fade = True
                    temp3 = True
                    button.setFrame(2)
                elif not click:
                    button.setFrame(1)
                if clickset == 1:
                    clickset = 2
                    if "start" in button.type:
                        out = True
                    if "options" in button.type: print("1")
                    if "exit" in button.type:
                        out = True
                        temp2 = True
            else:
                button.setFrame(0)

        if fade:
            if fade_count < 50:
               fade_count +=4
               fader.image.set_alpha(fade_count)
        if not fade:
            if fade_count >=0:
                fade_count -=8
                fader.image.set_alpha(fade_count)
        'draw'
        pointer.update(pg.mouse.get_pos())
        screen.fill(CUSTOM)
        menu.draw(screen)
        screeneffects.draw(screen)
        screen.blit(pointer.image, pointer.rect)
    if mapgen_area:
        if intro:
            level = hall([0, 0, "strt"], level)
            fade_count -= 5
            fader.image.set_alpha(fade_count)
            if len(level) > 5:
                map = printmap(level)
                temp3 = True
                if fade_count <= -150:
                    intro = False
                    out = True
        if out:
            fade_count += 2
            fader.image.set_alpha(fade_count)
            if fade_count >= 400:
                out = False
                mapgen_area = False
                map_at = hall([0, 0, "get_pos_strt"], level)
                play_area = True
                intro = True
                temp3 = True
                temp2 = False
        'inputs'
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

        pointer.update(pg.mouse.get_pos())
        screen.fill(WHITE)
        if temp3: map.draw(screen)
        screeneffects.draw(screen)
        screen.blit(pointer.image, pointer.rect)
    if play_area:
        if intro2:
            sala, offsets, size, tiles, tile_breakable, background = changeRoom(map_at, level)
            player1.update([temp4, 0, "get_at"])

            intro2 = False
        if intro:

            if temp3:
                sala, offsets, size, tiles, tile_breakable, background = changeRoom(map_at, level)
                player1 = Corak()
                player1.update(["S", 0, "get_at"])
                player1.update([0, 0, "Map"])
                temp3 = False
            fade_count -= 2
            fader.image.set_alpha(fade_count)
            if fade_count <= -0:
                intro = False
        'inputs'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                elif event.button == 3:
                    print(1)

                background.image.fill(BLUE)
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
                    clickset = 1
                background.image.fill(WHITE)


            elif event.type == pg.MOUSEMOTION:
                if temp6 > 0:
                    temp6 -= 5

            elif event.type == pg.KEYDOWN:
                if event.key == (pg.K_w or pg.K_UP):
                    player1.Do = [0, -1, "U"]
                elif event.key == (pg.K_a or pg.K_LEFT):
                    player1.Do = [-1, 0, "L"]
                elif event.key == (pg.K_d or pg.K_RIGHT):
                    player1.Do = [1, 0, "R"]
                elif event.key == (pg.K_s or pg.K_DOWN):
                    player1.Do = [0, 0, "X"]
                elif event.key == (pg.K_z or pg.K_q):
                    player1.Do = [-1, 0, "H"]
                elif event.key == (pg.K_x or pg.K_e):
                    player1.Do = [1, 0, "H"]

                elif event.key == pg.K_EQUALS:
                    print(player1.at, map_at, level[map_at[1]][map_at[0]])
                    for a in sala: print(a)
                    print(temp2, temp4)
                    print(player1.cantGo)
                    break

                elif event.key == pg.K_SPACE:
                    player1.focus = True
                    player1.cantGo = ["x"]
                    break
                else:
                    player1.Do = [0, 0, "Z"]

                    if temp5: temp5 = False
                    else: temp5 = True
                player1.update(player1.Do)

                map_at, intro2, temp4 = CheckLevel(map_at)

        'draw'

        screen.fill(BLACK)

        screen.blit(background.image, background.rect)
        tiles.draw(screen)
        tile_breakable.draw(screen)


        fader.image.set_alpha(fade_count)
        if temp6 <= 0: temp6 = 1
        if temp5:
            screen.fill(WHITE)
            map.draw(screen)
        pg.draw.rect(screen, BLUE, [player1.rect.x, player1.rect.y, size, size])

        fader.image.fill(BLACK)

        pointerLight.update(pg.mouse.get_pos())
        fader.image.blit(pointerLight.image, pointerLight.rect), pg.SRCALPHA


        playerLight.update(player1.rect.bottomright)
        playerLight.image = pg.transform.scale(playerLight.image, (size*5, size*5))

        fader.image.blit(playerLight.image, playerLight.rect.center), pg.SRCALPHA



        fader2.image.fill(BLACK)

        fader2.image.set_alpha(temp6)

        screen.blit(fader.image, (0, 0), special_flags=pg.BLEND_MULT)


        screen.blit(fader2.image, (0, 0))

        if temp6 < 190:
            temp6 +=3

    pg.display.update()
'''
pointerLight.update(pg.mouse.get_pos())
        playerLight.update((player1.rect.x+(size/2), player1.rect.y+(size/2)))

        fader.image.fill(BLACK)
        fader.image.blit(pointerLight.image, pointerLight.rect), pg.SRCALPHA
        fader.image.blit(playerLight.image, playerLight.rect), pg.SRCALPHA

'''