class Drop:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos

    def update_pos(self):
        self.pos[1] += 15

    def get_type(self):
        return self.type

    def get_pos(self):
        return self.pos
