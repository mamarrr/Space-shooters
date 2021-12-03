import pygame


class Player:
    def __init__(self):
        self.pos = 400
        self.cooldown = 0

    def get_pos(self):
        return self.pos

    def draw_player(self, surface):
        pygame.draw.polygon(surface, (255, 0, 0), [(self.get_pos() - 25, 725), (self.get_pos(), 675), (self.get_pos() + 25, 725)])

    def update_pos(self, where):
        if where == "right" and self.pos <= 750:
            self.pos += 15
        if where == "left" and self.pos >= 50:
            self.pos -= 15
