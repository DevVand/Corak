import pygame
from Game.Corak.dicio import *
from Game.Corak.mapread4 import mapread

class Corak(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.at = [1, 6]
        self.pos = [size * self.at[0] + offsets[0], size * self.at[1] + offsets[1]]

        self.turn = True
        self.jump = False
        self.air = False
        self.focus = False
        self.grab = False
        self.hit = False

    def checkMap(self):
        self.cantGo = []
        self.canGo = []
        for x in -1, 1:
            try:
                print(sala[self.at[1]][self.at[0] + x])
                if sala[self.at[1]][self.at[0] + x] == "0" or self.at[0] + x < 0:
                    self.canGo.append([x, 0])
            except:
                print("")
                self.canGo.append([x, 0])
        for y in -1, 1:
            try:
                if sala[self.at[1] + y][self.at[0]] == "0" or self.at[1] + y < 0:
                    self.canGo.append([0, y])
            except:
                self.canGo.append([0, y])
        print(self.canGo)

        self.air = False

        for xy in self.canGo:
            if xy == [0, 1]:
                self.air = True


        self.checkMove()

    def checkMove(self):

        if self.turn:
            self.cantGo.append([0, 0])

            if self.air:
                self.cantGo.append([0, -1])


        if not self.turn:
            if self.air:
                self.cantGo.append([0, -1])

            if not self.jump and self.air:
                self.goTo = [0, 1]
                self.jump = True
                self.Move()


            if self.jump:
                self.jump = False

            self.turn = True
            self.checkMove()
            print("b")
        print(self.cantGo)

    def Move(self):
        for xy in self.canGo:
            if xy == goTo:

                self.at[0] = self.at[0] + goTo[0]
                self.at[1] = self.at[1] + goTo[1]
                self.pos[0] = size * self.at[0] + offsets[0]
                self.pos[1] = size * self.at[1] + offsets[1]
                print(self.at)

                if -1 == goTo[1]:
                    self.jump = True
                    self.air = True

                self.goTo = []
                self.turn = False
                print("a")
                self.checkMap()



        if -1 == self.at[0]:
            print("levelleft")
        elif len(sala[0]) == self.at[0]:
            print("levelright")
        elif -1 == self.at[1]:
            print("levelup")
        elif len(sala[0]) == self.at[1]:
            print("leveldown")



screen = pygame.display.set_mode((ScreenX, ScreenY))

txt = "../salas/LUD3wayX"
sala = openSala(txt)
tiles = mapread(sala)
size = getSize(sala)
offsets = getOffset(sala, size, "sala")

goTo = [0, 0]


player1 = Corak()

print(tiles)


left = False
right = False
b = 10
a = 0
c = 0
player1.checkMap()



clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                goTo = [0, -1]
            elif event.key == pygame.K_a:
                goTo = [-1, 0]
            elif event.key == pygame.K_d:
                goTo = [1, 0]
            elif event.key == pygame.K_s:
                goTo = [0, 1]
            elif event.key == pygame.K_UP:
                goTo = [0, -1]
            elif event.key == pygame.K_LEFT:
                goTo = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                goTo = [1, 0]
            elif event.key == pygame.K_DOWN:
                goTo = [0, 1]

            player1.Move()



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


    screen.fill(WHITE)
    tiles.draw(screen)
    pygame.draw.rect(screen, RED, [mousex, mousey, 10, 10])
    pygame.draw.rect(screen, BLACK, [int(b), c, 10, 10])
    pygame.draw.rect(screen, BLUE, [player1.pos[0], player1.pos[1], size, size])
    pygame.display.flip()


pygame.quit()
