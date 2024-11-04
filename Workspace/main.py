import pygame
import random
import math
from shakeMechanics import ShakeEffect

pygame.init()

gamescreen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Shuttle Hyperspeed")
clock = pygame.time.Clock()

cockpit_image = pygame.image.load("cockpit.png")
cockpit_image = pygame.transform.scale(cockpit_image, (1280, 720))

enemy_image = pygame.image.load("enemyship.png")
enemy_image = pygame.transform.scale(enemy_image, (65, 65))

boss_image = pygame.image.load("boss.png")
boss_image = pygame.transform.scale(boss_image, (180, 180))

shake_effect = ShakeEffect(gamescreen, boss_image, (555, 190))
bossFight = True

points = [  # These points are here to define the areas where enemies are allowed to spawn. (Left Window)
    (0, 12),
    (454, 181),
    (492, 369),
    (135, 439),
    (127, 433),
    (75, 454),
    (73, 451),
    (52, 447),
    (36, 447),
    (0, 461),
]

points2 = [  # These points are here to define the areas where enemies are allowed to spawn. (Middle Window)
    (517, 153),
    (488, 186),
    (513, 366),
    (760, 366),
    (799, 183),
    (767, 149),
    (636, 148),
]

points3 = [  # These points are here to define the areas where enemies are allowed to spawn. (Rigt Window)
    (812, 188),
    (1207, 1),
    (1276, 3),
    (1275, 420),
    (1275, 444),
    (1106, 394),
    (1056, 387),
    (787, 379),
    (775, 349),
    (817, 181),
    (1026, 90),
]

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


def hue_to_rgb(hue):  # This hue to rgb function was not created by me.
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
        elif event.type == pygame.MOUSEBUTTONDOWN:  # For testing purposes
            x, y = pygame.mouse.get_pos()
            print(f"Pos: ({x}, {y})")

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

    pygame.draw.polygon(gamescreen, (0, 0, 0), points)  # For testing (Left Window)

    pygame.draw.polygon(gamescreen, (0, 0, 0), points2)  # For testing (Middle Window)

    pygame.draw.polygon(gamescreen, (0, 0, 0), points3)  # For testing (Right Window)

    for i in range(len(xpos)):
        pygame.draw.circle(
            gamescreen, colors[i], (int(xpos[i]), int(ypos[i])), int(sizes[i])
        )

    pygame.draw.circle(gamescreen, path_color, (xpos_path, ypos_path), 2)

    gamescreen.blit(cockpit_image, (0, 0))

    gamescreen.blit(enemy_image, (0, 0))

    if bossFight and not shake_effect.is_shaking:
        shake_effect.start()

    shake_effect.update()

    pygame.display.flip()

pygame.quit()
