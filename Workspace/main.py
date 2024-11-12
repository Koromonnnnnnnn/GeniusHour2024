import pygame
import random
import math
from pygame import mixer
from shakeMechanics import ShakeEffect

pygame.init()
mixer.init()

gamescreen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Shuttle Hyperspeed")
clock = pygame.time.Clock()

cockpit_image = pygame.image.load("cockpit.png")
cockpit_image = pygame.transform.scale(cockpit_image, (1280, 720))

enemy_image = pygame.image.load("enemyship.png")
enemy_image = pygame.transform.scale(enemy_image, (65, 65))

boss_image = pygame.image.load("boss.png")
boss_image = pygame.transform.scale(boss_image, (180, 180))

hitMarker = pygame.image.load("hitMarker.png")
hitMarker = pygame.transform.scale(hitMarker, (50, 50))

shake_effect = ShakeEffect(gamescreen, boss_image, (555, 190))
bossFight = False

boss_music = pygame.mixer.music.load("bossBattle.mp3")
pygame.mixer.music.set_volume(0.5)

shootSFX = pygame.mixer.Sound("blasterShot.mp3")
shootSFX.set_volume(0.5)

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

# repurposed space invader code


class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True

    def draw(self, surface):
        if self.isAlive:
            surface.blit(enemy_image, (self.xpos, self.ypos))

    def move(self, dx, dy):
        self.xpos += dx
        self.ypos += dy


class AlienSpawner:
    def __init__(self, surface):
        self.surface = surface
        self.armada = []
        self.spawnAliens()

    def spawnAliens(self):
        for i in [points, points2, points3]:
            for xpos, ypos in i:
                self.armada.append(Alien(xpos, ypos))

    def draw(self, surface):
        for alien in self.armada:
            alien.draw(surface)

    def move(self, dx, dy):
        for alien in self.armada:
            if alien.isAlive:
                alien.move(dx, dy)

    def checkCollisions(self, mouse_pos):
        global gameOver
        for alien in self.armada:
            if alien.isAlive:
                alien_rect = pygame.Rect(alien.xpos, alien.ypos, 65, 65)
                if alien_rect.collidepoint(mouse_pos):
                    alien.isAlive = False
                    self.armada = [alien for alien in self.armada if alien.isAlive]
                    return True
        return False


spawnAlien = AlienSpawner(gamescreen)

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


bossmusic_playing = False

hitmarker_positions = []

while not gameOver:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # For testing purposes
            x, y = pygame.mouse.get_pos()
            print(f"Pos: ({x}, {y})")
            hitmarker_positions.append((x, y))
            pygame.mixer.Sound.play(shootSFX)
            if spawnAlien.checkCollisions((x, y)):
                print(len(spawnAlien.armada))
                pass

    # Code from last years particle slide deck

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

    spawnAlien.move(0, 0.2)

    pygame.draw.circle(gamescreen, path_color, (xpos_path, ypos_path), 2)

    for pos in hitmarker_positions:
        gamescreen.blit(hitMarker, pos)

    spawnAlien.draw(gamescreen)

    gamescreen.blit(cockpit_image, (0, 0))

    if len(spawnAlien.armada) == 0:
        bossFight = True
    if bossFight and not shake_effect.is_shaking:
        shake_effect.start()
    if bossFight and not bossmusic_playing:
        pygame.mixer.music.play(-1)
        bossmusic_playing = True

    shake_effect.update()

    pygame.display.flip()

pygame.quit()
