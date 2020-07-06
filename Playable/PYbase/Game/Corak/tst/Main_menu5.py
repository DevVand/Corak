from Game.Corak.mapread4 import *
#from Corak.Worldgen3 import maphall

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

    def CheckLevel(S, at):
        if -1 >= at[0]:
            print("levelleft")
            maphall([-1, ])
        elif len(sala[0]) == at[0]:
            print("levelright")
        elif -1 >= at[1]:
            print("levelup")
        elif len(sala) == at[1]:
            print("leveldown")
        else: S.checkMap(at)
    def checkMap(S, at):
        S.cantGo = []
        print(S.focus)
        if S.focus: distance = 2
        else: distance = 1
        for i in range(1, distance+1):
            try:
                if sala[at[1]][at[0] + i] in "12":
                    S.cantGo.extend(["R", i * "R"])
            except: pass
            try:
                if at[0] - 1 >= 0:
                    if sala[at[1]][at[0] - i] in "12":
                        print("a")
                        S.cantGo.extend(["L", i * "L"])
            except:
                pass
            try:
                if sala[at[1] + 1][at[0]] in "123":
                    S.cantGo.append("D")
            except: pass
            try:
                if at[1] - 1 >= 0:
                    if sala[at[1] - i][at[0]] in "123":
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
        print(S.turn, S.air)
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
            if str(sala[at[1]][at[0] + direction]) in "2":
                sala[at[1]] = sala[at[1]][:at[0]+direction:] + "0" + sala[at[1]][-(len(sala[at[1]])-1 - (direction + at[0]))::]
                for tile in tiles2:
                    if tile.at == [at[0] + direction, at[1]]:
                        tiles2.remove(tile)
                if S.focus:
                    S.focus = False
                    print("focus")
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
    def __init__(s, type, size, at):
        pg.sprite.Sprite.__init__(s)
        if "png" not in type:
            s.image = pg.Surface(size)
            s.rect = s.image.get_rect()
            s.rect.x = at[0]
            s.rect.y = at[1]
            if type == 0: s.image.fill(BLACK)
            if type == 1: s.image.fill(GRAY)
        else:
            s.image = pg.image.load(type).convert()
            s.rx, s.ry = Spriter.getNewSize(s)

            s.image = pg.transform.scale(s.image, (s.rx * size, s.ry * size))
            s.rx, s.ry = Spriter.getNewSize(s)
            s.at = at

            print(s.rect)
    def sizearrange(self, size):

        s.image = pg.image.load(type).convert()
        self.rect = self.image.get_rect()
        rx = self.rect[2]
        ry = self.rect[3]
        return rx, ry


def init():
    screen = pg.display.set_mode((ScreenX, ScreenY), 0)
    clock = pg.time.Clock()
    mopen = False
    temp = 1
    tab1 = Spriter("1", (150, 350), [ScreenX / 2, ScreenY / 2])

    pg.mouse.set_visible(False)
    menukeys = pg.sprite.Group()
    menu_strt = Spriter("menu.png", generalsize, [ScreenX / 2, ScreenY / 2])

    pointer = Spriter("pointer.png", generalsize, 0)
    menukeys.add(menu_strt)
    '''
    SpriteGroup = pg.sprite.Group()
    SpriteGroup.add(tab1)
    SpriteGroup.add(menu_strt)
    '''
    selected = [0, 0, 0, 0, 0]
    temp2 = 0
    while True:
        clock.tick(FPS)
        mx, my = pg.mouse.get_pos()
        pg.display.set_caption(str(round(clock.get_fps())))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("temp2", temp2)
                    if temp2 == 2: temp2 = 0
                    else: temp2 += 1
                    click = [mx, my]
                elif event.button == 3:
                    print(1)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    pg.quit()

            #pygame.sprite.collide_rect()



        screen.fill(CUSTOM)

        #menukeys.draw(screen)
        screen.blit(menu_strt.image, middle, (menu_strt.rx / 3 * selected[0], 0, menu_strt.rx / 3, menu_strt.ry))

        screen.blit(pointer.image, [mx, my])


        pg.display.update()

init()

txt = "LRUDX.txt"
sala = openSala(txt)
tiles = mapread(sala)
tiles2 = pg.sprite.Group()
size = getSize(sala)
offsets = getOffset(sala, size)
player1 = Corak()
print(tiles)

'''
left = False
right = False
b = 10
a = 0
c = 0
    
    if left and a > -max_speed:
        a -= aceeleration
    if right and a < max_speed:
        a += aceeleration
    if not left and not right:
        a = a/friction

    b = b+a
    c = c+gravity
    
'''

player1.update([0, 0, "Map"])

for tile in tiles:
    if tile.type == 2:
        tiles2.add(tile)
        tiles.remove(tile)

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                player1.Do = [0, -1, "U"]
                player1.update(player1.Do)

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player1.Do = [0, -1, "U"]

            elif event.key == pg.K_a:
                player1.Do = [-1, 0, "L"]
            elif event.key == pg.K_d:
                player1.Do = [1, 0, "R"]
            elif event.key == pg.K_s:
                player1.Do = [0, 0, "X"]
            elif event.key == pg.K_z:
                player1.Do = [-1, 0, "H"]
            elif event.key == pg.K_x:
                player1.Do = [1, 0, "H"]
            elif event.key == pg.K_UP:
                player1.Do = [0, -1, "U"]
            elif event.key == pg.K_LEFT:
                player1.Do = [-1, 0, "L"]
            elif event.key == pg.K_RIGHT:
                player1.Do = [1, 0, "R"]
            elif event.key == pg.K_DOWN:
                player1.Do = [0, 0, "X"]
            elif event.key == pg.K_r:
                while len(tiles2) > 0: del tiles2[0]
                
                
                tiles = mapread(sala)
                tiles2 = pg.sprite.Group()
                break
            elif event.key == pg.K_SPACE:
                player1.focus = True
                player1.cantGo = ["x"]
                break
            else:
                player1.Do = [0, 0, "Z"]
            player1.update(player1.Do)
    mx, my = pg.mouse.get_pos()

    pg.display.set_caption(str(round(clock.get_fps())))
    clock.tick(FPS)
    if temp < 50: temp *= 2
    else: temp = 1

    screen.fill(WHITE)
    tiles.draw(screen)
    tiles2.draw(screen)
    pg.draw.rect(screen, RED, [mx, my, temp, 5])
    #pg.draw.rect(screen, BLACK, [int(b), c, 10, 10])
    pg.draw.rect(screen, BLUE, [player1.pos[0], player1.pos[1], size, size])
    pg.display.flip()

pg.quit()
