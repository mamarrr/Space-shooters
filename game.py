import pygame
import random
import os
from player import Player
from projectile import Projectile
from target import Target
from highscores import Highscores
from drops import Drop


class Game:
    def __init__(self, game_size):
        self.game_size = game_size
        self.targets = []
        self.projectiles = []
        self.drops = []
        self.score = 0
        self.lives = 5
        self.player_cooldown = 0
        self.game_over = False
        self.highscores = Highscores()
        self.images = {}
        self.difficulty = "Easy"

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 50)
        screen = pygame.display.set_mode(self.game_size)
        self.load_images()
        game_running = True
        player = Player()
        player_moving_right, player_moving_left = False, False
        while game_running:
            clock.tick(25)
            for event in pygame.event.get():
                if self.get_game_over() is True:
                    if event.type == pygame.KEYDOWN:
                        self.highscores.current_score = self.score
                        self.highscores.check_new_highest()
                        self.highscores.add_current_data_to_file()
                        if event.key == pygame.K_RETURN:
                            player = Player()
                            self.lives = 5
                            self.score = 0
                            self.player_cooldown = 0
                            self.targets = []
                            self.projectiles = []
                            self.drops = []
                            self.difficulty = "Easy"
                            self.game_over = False
                    if event.type == pygame.QUIT:
                        self.highscores.current_score = self.score
                        self.highscores.check_new_highest()
                        self.highscores.add_current_data_to_file()
                        game_running = False
                if event.type == pygame.QUIT:
                    self.highscores.current_score = self.score
                    self.highscores.check_new_highest()
                    self.highscores.add_current_data_to_file()
                    game_running = False
                if self.get_game_over() is False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            player_moving_right = True
                        if event.key == pygame.K_LEFT:
                            player_moving_left = True
                        if event.key == pygame.K_SPACE:
                            if self.player_allowed_to_shoot():
                                self.projectiles.append(Projectile(player.get_pos()))
                                self.player_cooldown = self.calculate_player_cooldown(player)
                                print(self.player_cooldown)
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT:
                            player_moving_right = False
                        if event.key == pygame.K_LEFT:
                            player_moving_left = False
                if event.type == pygame.USEREVENT:
                    self.player_cooldown -= 1
                    if self.game_over is False:
                        if player_moving_right:
                            player.update_pos("right")
                        if player_moving_left:
                            player.update_pos("left")
                    self.update_everything(screen, player)
                    screen.blit(self.images["spaceship"], (player.get_pos() - 36.5, 700))
                    if self.get_lives() <= 0:
                        self.game_over = True
                        self.show_game_over_screen(screen)
                    else:
                        self.draw_text(screen)
                    pygame.display.flip()
        pygame.quit()

    def update_everything(self, surface, player):
        self.check_difficulty()
        surface.fill("black")
        surface.blit(self.images["background"], (0, 0))
        self.check_targets()
        self.check_drops(player)
        self.create_targets(self.get_difficulty())
        self.draw_projectiles(surface)
        self.draw_targets(surface)
        self.draw_drops(surface)

    def check_difficulty(self):
        if self.score > 100:
            self.difficulty = "Normal"
        if self.score > 250:
            self.difficulty = "Hard"

    def create_targets(self, difficulty):
        if difficulty == "Easy":
            if len(self.targets) < 25:
                if random.random() > 0.95:
                    self.targets.append(Target(random.randint(25, 775), -25, random.random()))
        if difficulty == "Normal":
            if len(self.targets) < 27:
                if random.random() > 0.9:
                    self.targets.append(Target(random.randint(25, 775), -25, random.random()))
        if difficulty == "Hard":
            if len(self.targets) < 30:
                if random.random() > 0.8:
                    self.targets.append(Target(random.randint(25, 775), -25, random.random()))

    def check_targets(self):
        for target in self.targets:
            if target.get_pos()[1] >= 700:
                self.targets.remove(target)
                self.lives -= 1
            for projectile in self.projectiles:
                if (abs(projectile.get_pos()[0] - target.get_pos()[0]) <= 40) and (abs(projectile.get_pos()[1] - target.get_pos()[1]) <= 50):
                    if random.random() > 0.9:
                        if random.random() >= 0.5:
                            self.drops.append(Drop("heart", target.get_pos()))
                        else:
                            self.drops.append(Drop("cooldown_reduction", target.get_pos()))
                    self.targets.remove(target)
                    self.projectiles.remove(projectile)
                    self.score += 1

    def check_drops(self, player):
        for drop in self.drops:
            if drop.get_pos()[1] >= 800:
                self.drops.remove(drop)
            if (abs(drop.get_pos()[0] - player.get_pos()) <= 35) and (abs(drop.get_pos()[1] - 700) <= 35):
                if drop.type == "heart":
                    self.lives += 1
                if drop.type == "cooldown_reduction":
                    player.powerups.append("cooldown_reduction")
                self.drops.remove(drop)

    def calculate_player_cooldown(self, player):
        cooldown = 15
        for powerup in player.powerups:
            if powerup == "cooldown_reduction":
                cooldown -= 0.5
        return cooldown

    def draw_projectiles(self, surface):
        for projectile in self.projectiles:
            projectile.update_pos()
            surface.blit(self.images["projectile"], (projectile.get_pos()[0] - 10, projectile.get_pos()[1] - 10))

    def draw_targets(self, surface):
        for target in self.targets:
            target.update_pos()
            surface.blit(self.images["target"], (target.get_pos()[0] - 50, target.get_pos()[1] - 50))

    def draw_text(self, surface):
        font = pygame.font.Font('freesansbold.ttf', 20)
        score = font.render("Score: " + str(self.get_score()), True, (255, 255, 255))
        highscore = font.render("Highscore: " + str(self.highscores.get_highest()), True, (255, 255, 255))
        difficulty = font.render("Difficulty: " + str(self.get_difficulty()), True, (255, 255, 255))
        lives = font.render("Lives: " + str(self.get_lives()), True, (255, 255, 255))
        surface.blit(score, (30, 740))
        surface.blit(highscore, (30, 770))
        surface.blit(difficulty, (620, 20))
        surface.blit(lives, (700, 770))

    def draw_drops(self, surface):
        for drop in self.drops:
            drop.update_pos()
            surface.blit(self.images[drop.type], drop.get_pos())

    def show_game_over_screen(self, surface):
        font = pygame.font.Font('freesansbold.ttf', 30)
        over_text = font.render("Game Over!", True, (255, 255, 255))
        score = font.render("Score: " + str(self.get_score()), True, (255, 255, 255))
        highscore = font.render("Highscore: " + str(self.highscores.get_highest()), True, (255, 255, 255))
        play_again = font.render("Press Enter to play again", True, (255, 255, 255))
        surface.blit(over_text, (200, 150))
        surface.blit(score, (200, 300))
        surface.blit(highscore, (200, 450))
        surface.blit(play_again, (200, 600))

    def player_allowed_to_shoot(self):
        if self.player_cooldown <= 0:
            return True
        else:
            return False

    def load_images(self):
        for file_name in os.listdir("images"):
            if not file_name.endswith(".png"):
                continue
            image = pygame.image.load(r"images/" + file_name)
            if file_name.split(".")[0] == "spaceship":
                image = pygame.transform.scale(image, (75, 75))
            if file_name.split(".")[0] == "projectile":
                image = pygame.transform.scale(image, (20, 20))
            if file_name.split(".")[0] == "target":
                image = pygame.transform.scale(image, (100, 100))
            if file_name.split(".")[0] == "background":
                image = pygame.transform.scale(image, (800, 800))
            if file_name.split(".")[0] == "heart" or file_name.split(".")[0] == "cooldown_reduction":
                image = pygame.transform.scale(image, (20, 20))
            if file_name.split(".")[0] != "background":
                image.convert_alpha()
                image.set_colorkey((0, 0, 0))
            self.images[file_name.split(".")[0]] = image

    def get_targets(self):
        return self.targets

    def get_projectiles(self):
        return self.projectiles

    def get_game_over(self):
        return self.game_over

    def get_score(self):
        return self.score

    def get_lives(self):
        return self.lives

    def get_difficulty(self):
        return self.difficulty

    def get_player_cooldown(self):
        return self.player_cooldown
