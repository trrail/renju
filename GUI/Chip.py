import pygame


class Chip():
    def __init__(self, color, position):
        self.color = color
        self.position = ((position[0] + 1) * 25 + 9, (position[1] + 1) * 25 + 9)
        self.radius = 10

    def draw_chip(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)