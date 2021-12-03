import pygame


class Projectile:
    def __init__(self, playerpos):
        self.pos = [playerpos, 700]

    def update_pos(self):
        self.pos[1] -= 25

    def get_pos(self):
        return self.pos

