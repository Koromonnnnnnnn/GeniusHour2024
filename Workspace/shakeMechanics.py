import pygame
import random

class ShakeEffect:
    def __init__(self, surface, image, position, shake_intensity= 2, shake_duration=100):
        self.surface = surface
        self.image = image
        self.original_position = position
        self.shake_intensity = shake_intensity
        self.shake_duration = shake_duration
        self.start_time = None
        self.is_shaking = False

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.is_shaking = True

    def update(self):
        if self.is_shaking:
            elapsed = pygame.time.get_ticks() - self.start_time
            if elapsed < self.shake_duration:
                offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
                offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
                self.surface.blit(self.image, (self.original_position[0] + offset_x, self.original_position[1] + offset_y))
            else:
                self.is_shaking = False 