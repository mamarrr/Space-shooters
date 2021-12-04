class Highscores:
    def __init__(self):
        self.current_score = None
        self.highest = None
        self.check_highest()

    def add_current_data_to_file(self):
        file = open("highscores.txt", "a")
        file.write(f"{self.current_score},")
        file.close()
        self.check_new_highest()

    def check_new_highest(self):
        if int(self.current_score) > self.highest:
            self.highest = int(self.current_score)

    def check_highest(self):
        if self.highest is None:
            self.highest = 0
        for num in self.read_data():
            if num:
                if int(num) > self.highest:
                    self.highest = int(num)

    def read_data(self):
        file = open("highscores.txt", "r")
        data = file.read()
        data = data.split(",")
        return data

    def get_highest(self):
        return self.highest
