import pygame


class Player:
    def __init__(self):
        self.pos = 400
        self.cooldown = 0
        self.powerups = []

    def get_pos(self):
        return self.pos

    def update_pos(self, where):
        if where == "right" and self.pos <= 750:
            self.pos += 15
        if where == "left" and self.pos >= 50:
            self.pos -= 15