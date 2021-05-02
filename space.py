# Copyright 2021 Dinu Ion Irinel
import pygame
import os
import time
import random
pygame.font.init()
width = 750
height = 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")
score = 0
main_font = pygame.font.SysFont("comicsans", 50)
vel = 5
bg = pygame.image.load("back.jpg")
space = pygame.image.load("ship.png")
laser = pygame.image.load("laser.png")
enemie_img = pygame.image.load("enemies.png")
e = []
# ship class


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laserss = []
        self.down = 0

    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = space
        self.laser_img = laser
        self.mask = pygame.mask.from_surface(self.ship_img)


class Enemie:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = enemie_img
        self.laserss = []
        self.down = 0

    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))


class Bunkers:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 100, 50))


# main loop
def main():
    running = True
    fps = 60
    clock = pygame.time.Clock()
    player = Player(400, 600)
    enemie = Enemie(200, 200)
    bunker1 = Bunkers(300, 500)
    bunker2 = Bunkers(470, 530)
    bunker3 = Bunkers(100, 530)

    def redraw():
        screen.blit(bg, (0, 0))
        live_score = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        screen.blit(live_score, (10, 30))
        player.draw(screen)
        for i in e:
            enemie.draw(screen)
        bunker1.draw(screen)
        bunker2.draw(screen)
        bunker3.draw(screen)
        pygame.display.update()

    while running:
        clock.tick(fps)
        for i in range(0, 5):
            en = Enemie(random.randrange(50, width - 100),
                        random.randrange(-1500, -100))
            e.append(en)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - vel > 0:  # left
            player.x -= vel
        if keys[pygame.K_d] and player.x + vel + 100 < width:  # right
            player.x += vel
        redraw()


main()
