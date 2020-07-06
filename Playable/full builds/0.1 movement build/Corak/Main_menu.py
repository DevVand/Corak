import pygame
from Corak.dicio import *
from Corak.mapread4 import mapread

class Corak(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.at = [1, 11]
        self.pos = [size * self.at[0] + offsets[0], size * self.at[1] + offsets[1]]
        self.Do = []
        self.turn = True
        self.jump = False
        self.air = False
        self.focus = False
        self.grab = False

    def update(self, Do, turn):
        if turn:
            if Do[2] in "LRUD": self.Move(Do)
            if Do[2] in "H": self.Hit(Do[0], self.at, self.focus, self.air)
            if Do[2] in "X": self.Focus(self.focus, self.air)

    def Focus(self, focus, air):
        if not focus and not air:
            self.focus = True
        self.turn = False
        self.checkMap()

    def Hit(self, direction, at, focus, air):
        try:
            if str(sala[at[1]][at[0] + direction]) in "2":
                sala[at[1]] = sala[at[1]][:at[0] + direction:] + "0" + sala[at[1]][-(len(sala[at[1]]) - (direction + at[0] + 1))::]
                for tile in tiles2:
                    if tile.at == [at[0] + direction, at[1]]:
                        tiles2.remove(tile)

                if focus:
                    self.focus = False
                    print("focus")
                if air: self.air = False
        except:
            pass
        print("hit")
        self.turn = False
        self.checkMap()

    def CheckLevel(self, at):
        if -1 >= at[0]:
            print("levelleft")
        elif len(sala[0]) == at[0]:
            print("levelright")
        elif -1 >= at[1]:
            print("levelup")
        elif len(sala) == at[1]:
            print("leveldown")
        else: self.checkMap()

    def checkMap(self):
        self.cantGo = []
        if self.focus : distance = 2
        else : distance = 1
        for i in range(1, distance+1):
            try:
                if sala[self.at[1]][self.at[0] + i] in "12":
                    self.cantGo.extend(["R", i*"R"])
            except: pass
            try:
                if self.at[0] - 1 >= 0:
                    if sala[self.at[1]][self.at[0] - i] in "12":
                        print("a")
                        self.cantGo.extend(["L", i*"L"])
            except:
                pass
            try:
                if sala[self.at[1] + 1][self.at[0]] in "123":
                    self.cantGo.append("D")
            except: pass
            try:
                if self.at[1] - 1 >= 0:
                    if sala[self.at[1] - i][self.at[0]] in "123":
                        self.cantGo.extend(["U", i*"U"])
            except: pass
        self.checkMove()

    def checkMove(self):
        self.air = True
        if "D" in self.cantGo:
            self.air = False

        if self.turn:
            if self.air and not self.grab:
                self.cantGo.append("U")

        if not self.turn:
            if not any([self.jump, self.grab, self.focus]) and self.air:
                self.Do = [0, 1, "D"]
                self.jump = True
                self.Move(self.Do)

            if self.jump:
                self.jump = False

            self.turn = True
            self.checkMove()
        print(self.cantGo)

    def Move(self, Do):

        alltrue = True
        for direction in self.cantGo:
            if direction in Do[2]:
                alltrue = False
                if self.air and direction in "LR": self.grab = True, print("grab")
                if self.focus and direction in "LRU":
                    self.focus = False
                    alltrue = True

        if alltrue:
            if Do[1] == -1: self.jump = True, print("jump")
            if self.focus : Do[0] *= 2
            if self.focus : Do[1] *= 2
            self.focus = False
            self.grab = False

            self.at[0] = self.at[0] + Do[0]
            self.at[1] = self.at[1] + Do[1]
            self.pos[0] = size * self.at[0] + offsets[0]
            self.pos[1] = size * self.at[1] + offsets[1]

        Do = []
        self.turn = False
        self.CheckLevel(self.at)


screen = pygame.display.set_mode((ScreenX, ScreenY))

txt = "LRUDhallX.txt"
sala = openSala(txt)
tiles = mapread(sala)
tiles2 = pygame.sprite.Group()
size = getSize(sala)
offsets = getOffset(sala, size)

player1 = Corak()

print(tiles)

left = False
right = False
b = 10
a = 0
c = 0
player1.checkMap()

for tile in tiles:
    if tile.type == 2:
        tiles2.add(tile)
        tiles.remove(tile)
temp = 0
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player1.Do = [0, -1, "U"]
                player1.update(player1.Do, player1.turn)

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
                player1.turn = False
            elif event.key == pygame.K_SPACE:
                player1.focus = True
                player1.cantGo = []
                break
            else:
                player1.Do = [0, 0, "Z"]
            player1.update(player1.Do, player1.turn)
    mousex, mousey = pygame.mouse.get_pos()

    '''
    if left and a > -max_speed:
        a -= aceeleration
    if right and a < max_speed:
        a += aceeleration
    if not left and not right:
        a = a/friction

    b = b+a
    c = c+gravity
    '''

    pygame.display.set_caption(str(round(clock.get_fps())))
    clock.tick(FPS)
    if temp < 50: temp += 1
    else: temp = 0

    screen.fill(WHITE)
    tiles.draw(screen)
    tiles2.draw(screen)
    pygame.draw.rect(screen, RED, [mousex, mousey, temp, 10])
    #pygame.draw.rect(screen, BLACK, [int(b), c, 10, 10])
    pygame.draw.rect(screen, BLUE, [player1.pos[0], player1.pos[1], size, size])
    pygame.display.flip()

pygame.quit()
