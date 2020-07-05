import pygame as pg
from Game.Corak.dicio import *
from Game.Corak.Worldgen3 import hall
from Game.Corak.mapcr import printmap
from Game.Corak.mapread4 import mapread, generatenew

class Corak(pg.sprite.Sprite):
    def __init__(S):
        S.ac = [0, 0]
        S.sprite = pg.Surface([size, size])
        S.left = False
        S.sprite = Spriter("corak full.png", [7, 7], (0, 0))
        S.at = [1, 11]
        S.pos = [size * S.at[0] + offsets[0], size * S.at[1] + offsets[1], 0]

        S.pos_offsetX = S.at[0] * size
        S.pos_offsetY = S.at[1] * size

        S.Do = []
        S.turn = True
        S.jump = False
        S.air = False
        S.focus = False
        S.grab = False
        S.modLight = [1, 0]
        S.modfocus = False
    def get_at(S, Do):
        try:
            for y in range(len(sala)):
                for x in range(len(sala[0])):
                   if Do in sala[y][x]: S.at = [x, y]
        except: pass
        S.checkMap()
        S.Move([0, 0, "x"])
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
        S.checkMove()
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
            S.checkMove()
    def Move(S, Do):
        S.grab = False
        alltrue = True
        for direction in S.cantGo:
            if direction in Do[2]:
                alltrue = False
                if S.air and direction in "LR":
                    S.grab = True
                    if "L" in Do[2]:
                        S.left = True
                    elif "R" in Do[2]:
                        S.left = False
                if S.focus and direction in "LRU":
                    S.focus = False
                    alltrue = True

        if alltrue:
            if Do[1] == -1: S.jump = True
            if S.focus :
                Do[0] *= 2
                Do[1] *= 2
            S.focus = False

            if "L" in Do[2]:
                S.left = True
            elif "R" in Do[2]:
                S.left = False

            S.at[0] = S.at[0] + Do[0]
            S.at[1] = S.at[1] + Do[1]
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
                if S.grab: S.grab = False
        except: pass
        S.turn = False
        S.checkMap()
    def update(S, Do):
        if Do[2] in "LRUDx": S.Move(Do)
        if Do[2] in "H": S.Hit(Do[0], S.at)
        if Do[2] in "X": S.Focus()
    def posoffset(S):

        '''
        S.ac[0] += (S.at[0] * size) - S.pos_offsetX / 4
        S.ac[1] += (S.at[1] * size) - S.pos_offsetY / 4

        S.pos_offsetX += S.ac[0]
        S.pos_offsetY += S.ac[1]

        S.sprite.update([S.pos_offsetX + offsets[0], S.pos_offsetY + offsets[1]])
        '''

        S.pos_offsetX = abs(S.pos_offsetX + S.at[0] * size) / 2
        S.pos_offsetY = abs(S.pos_offsetY + S.at[1] * size) / 2

        S.sprite.update([int(S.pos_offsetX + .5) + offsets[0], int(S.pos_offsetY + .5) + offsets[1]])

class Spriter(pg.sprite.Sprite):
    def __init__(s, type, frames, pos):
        pg.sprite.Sprite.__init__(s)
        temp = "../Sprites/"+type

        if frames[1] >= 1 or frames[0] >= 1:
            s.frames = frames
            s.frame = [0, 0]
            s.type = type[:-4]
            s.fullimage = pg.image.load(temp).convert_alpha()
            s.fullrect = s.fullimage.get_rect()
            s.fullrect.x, s.fullrect.y = s.fullimage.get_size()
            if not frames[0] > 1:
                s.fullimage = pg.transform.scale(s.fullimage, (s.fullrect.x * upscale, s.fullrect.y * upscale))
            s.fullrect.x, s.fullrect.y = s.fullimage.get_size()

            temp = [0, 0]
            temp[0] = int(s.fullrect.x / s.frames[1])
            temp[1] = int(s.fullrect.y / s.frames[0])
            s.image = pg.Surface((temp[0], temp[1])).convert_alpha()
            s.image.fill(CLEAR)
            s.image.blit(s.fullimage, (0, 0), (s.frame[1] * temp[0], s.frame[0] * temp[1], s.fullrect.x, s.fullrect.y))

        else:
            s.image = pg.image.load(temp)
            s.rect = s.image.get_rect()
            s.rect.x, s.rect.y = s.image.get_size()
            s.image = pg.transform.scale(s.image, (s.rect.x * upscale, s.rect.y * upscale))
            s.frame, s.frames = [0, 0], [0, 0]

        s.rect = s.image.get_rect()

        s.update(pos)

    def setFrame(s, to):
        s.frame = to
        if s.frame[1] >= s.frames[1]: s.frame[1] = 0
        s.image.fill(CLEAR)
        s.image.blit(s.fullimage, (0, 0), (s.frame[1] * int(s.fullrect.x / s.frames[1]), s.frame[0] * int(s.fullrect.y / s.frames[0]), s.fullrect.x, s.fullrect.y))
    def update(s, pos):
        s.rect = s.image.get_rect()
        'to int'
        temp = [0, 0]
        temp[0] = int(pos[0])
        temp[1] = int(pos[1])

        if s.frames[0] > 1:
            s.rect.x = pos[0]
            s.rect.y = pos[1]
        else: s.rect.center = (temp[0], temp[1])

