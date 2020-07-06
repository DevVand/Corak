import pygame

sala = "LRUDhallX.txt"

a = []


file = open(sala, 'r')
while True:
    word = file.readline()
    if "X" in word:
        break
    a.append(word[:-1])
file.close

print("lines in list:", len(a))
print("colums in list:", len(a[0]))
print("list:", a)

actualword = ""
for andar in a:
    for temp in andar:
        actualword += temp
        actualword += "  "

    print(actualword)
    actualword = ""

offsetY = 0
offsetX = 0

x = 1000
y = 1000

if x >= y:
    if len(a[0]) > len(a):
        size = int(x / len(a[0]))
    else:
        size = int(y / len(a))
else:
    size = int(y / len(a))
    if len(a) > len(a[0]):
        size = int(y / len(a))
    else:
        size = int(x / len(a[0]))

print("size:", size)

screen = pygame.display
screen = pygame.display.set_mode((x, y))
screen1 = pygame.Surface((x, y))

r = (255, 0, 0)
g = (150, 150, 150)
b = (0, 0, 255)
ye = (255, 255, 0)
w = (255, 255, 255)
b = (0, 0, 0)

pointer = pygame.Surface((10, 10))
pointer.fill(r)

offsetX = int((x / 2) - ((len(a[0]) * size) / 2))
offsetY = int((y / 2) - ((len(a) * size) / 2))

alltile = ()

for Line in range(len(a)):
    for Colum in range(len(a[0])):
        if a[Line][Colum] == "0":
            pygame.draw.rect(screen1, w, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "1":
            pygame.draw.rect(screen1, b, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "2":
            pygame.draw.rect(screen1, g, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "3":
            pygame.draw.rect(screen1, ye, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "4":
            pygame.draw.rect(screen1, r, [size * Colum + offsetX, size * Line + offsetY, size, size])

clock = pygame.time.Clock()
print(len(a), "x", len(a[0]))

while True:


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()

    clock.tick(60)

    mousex, mousey = pygame.mouse.get_pos()

    #pygame.draw.rect(screen2, w, [mousex, mousey, 50, 50])

    screen.blit(screen1, (0, 0))
    screen.blit(pointer, (mousex, mousey))

    pygame.display.flip()


pygame.quit()