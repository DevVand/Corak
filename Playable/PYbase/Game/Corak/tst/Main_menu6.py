from Game.Corak.mapread4 import *
#from Corak.Worldgen3 import maphall

class Spriter(pg.sprite.Sprite):
    def __init__(s, type, size, frames):
        pg.sprite.Sprite.__init__(s)

        s.frames = frames
        s.frame = 0
        s.Fullimage = pg.image.load(type).convert()
        s.rx, s.ry = s.Fullimage.get_size()
        #s.Fullimage = pygame.transform.scale2x(s.Fullimage)
        s.Fullimage = pg.transform.scale(s.Fullimage, (s.rx * upscale, s.ry * upscale))
        s.Fullimage_region = (s.ry* 1, 0, s.ry*1, s.rx)

        s.rx, s.ry = s.Fullimage.get_size()

        s.image = pg.Surface((s.rx / s.frames, s.ry), pygame.SRCALPHA)
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

def strt_menu():
    #display setting
    'display setting'
    screen = pg.display.set_mode((ScreenX, ScreenY), 0)
    clock = pg.time.Clock()
    pg.mouse.set_visible(False)

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

    'variable init'
    click = False
    fade = False
    temp = 0
    temp2 = 1
    clickset = 0
    while True:
        clock.tick(FPS)
        if clickset == 1: clickset = 0
        mx, my = pg.mouse.get_pos()

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
                temp += 12
                if temp >= 255:
                    fade = False
                    clickset = 0
            else:
                if temp >= 50:
                    fade = False
                else:
                    temp += 8

            fader.image.set_alpha(temp)
        if fade and clickset == 2:
            worldgen()
        pg.display.update()


def worldgen():
    print(1)

strt_menu()
