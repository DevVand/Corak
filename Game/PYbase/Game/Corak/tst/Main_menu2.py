import pygame as pg
from Game.Corak.dicio import *
from Game.Corak.Worldgen3 import hall
from Game.Corak.mapcr import printmap
from Game.Corak.mapread4 import mapread, generatenew

class Corak(pg.sprite.Sprite):
    def __init__(S):
        S.sprite = pg.Surface([size, size])
        S.sprite.fill(WHITE)
        S.left = False
        S.sprite = Spriter("corak full.png", [7, 7], (0, 0))
        S.at = [1, 11]
        S.pos = [size * S.at[0] + offsets[0], size * S.at[1] + offsets[1], 0]

        S.pos_offsetX = S.at[0]
        S.pos_offsetY = S.at[1]


        S.Do = []
        S.turn = True
        S.jump = False
        S.air = False
        S.focus = False
        S.grab = False
        S.modLight = [0, 0]
        S.modLight[0] = 1
        S.modLight[1] = 0
        S.modfocus = False
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
        print(S.cantGo)
        S.Move([0, 0, "x"])
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
                    print("focus")
                if S.grab: S.grab = False
        except: pass
        S.turn = False
        S.checkMap()
    def update(S, Do):
        if Do[2] in "LRUDx": S.Move(Do)
        if Do[2] in "H": S.Hit(Do[0], S.at)
        if Do[2] in "X": S.Focus()
    def posoffset(S):
        if S.at[0] != S.pos_offsetX:
            S.pos_offsetX = abs((S.pos_offsetX + S.at[0])) / 2
        if S.at[1] != S.pos_offsetY:
            S.pos_offsetY = abs((S.pos_offsetY + S.at[1])) / 2
        S.sprite.update([int(size * S.pos_offsetX) + offsets[0], int(size * S.pos_offsetY) + offsets[1]])

class Spriter(pg.sprite.Sprite):
    def __init__(s, type, frames, pos):
        pg.sprite.Sprite.__init__(s)
        temp = "../Sprites/"+type

        if frames[1] > 1:
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

        s.image = pg.Surface(size)
        s.image.fill(colour)
        s.rect = s.image.get_rect()
        s.rect.x = at[0]
        s.rect.y = at[1]
        Surfaces.Do(s, type)
    def Do(s, type):
        if "fade" in type:
            s.image.set_alpha(0)

def changeRoom(map_at, level):
    #print("changeroom")
    txt = "../Salas/" + level[map_at[1]][map_at[0]]

    #print("txt", txt)
    sala = openSala(txt)

    #print("sala", sala)
    tiles_breakable, background, tiles_draw, tiles_base = mapread(sala)

    #print("tiles", tiles)
    size = getSize(sala)

   # print("size", size)
    offsets = getOffset(sala, size, "sala")
    return sala, offsets, size, tiles_breakable, background, tiles_draw, tiles_base

def CheckLevel(mapAt):
    out = -1
    come_from = ""
    if corak.at[0] < 0:
        mapAt[0] += L
        come_from = "R"
        out = 1
    elif corak.at[0] >= len(sala[0]):
        mapAt[0] += R
        come_from = "L"
        out = 1
    elif corak.at[1] < 0:
        mapAt[1] += U
        come_from = "D"
        out = 1
    elif corak.at[1] >= len(sala):
        mapAt[1] += D
        come_from = "U"
        out = 1
    else: corak.checkMap()
    return mapAt, out, come_from


    screeneffects.draw(screen)
    screen.blit(pointer.image, pointer.rect.center)

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
          [False, True, 0]
          ]
pg.mixer.pre_init(44200, 16, 2)

pg.mixer.init()
#music1 = pg.mixer.Sound("../Sound/kpLoop.wav")
vol = []

trigger = []
pg.mixer.music.load("../../Sound/kpLoop.wav")
trigger.append([True, False])

Piano = pg.mixer.Sound("../Sound/pianoLoop.wav")
Piano.set_volume(0)
vol.append(0.0)
trigger.append(False)

mLoop = pg.mixer.Sound("../Sound/mLoop.wav")
mLoop.set_volume(0)
vol.append(0.0)
trigger.append(False)
trigger.append(False)

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

Mvol = 0.0
menuCount = 0

'sprite setting  \' '
# menu intro
menu_logo = Spriter("menu/intro/logo.png", [1, 1], (middlex, middley))
#menu_logo.image = pg.transform.scale(menu_logo.image, menu_logo.rect.x)
menu_click = Spriter("menu/intro/click.png", [1, 1], (middlex, middley * 1.3))