class Surfaces(pg.sprite.Sprite):
    def __init__(s, type, colour, size, at):
        pg.sprite.Sprite.__init__(s)
        if ".png" in type: s.image = pg.image.load("../Sprites/" + type).convert_alpha()
        else: s.image = pg.Surface(size)

        s.rect = s.image.get_rect()
        s.rect.centerx = at[0]
        s.rect.centery = at[1]
        Surfaces.Do(s, type, colour)
    def Do(s, type, colour):
        if "fade" in type:
            s.image.fill(colour)
            s.image.set_alpha(0)
        if "X" in type:
            s.image.fill(colour)
            s.image.set_colorkey(colour)

def changeRoom(map_at, level):
    if len(map_at) >= 3: sala = openSala("../Salas/tutorial/" + str(map_at[0]))
    else:
        txt = "../Salas/" + level[map_at[1]][map_at[0]]
        sala = openSala(txt)

    tiles_breakable, background, tiles_draw, tiles_base = mapread(sala)

    size = getSize(sala)

    offsets = getOffset(sala, size, "sala")
    return sala, offsets, size, tiles_breakable, background, tiles_draw, tiles_base

def CheckLevel(mapAt):
    out = -1
    come_from = ""

    if corak.at[0] < 0:
        mapAt[0] += L
        come_from = "R"
        out = 2
    elif corak.at[0] >= len(sala[0]):
        mapAt[0] += R
        come_from = "L"
        out = 2
    elif corak.at[1] < 0:
        mapAt[1] += U
        come_from = "D"
        out = 2
    elif corak.at[1] >= len(sala):
        mapAt[1] += D
        come_from = "U"
        out = 2
    elif sala[corak.at[1]][corak.at[0]] in "x":
        out = 2
        mapAt[0] += 1
        if mapAt[0] > 4:
            out = 4
            mapAt = hall([0, 0, "get_pos_strt"], level)

    elif sala[corak.at[1]][corak.at[0]] in "R":
        out = 3

    else: corak.checkMap()

    return mapAt, out, come_from


    screeneffects.draw(screen)
    screen.blit(pointer.image, pointer.rect.center)

def intro_Area(InOut):
    if InOut == 0:
        global intro, out, looper, fade_count, mod, tempkeep
        tempkeep = ["intro", "out", "looper", "fade_count", "mod"]
        intro, out, looper, fade_count, mod = 0, -1, [0, False], 0, 0
    if intro == 0:
        # fadei in
        fade_count -= 2

        # set fade
        if fade_count <= 0:
            intro = -1
            pointerLight.image = pg.transform.scale(playerLight.image, (16*upscale*2, 16*upscale*2))

        fader.image.set_alpha(fade_count)
    if out >= 0:
        if out == 1: # fade out
            fade_count += 20
            if fade_count >= 255: out += 1
        elif out == 2: # fade in
            fade_count -= 10
            if fade_count <= -100:
                out += 1
        elif out >= 3:
            fade_count += 4
            if fade_count >= 400:
                intro = 0
                mod = 2
                out = -1
        fader.image.set_alpha(fade_count)

    #loop
    if looper[0] <= 50: looper[1] = True
    if looper[0] >= 230: looper[1] = False
    if looper[1]: looper[0] += 8
    else: looper[0] -= 8
    menu_click.image.set_alpha(looper[0])

    'input'
    if out <= 0:
        if click:
            intro = -1
            out += 2
            trigger[1][0] = True
            trigger[2][0] = True

    'draw'
    screen.image.fill(BLACK)

    screen.image.blit(menu_click.image, menu_click.rect)
    screen.image.blit(menu_logo.image, menu_logo.rect)
    screeneffects.draw(screen.image)

    pointerLight.update((mx, my))
    counterlight.image.blit(pointerLight.image, pointerLight.rect)
    screen.image.blit(counterlight.image, (0, 0), special_flags=pg.BLEND_MULT)

    return InOut + mod

