import pygame
import random
from player import Player
from projectile import Projectile
from target import Target


class Game:
    def __init__(self, game_size):
        self.game_size = game_size
        self.targets = []
        self.projectiles = []
        self.score = 0
        self.lives = 5
        self.player_cooldown = 0
        self.game_over = False

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 50)
        screen = pygame.display.set_mode(self.game_size)
        game_running = True
        player = Player()
        player_moving_right, player_moving_left = False, False
        while game_running:
            clock.tick(25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                if self.game_over is False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            player_moving_right = True
                            player.update_pos("right")
                        if event.key == pygame.K_LEFT:
                            player_moving_left = True
                            player.update_pos("left")
                        if event.key == pygame.K_SPACE:
                            if self.player_allowed_to_shoot():
                                self.projectiles.append(Projectile(player.get_pos()))
                                self.player_cooldown = 15
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
                    self.check_targets()
                    self.create_targets()
                    screen.fill("black")
                    self.draw_projectiles(screen)
                    self.draw_targets(screen)
                    player.draw_player(screen)
                    if self.get_lives() <= 0:
                        self.game_over = True
                        self.show_game_over_screen(screen)
                    else:
                        self.draw_text(screen)
                    pygame.display.flip()
        pygame.quit()

    def get_targets(self):
        return self.targets

    def get_projectiles(self):
        return self.projectiles

    def create_targets(self):
        if len(self.targets) < 5:
            if random.random() > 0.9:
                self.targets.append(Target(random.randint(25, 775), -25))

    def draw_projectiles(self, surface):
        for projectile in self.projectiles:
            projectile.update_pos()
            projectile.draw_projectile(surface)

    def draw_targets(self, surface):
        for target in self.targets:
            target.update_pos()
            target.draw_target(surface)

    def check_targets(self):
        for target in self.targets:
            if target.get_pos()[1] >= 700:
                self.targets.remove(target)
                self.lives -= 1
            for projectile in self.projectiles:
                if (abs(projectile.get_pos()[0] - target.get_pos()[0]) <= 20) and (abs(projectile.get_pos()[1] - target.get_pos()[1]) <= 20):
                    self.targets.remove(target)
                    self.projectiles.remove(projectile)
                    self.score += 1

    def get_score(self):
        return self.score

    def get_lives(self):
        return self.lives

    def draw_text(self, surface):
        font = pygame.font.Font('freesansbold.ttf', 20)
        score = font.render("Score: " + str(self.get_score()), True, (255, 255, 255))
        lives = font.render("Lives: " + str(self.get_lives()), True, (255, 255, 255))
        surface.blit(score, (30, 770))
        surface.blit(lives, (700, 770))

    def show_game_over_screen(self, surface):
        font = pygame.font.Font('freesansbold.ttf', 60)
        over_text = font.render("Game Over!", True, (255, 255, 255))
        score = font.render("Score: " + str(self.get_score()), True, (255, 255, 255))
        surface.blit(over_text, (200, 150))
        surface.blit(score, (200, 400))

    def get_player_cooldown(self):
        return self.player_cooldown

    def player_allowed_to_shoot(self):
        if self.player_cooldown <= 0:
            return True
        else:
            return False