# menu
menu = []
menu.append(pg.sprite.Group())
menu_strt = Spriter("menu/start.png", [1, 3], (middlex, middley * 0.5))
menu_opt = Spriter("menu/options.png", [1, 3], middle)
menu_quit = Spriter("menu/exit.png", [1, 3], (middlex, middley * 1.5))
menu[0].add(menu_strt, menu_opt, menu_quit)

menu.append(pg.sprite.Group())

# screen effects
fader = Surfaces("fade", BLACK, ScreenXY, (0, 0))
counterlight = Surfaces("fade", BLACK, ScreenXY, (0, 0))
fader2 = Surfaces("fade", BLACK, ScreenXY, (0, 0))
screeneffects = pg.sprite.Group()
screeneffects.add(fader)

# effects
pointerLight = Spriter("spotlight2.png", [1, 1], (0, 0))
playerLight = Spriter("spotlight2.png", [1, 1], (0, 0))
pointer = Spriter("menu/pointer.png", [1, 4], (0, 0))
tst2 = False
RGB = [101, 100, 111]


'var             \' '
global sala
click = False

fade_count = 255

intro = 0
out = -1

temp = 255
temp2 = False
temp4 = ""
temp = False

temp3 = False
clickset = 0

intro_area = False
menu_area = False
mapgen_area = False
play_area = False
pause_area = False

intro_area = True
# menu_area = True
# mapgen_area = True
# play_area = True
# pause_area = True
level = []
alltiles = []

final_effects = False

