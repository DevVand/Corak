import pygame

sala = "LRUDhallX.txt"

a = []
word = ""

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

offsetY = 0
offsetX = 0

x = 500
y = 500

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
r = (255, 0, 0)
g = (150, 150, 150)
b = (0, 0, 255)
ye = (255, 255, 0)
w = (255, 255, 255)
b = (0, 0, 0)
screen.fill((b))
pygame.display.flip()



offsetX = int((x / 2) - ((len(a[0]) * size) / 2))
offsetY = int((y / 2) - ((len(a) * size) / 2))

for Line in range(len(a)):
    for Colum in range(len(a[0])):
        if a[Line][Colum] == "0":
            pygame.draw.rect(screen, w, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "1":
            pygame.draw.rect(screen, b, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "2":
            pygame.draw.rect(screen, g, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "3":
            pygame.draw.rect(screen, ye, [size * Colum + offsetX, size * Line + offsetY, size, size])
        if a[Line][Colum] == "4":
            pygame.draw.rect(screen, r, [size * Colum + offsetX, size * Line + offsetY, size, size])

pygame.display.flip()
pygame.time.wait(150)

print(len(a), "x", len(a[0]))
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()

pygame.quit()
