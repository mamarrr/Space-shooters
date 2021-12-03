import pygame


class Projectile:
    def __init__(self, playerpos):
        self.pos = [playerpos, 700]

    def draw_projectile(self, surface):
        pygame.draw.line(surface, (255, 255, 255), self.get_pos(), (self.get_pos()[0], self.get_pos()[1] + 25))

    def update_pos(self):
        self.pos[1] -= 25

    def get_pos(self):
        return self.pos

