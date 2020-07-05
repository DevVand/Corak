import pygame as pg
from Game.Corak.dicio import *
from Game.Corak.Worldgen3 import hall
from Game.Corak.mapcr import printmap
from Game.Corak.mapread4 import mapread
class Corak(pg.sprite.Sprite):
    def __init__(S):
        S.sprite = pg.Surface([size, size])
        S.sprite.fill(WHITE)

        S.sprite = Spriter("corak.png", 1, (0, 0))
        S.rect = S.sprite.get_rect()
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

        S.update([0, 0, "Map"])
        print(S.cantGo)
        S.update([0, 0, "x"])
        print(S.at)
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
            if S.focus :
                Do[0] *= 2
                Do[1] *= 2
            S.focus = False
            S.grab = False
            S.at[0] = S.at[0] + Do[0]
            S.at[1] = S.at[1] + Do[1]
            S.rect.x = size * S.at[0] + offsets[0]
            S.rect.y = size * S.at[1] + offsets[1]
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
                for tile in tiles_breakable:
                    if tile.at == [at[0] + direction, at[1]]:
                        tiles_breakable.remove(tile)
                if S.focus:
                    S.focus = False
                    print("focus")
                if S.grab: S.grab = False
        except: pass
        S.turn = False
        S.update([0, 0, "Map"])
    def update(S, Do):
        if Do[2] in "LRUDx": S.Move(Do)
        if Do[2] in "H": S.Hit(Do[0], S.at)
        if Do[2] in "X": S.Focus()
        if Do[2] in "Move": S.checkMove()
        if Do[2] in "Map": S.checkMap()
        if "get_at" in Do[2]: S.get_at(Do[0])

class Spriter(pg.sprite.Sprite):
    def __init__(s, type, frames, pos):
        pg.sprite.Sprite.__init__(s)
        temp = "../Sprites/"+type
        if frames > 1:
            s.frames = frames
            s.frame = 0
            s.type = type[:-4]

            s.Fullimage = pg.image.load(temp).convert_alpha()
            s.fullrect = s.Fullimage.get_rect()

            s.fullrect.x, s.fullrect.y = s.Fullimage.get_size()
            s.Fullimage = pg.transform.scale(s.Fullimage, (s.fullrect.x * upscale, s.fullrect.y * upscale))
            s.fullrect.x, s.fullrect.y = s.Fullimage.get_size()

            s.image = pg.Surface((s.fullrect.x / s.frames, s.fullrect.y), pg.SRCALPHA).convert_alpha()
            s.image.blit(s.Fullimage, (0, 0), (s.frame * (s.fullrect.x/s.frames), 0, s.fullrect.x, s.fullrect.y))
        else:
            s.image = pg.image.load(temp)
            s.rect = s.image.get_rect()
            s.rect.x, s.rect.y = s.image.get_size()
            s.image = pg.transform.scale(s.image, (s.rect.x * upscale, s.rect.y * upscale))

        s.rect = s.image.get_rect()
        s.update(pos)

        #screen.blit(Fullimage, (0, 0), area=Fullimage_region)
    def setFrame(s, to):
        s.frame = to
        if s.frame >= s.frames: s.frame = 0
        s.image.fill(CLEAR)
        s.image.blit(s.Fullimage, (0, 0), (s.frame * (s.fullrect.x/s.frames), 0, s.fullrect.x, s.fullrect.y))
    def update(s, pos):
        s.rect = s.image.get_rect()
        s.rect.center = (pos[0], pos[1])

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
    tiles_breakable, background, ttst = mapread(sala)

    #print("tiles", tiles)
    size = getSize(sala)

   # print("size", size)
    offsets = getOffset(sala, size, "sala")
    return sala, offsets, size, tiles_breakable, background, ttst

def CheckLevel(mapAt):
    intro = -1
    come_from = ""
    if corak.at[0] < 0:
        mapAt[0] += L
        come_from = "R"
        intro = 1
    elif corak.at[0] >= len(sala[0]):
        mapAt[0] += R
        come_from = "L"
        intro = 1
    elif corak.at[1] < 0:
        mapAt[1] += U
        come_from = "D"
        intro = 1
    elif corak.at[1] >= len(sala):
        mapAt[1] += D
        come_from = "U"
        intro = 1
    else: corak.checkMap()
    return mapAt, intro, come_from


    screeneffects.draw(screen)
    screen.blit(pointer.image, pointer.rect)
'display setting'
#screen = pg.display.set_mode((ScreenX, ScreenY))

screen2 = pg.display.set_mode((FScreenX, FScreenY))

screen = Surfaces("x", BLACK, ScreenXY, (0, 0))

clock = pg.time.Clock()
pg.mouse.set_visible(False)

