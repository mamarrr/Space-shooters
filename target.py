import pygame


class Target:
    def __init__(self, x, y):
        self.pos = [x, y]

    def draw_target(self, surface):
        pygame.draw.circle(surface, (0, 0, 255), self.get_pos(), 20)

    def update_pos(self):
        self.pos[1] += 4

    def get_pos(self):
        return self.pos