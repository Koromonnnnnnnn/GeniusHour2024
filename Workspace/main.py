import pygame
import random
import math

pygame.init()

gamescreen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Shuttle Hyperspeed")
clock = pygame.time.Clock()

cockpit_image = pygame.image.load("cockpit.png")
cockpit_image = pygame.transform.scale(
    cockpit_image, (1280, 720)
) 

gameOver = False

xpos = [] 
ypos = []
xVel = []
yVel = []
sizes = []
colors = []  
speed = 6  

angle = 0
hue = 0  

# This hue to rgb function was not created by me.
def hue_to_rgb(hue):
    h = hue / 60.0
    c = 255
    x = c * (1 - abs((h % 2) - 1))
    r = g = b = 0

    if 0 <= h < 1:
        r, g, b = c, x, 0
    elif 1 <= h < 2:
        r, g, b = x, c, 0
    elif 2 <= h < 3:
        r, g, b = 0, c, x
    elif 3 <= h < 4:
        r, g, b = 0, x, c
    elif 4 <= h < 5:
        r, g, b = x, 0, c
    elif 5 <= h < 6:
        r, g, b = c, 0, x

    return (int(r), int(g), int(b))


while not gameOver:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True

    angle += 1
    if angle > 360:
        angle = 0

    radians = math.radians(angle)

    for i in range(1):
        if len(xpos) < 1000:
            velX = random.uniform(-1, 1)
            velY = random.uniform(-1, 1)
            magnitude = math.sqrt(velX**2 + velY**2)
            if magnitude != 0:
                normalizedVelX = speed * velX / magnitude
                normalizedVelY = speed * velY / magnitude
            else:
                normalizedVelX = 0
                normalizedVelY = 0

            xpos.append(640)
            ypos.append(360)
            sizes.append(1)
            colors.append(hue_to_rgb(hue)) 
            xVel.append(normalizedVelX)
            yVel.append(normalizedVelY)

    for i in range(len(xpos)):
        xpos[i] += xVel[i]
        ypos[i] += yVel[i]
        sizes[i] += 0.03

        if xpos[i] < 0 or xpos[i] > 1280 or ypos[i] < 0 or ypos[i] > 720:
            xpos[i] = 640
            ypos[i] = 360
            sizes[i] = 1
            velX = random.uniform(-1, 1)
            velY = random.uniform(-1, 1)
            magnitude = math.sqrt(velX**2 + velY**2)
            if magnitude != 0:
                xVel[i] = speed * velX / magnitude
                yVel[i] = speed * velY / magnitude
            else:
                xVel[i] = 0
                yVel[i] = 0

            colors[i] = hue_to_rgb(hue)

    xpos_path = int(50 * math.cos(radians * 5) + 640)  
    ypos_path = int(50 * math.sin(radians * 5) + 360) 

    hue += 1
    if hue >= 360:
        hue = 0

    path_color = hue_to_rgb(hue)

    gamescreen.fill((0, 0, 0))  

    for i in range(len(xpos)):
        pygame.draw.circle(
            gamescreen, colors[i], (int(xpos[i]), int(ypos[i])), int(sizes[i])
        )

    pygame.draw.circle(gamescreen, path_color, (xpos_path, ypos_path), 2)

    gamescreen.blit(cockpit_image, (0, 0))

    pygame.display.flip()

pygame.quit()
