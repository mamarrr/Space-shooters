import pygame


class Target:
    def __init__(self, x, y, initial_movement):
        self.pos = [x, y]
        if initial_movement >= 0.5:
            self.move_left = True
            self.move_right = False
        else:
            self.move_right = True
            self.move_left = False

    def update_pos(self):
        if self.pos[0] <= 30:
            self.pos[1] += 55
            self.move_right = True
            self.move_left = False
        if self.pos[0] >= 770:
            self.pos[1] += 55
            self.move_right = False
            self.move_left = True
        if self.move_left:
            self.pos[0] -= 12
        if self.move_right:
            self.pos[0] += 12

    def get_pos(self):
        return self.pos