def menu_Area(InOut):
    if InOut == 0:
        global intro, out, fade_count, mod, opt_menu, i, tempkeep
        tempkeep = ["intro", "out", "fade_count", "mod", "opt_menu", "i"]
        intro, out, fade_count, mod, i = 0, -1, 255, 0, 0
    if intro == 0 :
        # fade in
        fade_count -= 4
        # set fade
        if fade_count <= 0:
            intro = -1
        fader.image.set_alpha(fade_count)
    if out >= 0:
        # fade out
        fade_count += 15
        # set fade
        if fade_count >= 230:
            # menu
            if out == 2:
                out = -1
                intro = 0
                i = 1
                for a in range(3):
                    tempBlit.image.blit(opt_icons.fullimage, (middlex * 0.30, middley * 1.30 - (50 * a)), (0, (opt_icons.fullrect.y / opt_icons.frames[0]) * a, opt_icons.fullrect.x,opt_icons.fullrect.y / opt_icons.frames[0]))
            if out == 2.1:
                out = -1
                intro = 0
                i = 0


            if out == 3:
                out = -1
                intro = 0
                i = 1
                for a in range(3):
                    tempBlit.image.blit(opt_icons.fullimage, (middlex * 0.30, middley * 1.30 - (50 * a)), (0, (opt_icons.fullrect.y / opt_icons.frames[0]) * a, opt_icons.fullrect.x,opt_icons.fullrect.y / opt_icons.frames[0]))
            if out == 3.1:
                out = -1
                intro = 0
                i = 0
            # strt
            if out == 1: mod = 49
            elif out == 10: mod = 100
        fader.image.set_alpha(fade_count)

    'inputs'
    if out <= 0:
        for btn in menu[i]:
            if btn.rect.collidepoint(pointer.rect.center):
                btn.setFrame([0, 1])
                if click:
                    btn.setFrame([0, 2])
                    if i == 0:
                        if "start" in btn.type: out = 1
                        if "options" in btn.type: out = 2
                        if "credits" in btn.type: out = 3
                        if "exit" in btn.type: out = 10
                    elif i == 1:
                        if "small" in btn.type: out = 0
                        elif "medium" in btn.type: pointer.setFrame([0, pointer.frame[1] + 1])
                        elif "large" in btn.type: pass
                        elif "back" in btn.type: out = 2.1
                        elif "pointer1" in btn.type: pointer.setFrame([0, 0])
                        elif "pointer2" in btn.type: pointer.setFrame([0, 1])
                        elif "pointer3" in btn.type: pointer.setFrame([0, 2])
                        elif "pointer4" in btn.type: pointer.setFrame([0, 3])
                        elif "vol0" in btn.type:
                            btn.setFrame([0, 1])
                        elif "vol1" in btn.type:
                            btn.setFrame([0, 1])
                        elif "music0" in btn.type:
                            btn.setFrame([0, 1])
                        elif "music1" in btn.type:
                            btn.setFrame([0, 1])
            else:
                btn.setFrame([0,0])

    '''
    if temp:
        if fade_count < 50:
           fade_count += 4
           fader.image.set_alpha(fade_count)
    if not temp:
        if fade_count >= 0:
            fade_count -= 8
            fader.image.set_alpha(fade_count)
    '''

    'draw'
    screen.image.fill(CUSTOM)
    for btn in menu[i]: screen.image.blit(btn.image, btn.rect)
    if opt_menu:  screen.image.blit(tempBlit.image, (0, 0))
    screen.image.blit(pointer.image, pointer.rect.center)
    screeneffects.draw(screen.image)

    return InOut + mod

def mapgen_Area(InOut):
    if InOut == 0:
        global intro, out, level, fade_count, tempsc, mod, tempkeep
        tempkeep = ["intro", "out", "fade_count", "tempsc", "mod"]
        intro, out, fade_count, mod = 0, -1, 255, 0
    if intro == 0:
        fade_count -= 5
        level = hall([0, 0, "strt"], level)
        fader.image.set_alpha(fade_count)
        if len(level) > 5:
            tempsc = printmap(level)
            if fade_count <= 0:
                intro = -1
                out = 0
    if out >= 0:
        fade_count += 2
        fader.image.set_alpha(fade_count)
        if fade_count >= 0:
            mod = 9
    print(fade_count)

    'draw'
    screen.image.fill(WHITE)
    if len(level) > 5: tempsc.draw(screen.image)
    screen.image.blit(pointer.image, pointer.rect.center)
    screeneffects.draw(screen.image)

    return InOut + mod