'sprite setting'
menu_logo = Spriter("menu/logo.png", 1, (middlex, middley))
#menu_logo.image = pg.transform.scale(menu_logo.rect.x)
menu_click = Spriter("menu/click.png", 1, (middlex, middley * 1.5))

menu = pg.sprite.Group()
menu_strt = Spriter("menu/start.png", 3, (middlex, middley * 0.5))
menu_opt = Spriter("menu/options.png", 3, middle)
menu_quit = Spriter("menu/exit.png", 3, (middlex, middley * 1.5))
menu.add(menu_strt, menu_opt, menu_quit)

fader = Surfaces("fade", BLACK, ScreenXY, (0, 0))
counterlight = Surfaces("fade", BLACK, ScreenXY, (0, 0))
fader2 = Surfaces("fade", BLACK, ScreenXY, (0, 0))
screeneffects = pg.sprite.Group()
screeneffects.add(fader)

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
loop = False
temp = 255
temp2 = False
temp4 = ""
temp5 = False
temp6 = 1
intro2 = False
clickset = 0
intro = True
intro_count = 0

out = False
out2 = False
out3 = False
out_count = -1

intro_area = True
menu_area = False
mapgen_area = False
play_area = False
fade = False
level = []
alltiles = []
level = []
while True:
    ''
    mx, my = pg.mouse.get_pos()
    mx /= upscale
    my /= upscale
    clock.tick(FPS)
    pg.display.set_caption(str(round(clock.get_fps())))
    if intro_area:
        if intro_count == 0:
            fade_count -= 2
            if fade_count <= 0:
                intro_count = -1
                loop = True
                pointerLight.image = pg.transform.scale(playerLight.image, (16*upscale*2, 16*upscale*2))

            fader.image.set_alpha(fade_count)
        if loop:
            if temp <= 50: temp3 = True
            if temp >= 255: temp3 = False
            if temp3: temp +=5
            else: temp -= 5
            menu_click.image.set_alpha(temp)
        if out_count >= 0:
            if out_count == 1:
                fade_count += 20
                if fade_count >= 255: out_count += 1
            elif out_count == 2:
                fade_count -= 10
                if fade_count <= -100:
                    out_count += 1
            elif out_count >= 3:
                fade_count += 4
                if fade_count >= 400:
                    intro_count = 0
                    intro_area = False
                    menu_area = True
                    out_count = -1
            fader.image.set_alpha(fade_count)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                intro_count = -1
                out_count += 2
        'draw'
        pointer.update((mx, my))
        screen.image.fill(BLACK)

        screen.image.blit(menu_click.image, menu_click.rect)
        screen.image.blit(menu_logo.image, menu_logo.rect)
        screeneffects.draw(screen.image)

        pointerLight.update((mx, my))
        counterlight.image.blit(pointerLight.image, pointerLight.rect), pg.SRCALPHA
        screen.image.blit(counterlight.image, (0, 0), special_flags=pg.BLEND_MULT)
    if menu_area:
        if intro_count == 0 :
            fade_count -= 2
            if fade_count <= 0:
                intro_count = -1
            fader.image.set_alpha(fade_count)
        if out_count >= 0:
            fade_count += 15
            if fade_count >= 400:
                intro_count = 0
                out_count = -1
                menu_area = False
                mapgen_area = True
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
            if button.rect.collidepoint(pointer.rect.topleft):
                if click:
                    fade = True
                    temp3 = False
                    button.setFrame(2)
                elif not click:
                    button.setFrame(1)
                if clickset == 1:
                    clickset = 2
                    if "start" in button.type:
                        out_count = 0
                    if "options" in button.type: print("1")
                    if "exit" in button.type:
                        out_count = 0
                        temp2 = True
            else:
                button.setFrame(0)
        pointer.update((mx, my))

        if fade:
            if fade_count < 50:
               fade_count +=4
               fader.image.set_alpha(fade_count)
        if not fade:
            if fade_count >=0:
                fade_count -=8
                fader.image.set_alpha(fade_count)
        'draw'
        screen.image.fill(CUSTOM)

        for button in menu:
            screen.image.blit(button.image, button.rect)

        screen.image.blit(pointer.image, pointer.rect.topleft)
        screeneffects.draw(screen.image)
    if mapgen_area:
        if intro_count == 0:
            level = hall([0, 0, "strt"], level)
            fade_count -= 5
            fader.image.set_alpha(fade_count)
            if len(level) > 5:
                map = printmap(level)
                temp3 = True
                if fade_count <= -150:
                    intro_count = -1
                    out_count = 0
        if out_count >= 0:
            fade_count += 2
            fader.image.set_alpha(fade_count)
            if fade_count >= 400:
                out_count = -1
                intro_count = 0
                mapgen_area = False
                map_at = hall([0, 0, "get_pos_strt"], level)
                play_area = True
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
        pointer.update((mx, my))

        'draw'
        screen.image.fill(WHITE)
        if temp3: map.draw(screen.image)
        screeneffects.draw(screen.image)
        screen.image.blit(pointer.image, pointer.rect.topleft)
    if play_area:
        if intro_count >= 0:
            if intro_count == 1:
                sala, offsets, size, tiles_breakable, background, ttst = changeRoom(map_at, level)
                corak.update([temp4, 0, "get_at"])

                corak.sprite = pg.transform.scale(corak.sprite, (size, size))
                pointerLight.image = pg.transform.scale(playerLight.image, (size * int(upscale*2), size * int(upscale*2)))
                playerLight.image = pg.transform.scale(playerLight.image, (size * int(upscale*2), size * int(upscale*2)))
                intro_count = -1
                background.image.fill(CRED)
            if intro_count == 0:
                sala, offsets, size, tiles_breakable, background, ttst = changeRoom(map_at, level)
                corak = Corak()
                corak.update(["S", 0, "get_at"])
                corak.update([0, 0, "Map"])

                corak.sprite = pg.transform.scale(corak.sprite, (size, size))
                pointerLight.image = pg.transform.scale(playerLight.image, (size * int(upscale*2), size * int(upscale*2)))
                playerLight.image = pg.transform.scale(playerLight.image, (size * int(upscale*2), size * int(upscale*2)))
                intro_count = -1
                background.image.fill(CRED)

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

                background.image.fill(WHITE)
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
                    clickset = 1
                background.image.fill(CRED)
            elif event.type == pg.MOUSEMOTION:
                if temp6 > 0:
                    temp6 -= 5

            elif event.type == pg.KEYDOWN:
                if event.key == (pg.K_w or pg.K_UP):
                    corak.Do = [0, -1, "U"]
                elif event.key == (pg.K_a or pg.K_LEFT):
                    corak.Do = [-1, 0, "L"]
                elif event.key == (pg.K_d or pg.K_RIGHT):
                    corak.Do = [1, 0, "R"]
                elif event.key == (pg.K_s or pg.K_DOWN):
                    corak.Do = [0, 0, "X"]
                elif event.key == (pg.K_z or pg.K_q):
                    corak.Do = [-1, 0, "H"]
                elif event.key == (pg.K_x or pg.K_e):
                    corak.Do = [1, 0, "H"]

                elif event.key == (pg.K_BACKSPACE):
                    if FPS < 70:
                        FPS = 1000
                    else: FPS = 60

                elif event.key == pg.K_EQUALS:
                    print(corak.at, map_at, level[map_at[1]][map_at[0]])
                    for a in sala: print(a)
                    print(temp2, temp4)
                    print(corak.cantGo)

                    temp2 = True if not temp2 else False
                    break

                elif event.key == pg.K_SPACE:
                    corak.focus = True
                    corak.cantGo = ["x"]
                    break
                else:
                    corak.Do = [0, 0, "Z"]
                    temp5 = True if not temp5 else False
                corak.update(corak.Do)

                map_at, intro_count, temp4 = CheckLevel(map_at)

        if temp6 <= 0: temp6 = 1

        'draw'
        screen.image.fill(BLACK)
        screen.image.blit(background.image, background.rect)
        #tiles.draw(screen.image)
        #tiles_deco.draw(screen.image)

        screen.image.blit(ttst.image, ttst.rect)

        tiles_breakable.draw(screen.image)
        screen.image.blit(corak.sprite, corak.rect)

        if temp2:
            fader.image.set_alpha(fade_count)
            counterlight.image.fill(BLACK)

            pointerLight.update((mx, my))

            playerLight.update(corak.rect.center)

            counterlight.image.blit(pointerLight.image, pointerLight.rect)


            counterlight.image.blit(playerLight.image, playerLight.rect)

            fader.image.fill(BLACK)
            fader.image.set_alpha(temp6)


            screen.image.blit(counterlight.image, (0, 0), special_flags=pg.BLEND_MULT)
            screen.image.blit(fader.image, (0, 0))

        if temp5:
            screen.image.fill(WHITE)
            map.draw(screen.image)

        if temp6 < 180:
            temp6 += 1

    tst = pg.transform.scale(screen.image, (FScreenX, FScreenY))

    screen2.blit(tst, (0, 0))

    pg.display.update()
'''
pointerLight.update(pg.mouse.get_pos())
        playerLight.update((player1.rect.x+(size/2), player1.rect.y+(size/2)))

        counterlight.image.fill(BLACK)
        counterlight.image.blit(pointerLight.image, pointerLight.rect), pg.SRCALPHA
        counterlight.image.blit(playerLight.image, playerLight.rect), pg.SRCALPHA

'''