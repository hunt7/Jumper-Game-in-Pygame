import pygame
import random


(Width, Height) = (500, 300)
running = True
FPS = 60
bg_color = (100, 160, 255)
ob_color = (0, 0, 0)
jp_color = (252, 88, 88)
obstacles = []
velocity = 7
jump = False
jumpCount = 0
points = 0
increment = False
move = 0
z = [points]
running2 = True


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = height
        self.width = width
        self.height = height

    def whoami(self):
        print("x: {}, y: {}, width: {}, height: {}".format(self.x, self.y, self.width, self.height))

    def make(self):
        pygame.draw.rect(window, ob_color, (self.x, Height-self.height, self.width, self.height))

    def move(self):
        self.x -= velocity

    def check(self):
        global points
        if self.x < -self.width:
            points += 10
            pygame.display.set_caption("Score: " + str(points))
            obstacles.pop()
            hesitate = random.randint(0, 1)
            obstacles.append(Obstacle(Width, Height, random.randint(30, 80), random.randint(50, 120)))
            #print(obstacles[-1].whoami())

class Jumper:
    def __init__(self, size):
        self.size = size
        self.x = size
        self.y = Height-size

    def whoami(self):
        print("x: {}, y: {}, size: {}".format(self.x, self.y, self.size))

    def make(self):
        pygame.draw.rect(window, jp_color, (self.x, self.y, self.size, self.size))

    def moveRight(self):
        if self.x+self.size< Width:
            self.x += 5

    def moveLeft(self):
        if self.x > 0:
            self.x -= 5


def life():
    global move
    move += 0.5
    for o in obstacles:
        o.make()
        o.move()
        o.check()
    jumper.make()


pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 60)
fontNG = pygame.font.SysFont('Comic Sans MS', 26)
window = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Score: 0")

#first initial obstacle
obstacles.append(Obstacle(Width, Height, random.randint(30, 60), random.randint(50, 120)))
jumper = Jumper(50)
jumper.make()


pygame.display.flip()
while running:
    pygame.time.delay(int(1000/FPS))

    if z[-1] != points:
        z.pop()
        z.append(points)
        if z[-1]%50 == 0:
            velocity += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        jumper.moveRight()

    if keys[pygame.K_LEFT]:
        jumper.moveLeft()

    if keys[pygame.K_UP]:
        if not jump:
            jump = True
        if jump and jumpCount > 12:
            jump = True
            jumpCount = 0

    if keys[pygame.K_DOWN]:
        jumper.y = Height-jumper.size+20

    if jump and jumpCount < 12.5:
        y = int(60 * jumpCount - 0.5 * 10 * (jumpCount ** 2))
        jumper.y = Height - jumper.size - y
        jumpCount += 0.5

    differenceX = obstacles[0].x - (jumper.x+jumper.size) + velocity
    differenceY = (Height-jumper.y) - obstacles[0].y

    if (differenceX < 0 and differenceX > -(jumper.size+jumper.size)) and differenceY < 0:
        pygame.time.delay(50)
        pygame.display.set_caption("")
        window.fill(bg_color)

        textsurface = font.render("Your Score: " + str(points), False, (0, 0, 0))
        window.blit(textsurface, (Width//2-150, Height//2-50))
        pygame.draw.rect(window, (0, 0, 0), (Width//2-50, 200, 100, 30))

        textsurfaceNG = fontNG.render("New Game", False, (255,255,255))
        window.blit(textsurfaceNG, (Width//2-43, 205))
        pygame.display.update()

        while running2:
            pygame.time.delay(17)
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        running = False
                        running2 = False
                        break

                    if e.key == pygame.K_RETURN:
                        pygame.draw.rect(window, (64, 64, 64), (Width // 2 - 50, 200, 100, 30))
                        textsurfaceNG = fontNG.render("New Game", False, (128, 128, 128))
                        window.blit(textsurfaceNG, (Width // 2 - 43, 205))

                        pygame.display.update()
                        pygame.time.delay(100)
                        textsurfaceNG = fontNG.render("New Game", False, (255, 255, 255))
                        pygame.draw.rect(window, (0, 0, 0), (Width // 2 - 50, 200, 100, 30))
                        window.blit(textsurfaceNG, (Width // 2 - 43, 205))
                        pygame.display.update()
                        pygame.time.delay(100)

                        jumper.x = 0
                        obstacles[0].x = Width
                        points = 0
                        velocity = 7
                        pygame.display.set_caption("Score: 0")
                        running2 = False
                        jump = False
                        jumpCount = 0
                        jumper.y = Height - jumper.size

    running2 = True
    window.fill(bg_color)
    life()
    pygame.display.update()