def play_Area(InOut):
    screen
    if InOut == 0:
        global intro, out, fade_count, mod
        global sala, offsets, size, tiles_breakable, background, tiles_draw, tiles_base
        global moveLight, corak, map_at, temp4, frame
        intro, out, fade_count, mod = 4, -1, 0, 0
        frame = 0
        #map_at = [0,0,0,0]
        map_at = hall([0, 0, "get_pos_strt"], level)
    if intro >= 0:
        if intro >= 1:
            sala, offsets, size, tiles_breakable, background, tiles_draw, tiles_base = changeRoom(map_at, level)
            moveLight = 1

            if intro >= 4:
                background.image.fill(BLACK)
                tiles_draw.image.fill(WHITE2)
                tiles_draw.image.blit(tiles_base.image, (0, 0))
                tiles_draw.image.set_colorkey(WHITE2)

                if intro == 4: corak = Corak()
                corak.get_at("S")
                corak.checkMap()
                if map_at[0] >= 4:
                    intro = 1

            elif intro == 1:
                background.image.fill(CUSTOM2)
                tiles_draw.image.fill(CUSTOM)
                tiles_draw.image.blit(tiles_base.image, (0, 0))
                tiles_draw.image.set_colorkey(CUSTOM)

                corak = Corak()
                map_at = hall([0, 0, "get_pos_strt"], level)
                corak.get_at("S")
                corak.checkMap()
                intro = -1

            elif intro == 2:
                background.image.fill(CUSTOM3)
                tiles_draw.image.fill(CUSTOM)
                tiles_draw.image.blit(tiles_base.image, (0, 0))
                tiles_draw.image.set_colorkey(CUSTOM)
                corak.get_at(temp4)
            elif intro == 3:
                corak.get_at("0")

            # scale
            corak.modLight[1] = (size * int(upscale * 2.5)) * corak.modLight[0]
            corak.sprite.image = pg.transform.scale(corak.sprite.image, (size, size))
            pointerLight.image = pg.transform.scale(playerLight.image, (corak.modLight[1], corak.modLight[1]))
            playerLight.image = pg.transform.scale(playerLight.image, (corak.modLight[1], corak.modLight[1]))

            if "mod-" in level[map_at[1]][map_at[0]]:

                background.image.fill(CUSTOM2)
                tiles_draw.image.fill(CRED)
                tiles_draw.image.blit(tiles_base.image, (0, 0))
                tiles_draw.image.set_colorkey(CRED)

            print(corak.at, map_at, level[map_at[1]][map_at[0]])

            intro = 0
            corak.Do = [0, 0, "Z"]
        fade_count -= 1
        if fade_count <= 0: intro = -1
        fader.image.set_alpha(fade_count)
    if out >= 0:

        fade_count += 7
        if fade_count >= 250:
            if out == 1: intro = 1
            if out == 2: intro = 2
            if out == 3: intro = 3
            if out == 4: intro = 4
            if out == 5: intro = 5
            out = -1
        fader.image.set_alpha(fade_count)
    '''
    if pause_area:
        menuCount = 0
        if clickset == 1: clickset = 0

        screen.image.blit(tempscreen.image, (0, 0))
        'input'
        for button in menu[0]:
            screen.image.blit(button.image, button.rect)
            if button.rect.collidepoint(pointer.rect.center):
                button.setFrame([0, 1])
                if click:
                    if not menuTrigger[1][0]:
                        menuTrigger[1][0] = True
                        menuTrigger[1][1] = True
                    fade = True
                    temp3 = False
                    button.setFrame([0, 2])
                if clickset == 1:
                    clickset = 2
                    if "start" in button.type:
                        if not menuTrigger[2][0]:
                            menuTrigger[2][0] = True
                            menuTrigger[2][1] = True
                        intro = 3
                        out = 3
                    if "options" in button.type:
                        menuTrigger[1][0] = False
                        trigger[2] = True
                        pointer.setFrame([0, pointer.frame[1] + 1])
                    if "exit" in button.type:
                        out = 0
                        temp2 = True
                if not menuTrigger[0][0]:
                    menuTrigger[0][0] = True
                    menuTrigger[0][1] = True

                menuCount += 1

            else:
                button.setFrame([0, 0])

        if menuCount == 0:
            menuTrigger[0][0], menuTrigger[2][0] = False, False

        screen.image.blit(pointer.image, pointer.rect.center)
    '''

    if clickset:
        tiles_draw.image.fill(GRAY)
        tiles_draw.image.set_colorkey(GRAY)

        tiles_draw.image.fill(RGB)
        tiles_draw.image.set_colorkey(RGB)
        tiles_draw.image.blit(tiles_base.image, (0, 0))
    if click: background.image.fill((20, 10, 10))

    if keypress:
        corak.update(corak.Do)
        map_at, out, temp4 = CheckLevel(map_at)

    corak.posoffset()
    'frame'
    # air
    if corak.air:
        frame += 1
        if frame > 1: frame = 0
        corak.sprite.setFrame([2, frame])
    # grab
    if corak.grab:
        frame += 1
        if frame > 1: frame = 0
        corak.sprite.setFrame([1, frame])
    # jump
    if "U" in corak.Do[2]:
        frame += 1
        if frame > 3: frame = 0
        corak.sprite.setFrame([3, frame])
    # ground
    elif not corak.air:
        frame = 1
        corak.sprite.setFrame([0, frame])
    # focus
    if corak.focus:
        frame = 0
        corak.sprite.setFrame([4, frame])
    # dash
    if not corak.at[0] * size - 0.01 < corak.pos_offsetX < corak.at[0] * size + 0.01:
        frame = 1
        corak.sprite.setFrame([4, frame])
    # air
    if not corak.at[1] * size - 0.02 < corak.pos_offsetY:
        frame = +1
        if frame > 1: frame = 0
        corak.sprite.setFrame([2, frame])
    if corak.left or corak.Do[0] == -1: corak.sprite.image = pg.transform.flip(corak.sprite.image, True, False)

    'draw'
    screen.image.blit(background.image, background.rect)
    # tiles.draw(screen.image)

    screen.image.blit(corak.sprite.image, corak.sprite.rect)
    screen.image.blit(tiles_draw.image, tiles_draw.rect)

    # screen.image.blit(tiles_deco.image, tiles_deco.rect)

    screen.image.blit(pointer.image, pointer.rect.center)

    tiles_breakable.draw(screen.image)
    if temp2:
        fader2.image.set_alpha(fade_count)
        counterlight.image.fill(BLACK)

        pointerLight.update((mx, my))
        counterlight.image.blit(pointerLight.image, pointerLight.rect)

        playerLight.update(corak.sprite.rect.center)
        counterlight.image.blit(playerLight.image, playerLight.rect)

        counterlight.image.set_alpha(moveLight)

        fader2.image.fill(BLACK)
        fader2.image.set_alpha(moveLight)

        screen.image.blit(counterlight.image, (0, 0), special_flags=pg.BLEND_MULT)
        screen.image.blit(fader2.image, (0, 0))
    if temp2: screen.image.blit(pointer.image, pointer.rect.center)

    if moveLight < 150:
        moveLight += 1.5

    screeneffects.draw(screen.image)
    return InOut + mod