Active = True
while Active:
    ''
    mx, my = pg.mouse.get_pos()
    mx /= upscale
    my /= upscale
    pointer.update((mx, my))
    clock.tick(FPS)
    pg.display.set_caption(str(round(clock.get_fps())))

    if mixerOn[0]:
        if mixerOn[1]:
            if trigger[0][0]: #kp strt
                if not trigger[0][1]: #kp end strt
                    if Mvol <= 0.7:
                        Mvol += 0.001
                        pg.mixer.music.set_volume(Mvol)
                elif Mvol > 0.0: ## kp end
                    Mvol -= 0.005
                    pg.mixer.music.set_volume(Mvol)
                else: trigger[0][0] = False
            if trigger[1]: #piano
                if vol[0] <= 0.5:
                    vol[0] += 0.005
                    Piano.set_volume(vol[0])
            if trigger[2]:
                if vol[1] <= 0.4:
                    vol[1] += 0.01
                    mLoop.set_volume(vol[1])
        if mixerOn[2]:
            if menuTrigger[0][1]:
                select.stop()
                select.play(0)
                menuTrigger[0][1] = False
            if menuTrigger[1][1]:
                clicks.stop()
                clicks.play(0)
                menuTrigger[1][1] = False
            if menuTrigger[2][1]:
                click2.stop()
                click2.play(0)
                menuTrigger[2][1] = False
        if mixerOn[3][0]:
            pg.mixer.quit()
            pg.mixer.pre_init(mixerOn[3][1], 16, 2)
            pg.mixer.init()

            Piano.stop()
            mLoop.stop()
            pg.mixer.music.stop()

            Piano.play(-1)
            mLoop.play(-1)

            pg.mixer.music.load("../../Sound/kpLoop.wav")
            pg.mixer.music.play(-1)

            mixerOn[3][0] = False
    if intro_area:
        if intro == 0: #fadei in
            fade_count -= 2
            if fade_count <= 0: #set fade
                intro = -1
                pointerLight.image = pg.transform.scale(playerLight.image, (16*upscale*2, 16*upscale*2))
            fader.image.set_alpha(fade_count)

        #loop
        if temp <= 50: temp3 = True
        if temp >= 255: temp3 = False
        if temp3: temp += 8
        else: temp -= 8
        menu_click.image.set_alpha(temp)

        if out >= 0:
            if out == 1: #fade out
                fade_count += 20
                if fade_count >= 255: out += 1 #set out
            elif out == 2:
                fade_count -= 10
                if fade_count <= -100:
                    out += 1
            elif out >= 3:
                fade_count += 4
                if fade_count >= 400:
                    intro = 0
                    intro_area = False
                    menu_area = True
                    out = -1
            fader.image.set_alpha(fade_count)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                Active = False
            if event.type == pg.MOUSEBUTTONDOWN:
                intro = -1
                out += 2
                trigger[1] = True

            elif event.type == pg.KEYDOWN:
                if event.key == (pg.K_BACKSPACE):
                    if FPS < 70:
                        FPS = 1000
                    else: FPS = 60
        'draw'
        screen.image.fill(BLACK)

        screen.image.blit(menu_click.image, menu_click.rect)
        screen.image.blit(menu_logo.image, menu_logo.rect)
        screeneffects.draw(screen.image)

        pointerLight.update((mx, my))
        counterlight.image.blit(pointerLight.image, pointerLight.rect)
        screen.image.blit(counterlight.image, (0, 0), special_flags=pg.BLEND_MULT)
    if menu_area:
        temp
        if intro == 0 :
            fade_count -= 2
            if fade_count <= 0:
                intro = -1
            fader.image.set_alpha(fade_count)
        if out >= 0:
            fade_count += 15
            if fade_count >= 400:
                intro = 0
                out = -1
                menu_area = False
                mapgen_area = True
                trigger[0][1] = True
                if temp2: Active = False
        'reset'
        menuCount = 0
        if clickset == 1: clickset = 0

        'draw'
        screen.image.fill(CUSTOM)
        for button in menu[0]: screen.image.blit(button.image, button.rect)
        screeneffects.draw(screen.image)

        'inputs'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Active = False
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
                    Active = False
                elif event.key == (pg.K_BACKSPACE):
                    if FPS < 70:
                        FPS = 1000
                    else: FPS = 60
        for button in menu[0]:
            if button.rect.collidepoint(pointer.rect.center):
                button.setFrame([0, 1])
                if click:
                    if not menuTrigger[1][0]:
                        menuTrigger[1][0] = True
                        menuTrigger[1][1] = True

                    temp = True
                    temp3 = False
                    button.setFrame([0, 2])
                if clickset == 1:
                    clickset = 2
                    if "start" in button.type:
                        if not menuTrigger[2][0]:
                            menuTrigger[2][0] = True
                            menuTrigger[2][1] = True
                        out = 0
                    if "options" in button.type:
                        menuTrigger[1][0] = False
                        trigger[2] = True
                        pointer.setFrame([0,  pointer.frame[1] + 1])

                        mixerOn[3][0] = True
                        mixerOn[3][1] = 22100
                    if "exit" in button.type:

                        menuTrigger[1][0] = False
                        mixerOn[3][0] = True
                        mixerOn[3][1] = 88400
                        #out = 0
                        #temp2 = True
                if not menuTrigger[0][0]:
                    menuTrigger[0][0] = True
                    menuTrigger[0][1] = True

                menuCount += 1

            else: button.setFrame([0, 0])

        if menuCount == 0:
            menuTrigger[0][0], menuTrigger[2][0] = False, False


        if temp:
            if fade_count < 50:
               fade_count += 4
               fader.image.set_alpha(fade_count)
        if not temp:
            if fade_count >= 0:
                fade_count -= 8
                fader.image.set_alpha(fade_count)

        screen.image.blit(pointer.image, pointer.rect.center)
    if mapgen_area:
        if intro == 0:
            level = hall([0, 0, "strt"], level)
            fade_count -= 5
            fader.image.set_alpha(fade_count)
            if len(level) > 5:
                temp = True
                if fade_count <= 0:
                    intro = -1
                    out = 0
        if out >= 0:
            fade_count += 2
            fader.image.set_alpha(fade_count)
            if fade_count >= 50:
                out = -1
                intro = 1
                map_at = hall([0, 0, "get_pos_strt"], level)
                mapgen_area = False
                play_area = True
                temp2 = False
        'inputs'
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Active = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                elif event.button == 3:
                    print(1)
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False
                    clickset = 1

        'draw'
        screen.image.fill(BLACK)
        screeneffects.draw(screen.image)
        screen.image.blit(pointer.image, pointer.rect.center)
    if play_area:
        if intro >= 0:
            if intro >= 1:
                sala, offsets, size, tiles_breakable, background, tiles_draw, tiles_base = changeRoom(map_at, level)

                moveLight = 1
                if intro == 1:
                    corak = Corak()
                    corak.get_at("S")
                    corak.checkMap()
                    intro = -1
                elif intro == 2: corak.get_at(temp4)
                elif intro == 3: corak.get_at("0")


                # scale
                corak.modLight[1] = (size * int(upscale * 2.5)) * corak.modLight[0]
                corak.sprite.image = pg.transform.scale(corak.sprite.image, (size, size))
                pointerLight.image = pg.transform.scale(playerLight.image, (corak.modLight[1], corak.modLight[1]))
                playerLight.image = pg.transform.scale(playerLight.image, (corak.modLight[1], corak.modLight[1]))

                background.image.fill((20, 10, 10))
                tiles_draw.image.fill(CRED)
                tiles_draw.image.blit(tiles_base.image, (0, 0))
                tiles_draw.image.set_colorkey(CRED)

                intro = 0
                corak.Do = [0, 0, "Z"]
            fade_count -= 2
            if fade_count <= 0: intro = -1
            fader.image.set_alpha(fade_count)
        if out >= 0:
            fade_count += 15
            if fade_count >= 250:
                intro = 2
                if out == 3: intro = 3
                out = -1
            fader.image.set_alpha(fade_count)
        if pause_area:
            menuCount = 0
            if clickset == 1: clickset = 0

            screen.image.blit(tempscreen.image, (0, 0))
            'input'
            for event in pg.event.get():
                if event.type == pg.QUIT: Active = False
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
                    if event.key == (pg.K_w or pg.K_UP):
                        corak.Do = [0, -1, "U"]
                    elif event.key == (pg.K_BACKSPACE):
                        if FPS < 70:
                            FPS = 1000
                        else: FPS = 60
                    elif event.key == pg.K_EQUALS:
                        print(corak.at, map_at, level[map_at[1]][map_at[0]])
                        for a in sala: print(a)
                        print(temp2, temp4)
                        print(corak.cantGo)

                    elif event.key == pg.K_ESCAPE:
                        pause_area = False

                        screen.image.set_alpha(255)

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

                else: button.setFrame([0, 0])

            if menuCount == 0:
                menuTrigger[0][0], menuTrigger[2][0] = False, False


            screen.image.blit(pointer.image, pointer.rect.center)
        else:
            'inputs'
            for event in pg.event.get():
                if event.type == pg.QUIT: Active = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    print(1)

                if event.type == pg.MOUSEBUTTONUP:

                    tiles_draw.image.fill(GRAY)
                    tiles_draw.image.blit(tiles_base.image, (0, 0))
                    tiles_draw.image.set_colorkey(GRAY)

                elif event.type == pg.MOUSEMOTION:
                    if moveLight > 0:
                        moveLight -= 6

                elif event.type == pg.KEYDOWN:
                    if event.key == (pg.K_w or pg.K_UP): corak.Do = [0, -1, "U"]
                    elif event.key == (pg.K_a or pg.K_LEFT): corak.Do = [-1, 0, "L"]
                    elif event.key == (pg.K_d or pg.K_RIGHT): corak.Do = [1, 0, "R"]
                    elif event.key == (pg.K_s or pg.K_DOWN): corak.Do = [0, 0, "X"]
                    elif event.key == (pg.K_z or pg.K_q): corak.Do = [-1, 0, "H"]
                    elif event.key == (pg.K_x or pg.K_e): corak.Do = [1, 0, "H"]
                    elif event.key == (pg.K_BACKSPACE):
                        if FPS < 70:
                            FPS = 1000
                        else: FPS = 60
                        break
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
                    elif event.key == pg.K_ESCAPE:
                        pause_area = True
                        tempscreen.image.blit(screen.image, (0, 0))
                        break
                    else:
                        corak.Do = [0, 0, "Z"]

                    corak.update(corak.Do)

                    map_at, out, temp4 = CheckLevel(map_at)

            'frame'
            if corak.air: # air
                frame += 1
                if frame > 1: frame = 0
                corak.sprite.setFrame([2, frame])
            if corak.grab: # grab
                frame += 1
                if frame > 1: frame = 0
                corak.sprite.setFrame([1, frame])
            if "U" in corak.Do[2]: # jump
                frame += 1
                if frame > 3: frame = 0
                corak.sprite.setFrame([3, frame])
            elif not corak.air: # ground
                frame = 1
                corak.sprite.setFrame([0, frame])
            if corak.focus: # focus
                frame = 1
                corak.sprite.setFrame([4, frame])
            if corak.left or corak.Do[2] in "ZX": corak.sprite.image = pg.transform.flip(corak.sprite.image, True, False)
            else: corak.sprite.image = pg.transform.flip(corak.sprite.image, False, False)

            corak.posoffset()

            'draw'
            screen.image.fill(BLACK)
            screen.image.blit(background.image, background.rect)
            #tiles.draw(screen.image)
            screen.image.blit(tiles_draw.image, tiles_draw.rect)

            screen.image.blit(corak.sprite.image, corak.sprite.rect)
            #screen.image.blit(tiles_deco.image, tiles_deco.rect)

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
            else: screen.image.blit(pointer.image, pointer.rect.center)

            if moveLight < 150:
                moveLight += 1

        screeneffects.draw(screen.image)

    tst = pg.transform.scale(screen.image, (FScreenX, FScreenY))

    toBlit.blit(tst, (0, 0))

    pg.display.update()
'''
pointerLight.update(pg.mouse.get_pos())
        playerLight.update((player1.rect.x+(size/2), player1.rect.y+(size/2)))

        counterlight.image.fill(BLACK)
        counterlight.image.blit(pointerLight.image, pointerLight.rect)
        counterlight.image.blit(playerLight.image, playerLight.rect)

'''
pg.quit()

'''temp \\\\\\'''
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