def end_Area(InOut):
    return True

'display setting \' '
#screen = pg.display.set_mode((ScreenX, ScreenY))
toBlit = pg.display.set_mode((FScreenX, FScreenY))

screen = Surfaces("x", BLACK, ScreenXY, (0, 0))
tempscreen = Surfaces("x", BLACK, ScreenXY, (0, 0))

clock = pg.time.Clock()

pg.mouse.set_visible(False)

'audio setting   \' '
#mixer = pg.mixer.Sound("../Sound/s_4.wav")

mixerOn = [True, # 0 strt
           True, # 1 music
           True, # 2 menu
          [False, False],
          [False, True, 0],
          [False, False, False, False]
          ]
pg.mixer.pre_init(44200, 16, 2)
pg.mixer.init()

vol = []
trigger = []
Mvol = 10
Evol = 10

#
pg.mixer.music.load("../Sound/kpLoop.wav")
trigger.append([True, False])
vol.append(0.0)

Piano = pg.mixer.Sound("../Sound/pianoLoop.wav")
Piano.set_volume(0)
vol.append(0.0)
trigger.append([False, False])

mLoop = pg.mixer.Sound("../Sound/mLoop.wav")
mLoop.set_volume(0)
vol.append(0.0)
trigger.append([False, False])

#menu
menuTrigger = []
select = pg.mixer.Sound("../Sound/select.wav")
select.set_volume(0.9)
menuTrigger.append([False, False])

clicks = pg.mixer.Sound("../Sound/click.wav")
clicks.set_volume(0.8)
menuTrigger.append([False, False])

click2 = pg.mixer.Sound("../Sound/click2.wav")
click2.set_volume(0.7)
menuTrigger.append([False, False])

pg.mixer.music.set_volume(0)

Piano.play(-1)
mLoop.play(-1)
pg.mixer.music.play(-1)

menuCount = 0

'sprite setting  \' '
# menu intro
menu_logo = Spriter("menu/intro/logo.png", [1, 1], (middlex, middley))
#menu_logo.image = pg.transform.scale(menu_logo.image, menu_logo.rect.x)
menu_click = Surfaces("menu/intro/click.png", CLEAR, [1, 1], (middlex, middley * 1.3))

# menu
menu = []
menu.append(pg.sprite.Group())
menu_strt = Spriter("menu/start.png", [1, 3], (middlex, middley * 0.4))
menu_opt = Spriter("menu/options.png", [1, 3], (middlex, middley * 0.8))
menu_credits = Spriter("menu/credits.png", [1, 3], (middlex, middley * 1.2))
menu_exit = Spriter("menu/exit.png", [1, 3], (middlex, middley * 1.6))
menu[0].add(menu_strt, menu_opt, menu_exit, menu_credits)
menu.append(pg.sprite.Group())

opt_menu = False
menu.append(pg.sprite.Group())
menu_back = Spriter("menu/options/back.png", [1, 3], (middlex * 0.40, middley * 1.70))
menu_small = Spriter("menu/options/small_scr.png", [1, 3], (middlex * 0.7, middley * 1.4))
menu_medium = Spriter("menu/options/medium_scr.png", [1, 3], (middlex, middley * 1.4))
menu_large = Spriter("menu/options/large_scr.png", [1, 3], (middlex * 1.7, middley * 1.4))
menu[1].add(menu_back, menu_small, menu_medium, menu_large)

opt_icons = Spriter("menu/options/opt_icons.png", [3, 1], (middlex * 0.8, middley))
pointer1 = Spriter("menu/options/pointer1.png", [1, 2], (middlex * 0.7, middley * 0.2))
pointer2 = Spriter("menu/options/pointer2.png", [1, 2], (middlex * 1.0, middley * 0.2))
pointer3 = Spriter("menu/options/pointer3.png", [1, 2], (middlex * 1.3, middley * 0.2))
pointer4 = Spriter("menu/options/pointer4.png", [1, 2], (middlex * 1.6, middley * 0.2))

vol0 = Spriter("menu/options/vol0.png", [1, 2], (middlex * 0.7, middley * 0.6))
vol1 = Spriter("menu/options/vol1.png", [1, 2], (middlex * 1.2, middley * 0.6))

music0 = Spriter("menu/options/music0.png", [1, 2], (middlex * 0.7, middley))
music1 = Spriter("menu/options/music1.png", [1, 2], (middlex * 1.2, middley))
menu[1].add(pointer1, pointer2, pointer3, pointer4, music0, music1, vol0, vol1)

# screen effects
tempBlit = Surfaces("X", KEY, ScreenXY, middle)
fader = Surfaces("fade", BLACK, ScreenXY, middle)
counterlight = Surfaces("fade", BLACK, ScreenXY, middle)
fader2 = Surfaces("fade", BLACK, ScreenXY, middle)
screeneffects = pg.sprite.Group()
screeneffects.add(fader)

# effects
pointerLight = Spriter("spotlight2.png", [1, 1], (0, 0))
playerLight = Spriter("spotlight2.png", [1, 1], (0, 0))
pointer = Spriter("menu/pointer.png", [1, 4], (0, 0))
tst2 = False
RGB = [101, 100, 111]

'var             \' '
global sala, area, keep
keep = "sala", "area", "keep"

InOut = 0

click = False
#temp
temp = 255
temp2 = False
temp4 = ""
temp = False

temp3 = False
clickset = 0

#area
menu_area = False
mapgen_area = False
play_area = False
pause_area = False
fullout = False

intro_area = True
# menu_area = True
# mapgen_area = True
# play_area = True
# pause_area = True
level = []
alltiles = []

Active = True
area = intro_Area
while Active:

    clickset = False
    keypress = False
    mx, my = pg.mouse.get_pos()
    mx /= upscale
    my /= upscale
    RGB=[255,mx,my]
    pointer.update((mx, my))
    clock.tick(FPS)
    pg.display.set_caption(str(round(clock.get_fps())))
    for event in pg.event.get():
        if event.type == pg.QUIT: Active = False

        if event.type == pg.MOUSEMOTION: pass
        if event.type == pg.MOUSEBUTTONDOWN: click = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                click = False
                clickset = True

        if event.type == pg.KEYDOWN:
            keypress = True
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

            if event.key == pg.K_ESCAPE:
                pause_area = True
                tempscreen.image.blit(screen.image, (0, 0))

            if event.key == pg.K_SPACE:
                corak.focus = True
                corak.cantGo = ["x"]

            if event.key == pg.K_EQUALS:
                for a in sala: print(a)
                temp2 = True if not temp2 else False

                print(corak.at, map_at, level[map_at[1]][map_at[0]])

            if event.key == (pg.K_BACKSPACE):
                if FPS < 70:
                    FPS = 1000
                else:
                    FPS = 60

    InOut = area(InOut)

    tst = pg.transform.scale(screen.image, (FScreenX, FScreenY))
    toBlit.blit(tst, (0, 0))
    pg.display.update()

    if InOut == 0: InOut += 1
    elif InOut >= 2:

        if InOut == 2:
            InOut = 0
            area = intro_Area

        elif InOut == 3:
            InOut = 0
            area = menu_Area

        elif InOut == 10:
            InOut = 0
            area = play_Area

        elif InOut == 50:
            InOut = 0
            area = mapgen_Area


        elif InOut >= 100:
            area = end_Area

        print(globals())
        temp = globals()
        while len(tempkeep) > 0:
            if tempkeep[0] in temp:
                del temp[tempkeep[0]]
                tempkeep.remove(tempkeep[0])
        del tempkeep
        print(globals())

while Active:
    ''
    'reset'
    clickset = False
    keypress = False

    mx, my = pg.mouse.get_pos()
    mx /= upscale
    my /= upscale
    pointer.update((mx, my))
    clock.tick(FPS)
    pg.display.set_caption(str(round(clock.get_fps())))
    for event in pg.event.get():
        if event.type == pg.QUIT: Active = False

        if event.type == pg.MOUSEMOTION: pass
        if event.type == pg.MOUSEBUTTONDOWN: click = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                click = False
                clickset = True

        if event.type == pg.KEYDOWN:
            keypress = True
            if play_area:
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

            if event.key == pg.K_ESCAPE:
                pause_area = True
                tempscreen.image.blit(screen.image, (0, 0))

            if event.key == pg.K_SPACE:
                corak.focus = True
                corak.cantGo = ["x"]

            if event.key == pg.K_EQUALS:
                for a in sala: print(a)
                temp2 = True if not temp2 else False

                print(corak.at, map_at, level[map_at[1]][map_at[0]])

            if event.key == (pg.K_BACKSPACE):
                if FPS < 70:
                    FPS = 1000
                else:
                    FPS = 60

    if mixerOn[0]:
        if mixerOn[1]:
            # kp
              # strt
            if trigger[0][0]:
                if vol[0] <= 0.7:
                    vol[0] += 0.002
                    pg.mixer.music.set_volume((vol[0]/10) * Mvol)
                else: trigger[0][0] = False
              # end
            if trigger[0][1]:
                if vol[0] > 0.0:
                    vol[0] -= 0.005
                    pg.mixer.music.set_volume((vol[0]/10) * Mvol)
                if vol[0] <= 0.01:
                    trigger[0][1] = False
            # piano
              # strt
            if trigger[1][0]:
                if vol[1] <= 0.9:
                    vol[1] += 0.01
                    Piano.set_volume((vol[1]/10) * Mvol)
                else: trigger[1][0] = False
              # end
            if trigger[1][1]:
                if vol[1] > 0.0:
                    vol[1] -= 0.005
                    Piano.set_volume((vol[1]/10) * Mvol)
                if vol[1] <= 0.01: trigger[1][1] = False
            #
              # strt
            if trigger[2][0]:
                if vol[2] <= 0.8:
                    vol[2] += 0.001
                    mLoop.set_volume((vol[2]/10) * Mvol)
                else: trigger[2][0] = False
              # end
            if trigger[2][1]:
                if vol[2] > 0.0:
                    vol[2] -= 0.005
                    mLoop.set_volume((vol[2]/10) * Mvol)
                if vol[2] <= 0.01: trigger[2][1] = False
        if mixerOn[2]:
            # select
            if menuTrigger[0][1]:
                select.stop()
                select.play(0)
                menuTrigger[0][1] = False
            # click
            if menuTrigger[1][1]:
                clicks.stop()
                clicks.play(0)
                menuTrigger[1][1] = False
            # click set
            if menuTrigger[2][1]:
                click2.stop()
                click2.play(0)
                menuTrigger[2][1] = False
        if mixerOn[3]:
            trigger[0][1] = True
            trigger[1][1] = True
            trigger[2][1] = True
            mixerOn[3] = False
        if mixerOn[4][0]:
            if not trigger[0][1] and not trigger[1][1] and not trigger[2][1]:

                Piano.stop()
                mLoop.stop()
                pg.mixer.music.stop()

                pg.mixer.quit()
                pg.mixer.pre_init(22100, 16, 2)
                pg.mixer.init()

                pg.mixer.music.load("../Sound/kpLoop.wav")

                pg.mixer.music.set_volume(0)
                Piano.set_volume(0)
                mLoop.set_volume(0)

                Piano.play(-1)
                mLoop.play(-1)
                pg.mixer.music.play(-1)

                mixerOn[4][0] = False
        if mixerOn[5][0]:
            if not mixerOn[3]:
                if not trigger[0][1] and not trigger[1][1] and not trigger[2][1]:
                    if mixerOn[5][1]: trigger[0][0] = True
                    if mixerOn[5][2]: trigger[1][0] = True
                    if mixerOn[5][3]: trigger[2][0] = True
                    mixerOn[5][0] = False

    if play_area:
        'in out'
        if intro >= 0:
            if intro >= 1:
                sala, offsets, size, tiles_breakable, background, tiles_draw, tiles_base = changeRoom(map_at, level)
                moveLight = 1

                if intro >= 4:
                    background.image.fill(BLACK)
                    tiles_draw.image.fill(WHITE2)
                    tiles_draw.image.blit(tiles_base.image, (0, 0))
                    tiles_draw.image.set_colorkey(WHITE2)

                    if intro == 4: corak = Corak()
                    corak.get_at("S")
                    corak.checkMap()
                    if map_at[0] >= 4:
                        intro = 1

                elif intro == 1:
                    background.image.fill(CUSTOM2)
                    tiles_draw.image.fill(CUSTOM)
                    tiles_draw.image.blit(tiles_base.image, (0, 0))
                    tiles_draw.image.set_colorkey(CUSTOM)

                    corak = Corak()
                    map_at = hall([0, 0, "get_pos_strt"], level)
                    corak.get_at("S")
                    corak.checkMap()
                    intro = -1

                elif intro == 2:
                    background.image.fill(CUSTOM3)
                    tiles_draw.image.fill(CUSTOM)
                    tiles_draw.image.blit(tiles_base.image, (0, 0))
                    tiles_draw.image.set_colorkey(CUSTOM)
                    corak.get_at(temp4)
                elif intro == 3:
                    corak.get_at("0")

                # scale
                corak.modLight[1] = (size * int(upscale * 2.5)) * corak.modLight[0]
                corak.sprite.image = pg.transform.scale(corak.sprite.image, (size, size))
                pointerLight.image = pg.transform.scale(playerLight.image, (corak.modLight[1], corak.modLight[1]))
                playerLight.image = pg.transform.scale(playerLight.image, (corak.modLight[1], corak.modLight[1]))

                if "mod-" in level[map_at[1]][map_at[0]]:

                    background.image.fill(CUSTOM2)
                    tiles_draw.image.fill(CRED)
                    tiles_draw.image.blit(tiles_base.image, (0, 0))
                    tiles_draw.image.set_colorkey(CRED)

                print(corak.at, map_at, level[map_at[1]][map_at[0]])

                intro = 0
                corak.Do = [0, 0, "Z"]
            fade_count -= 1
            if fade_count <= 0: intro = -1
            fader.image.set_alpha(fade_count)
        if out >= 0:

            fade_count += 7
            if fade_count >= 250:
                if out == 1: intro = 1
                if out == 2: intro = 2
                if out == 3: intro = 3
                if out == 4: intro = 4

                if out == 5: intro = 5
                out = -1
            fader.image.set_alpha(fade_count)

        if pause_area:
            menuCount = 0
            if clickset == 1: clickset = 0

            screen.image.blit(tempscreen.image, (0, 0))
            'input'
            for button in menu[0]:
                screen.image.blit(button.image, button.rect)
                if button.rect.collidepoint(pointer.rect.center):
                    button.setFrame([0, 1])
                    if click:
                        if not menuTrigger[1][0]:
                            menuTrigger[1][0] = True
                            menuTrigger[1][1] = True
                        fade = True
                        temp3 = False
                        button.setFrame([0, 2])
                    if clickset == 1:
                        clickset = 2
                        if "start" in button.type:
                            if not menuTrigger[2][0]:
                                menuTrigger[2][0] = True
                                menuTrigger[2][1] = True
                            intro = 3
                            out = 3
                        if "options" in button.type:
                            menuTrigger[1][0] = False
                            trigger[2] = True
                            pointer.setFrame([0, pointer.frame[1] + 1])
                        if "exit" in button.type:
                            out = 0
                            temp2 = True
                    if not menuTrigger[0][0]:
                        menuTrigger[0][0] = True
                        menuTrigger[0][1] = True

                    menuCount += 1

                else:
                    button.setFrame([0, 0])

            if menuCount == 0:
                menuTrigger[0][0], menuTrigger[2][0] = False, False

            screen.image.blit(pointer.image, pointer.rect.center)
        else:
            if clickset:
                tiles_draw.image.fill(GRAY)
                tiles_draw.image.blit(tiles_base.image, (0, 0))
                tiles_draw.image.set_colorkey(GRAY)
            if click: background.image.fill((20, 10, 10))

            if keypress:
                corak.update(corak.Do)
                map_at, out, temp4 = CheckLevel(map_at)

            corak.posoffset()
            'frame'
            # air
            if corak.air:
                frame += 1
                if frame > 1: frame = 0
                corak.sprite.setFrame([2, frame])
            # grab
            if corak.grab:
                frame += 1
                if frame > 1: frame = 0
                corak.sprite.setFrame([1, frame])
            # jump
            if "U" in corak.Do[2]:
                frame += 1
                if frame > 3: frame = 0
                corak.sprite.setFrame([3, frame])
            # ground
            elif not corak.air:
                frame = 1
                corak.sprite.setFrame([0, frame])
            # focus
            if corak.focus:
                frame = 0
                corak.sprite.setFrame([4, frame])
            # dash
            if not corak.at[0] * size - 0.01 < corak.pos_offsetX < corak.at[0] * size + 0.01:
                frame = 1
                corak.sprite.setFrame([4, frame])
            # air
            if not corak.at[1] * size - 0.02 < corak.pos_offsetY:
                frame = +1
                if frame > 1: frame = 0
                corak.sprite.setFrame([2, frame])
            if corak.left or corak.Do[0] == -1: corak.sprite.image = pg.transform.flip(corak.sprite.image, True, False)

            'draw'
            screen.image.fill(BLACK)
            screen.image.blit(background.image, background.rect)
            # tiles.draw(screen.image)
            screen.image.blit(tiles_draw.image, tiles_draw.rect)

            screen.image.blit(corak.sprite.image, corak.sprite.rect)
            # screen.image.blit(tiles_deco.image, tiles_deco.rect)

            tiles_breakable.draw(screen.image)
            if temp2:
                fader2.image.set_alpha(fade_count)
                counterlight.image.fill(BLACK)

                pointerLight.update((mx, my))
                counterlight.image.blit(pointerLight.image, pointerLight.rect)

                playerLight.update(corak.sprite.rect.center)
                counterlight.image.blit(playerLight.image, playerLight.rect)

                counterlight.image.set_alpha(moveLight)

                fader2.image.fill(BLACK)
                fader2.image.set_alpha(moveLight)

                screen.image.blit(counterlight.image, (0, 0), special_flags=pg.BLEND_MULT)
                screen.image.blit(fader2.image, (0, 0))
            if temp2: screen.image.blit(pointer.image, pointer.rect.center)

            if moveLight < 150:
                moveLight += 1.5

        screeneffects.draw(screen.image)

    tst = pg.transform.scale(screen.image, (FScreenX, FScreenY))
    toBlit.blit(tst, (0, 0))
    pg.display.update()

pg.quit()

'''temp \\\\\\'''

'''
if moveLight > 0:
moveLight -= 6

else:
corak.Do = [0, 0, "Z"]

corak.update(corak.Do)

map_at, out, temp4 = CheckLevel(map_at)
'''

''' 
from \
play area \
light size \

if corak.sprite.rect.collidepoint(pointer.rect.center):
    temp22 = int(corak.modLight[1] * 1.4)
else:
    temp22 = corak.modLight[1]

playerLight.image = pg.transform.scale(playerLight.image, (temp22, temp22))
'''

'''
pointerLight.update(pg.mouse.get_pos())
        playerLight.update((player1.rect.x+(size/2), player1.rect.y+(size/2)))

        counterlight.image.fill(BLACK)
        counterlight.image.blit(pointerLight.image, pointerLight.rect)
        counterlight.image.blit(playerLight.image, playerLight.rect)

'''
