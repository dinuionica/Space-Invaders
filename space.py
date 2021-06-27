# Dinu Ion-Irinel 2020
import pygame
import random
pygame.init()

# The game screen
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Joc Space Invaders')
bg = pygame.image.load('back.png')
fps = 70
White = (255, 255, 255)
Black= (0, 0, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)

# The class of ship
class Ship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.lives = 5
        self.score = 0
        self.level = 3
        self.highscore = 0

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# The class of enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.group_rect = pygame.Rect(130, 75, 500, 250)
        self.direction = ship.level * 10
        self.lives = ship.level
    def update(self):
        self.rect.x += self.direction
        self.group_rect.x += self.direction
        if self.group_rect.x + 500 >= 725:
            self.direction = -self.direction
        if self.group_rect.x <= 25:
            self.direction = -self.direction
            self.rect.y += 50
# The class of bunkers
class Bunk(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bunk.png')
        self.rect = self.image.get_rect()

# The class of laser
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('laser.png')
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.y += -10

# The class of bombs
class Bomb(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('laser.png')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 10


ship = Ship()
ship.rect.x = 375
ship.rect.y = 650

enemy_list = pygame.sprite.Group()
bunker_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()
# create enemies
def make_enemies():
    for row in range(1, 5):
        for column in range(1, 11):
            enemy = Enemy()
            enemy.rect.x = 80 + 40 * column
            enemy.rect.y = 25 + 40 * row
            enemy_list.add(enemy)
make_enemies()
# create bunkers
def make_bunkers():
    for bunk in range(3):
        for row in range(5):
            for column in range(10):
                bunker = Bunk()
                bunker.rect.x = 50 + 275 * bunk + 10 * column
                bunker.rect.y = 500 + 10 * row
                bunker_list.add(bunker)
make_bunkers()

# The function to display results
def redraw_function():
    screen.blit(bg, (0, 0))
    if playing:
        bottom = pygame.draw.rect(screen, Green, (50, 700, 650, 5))
        for i in range(ship.lives):
            pygame.draw.rect(screen, Red, (50 + i * 130, 715, 130, 15))
            
        # title of the game
        font = pygame.font.SysFont('Courier New', 30)
        text = font.render('Joc Space Invaders', False, Red)
        textRect = text.get_rect()
        textRect.center = (750 // 2, 25)
        screen.blit(text, textRect)

        # level of the game
        text = font.render('Level: ' + str(ship.level), False, Red)
        textRect = text.get_rect()
        textRect.center = (100, 25)
        screen.blit(text, textRect)

        # diplay score
        text = font.render('Score: ' + str(ship.score), False, Red)
        textRect = text.get_rect()
        textRect.center = (650, 25)
        screen.blit(text, textRect)

        # display objects created
        ship.draw()
        enemy_list.update()
        enemy_list.draw(screen)
        bunker_list.draw(screen)
        laser_list.update()
        laser_list.draw(screen)
        bomb_list.update()
        bomb_list.draw(screen)
    else:
        # title of the game
        font = pygame.font.SysFont('Courier New', 60)
        text = font.render('Joc Space Invaders', False, Green)
        textRect = text.get_rect()
        textRect.center = (750 // 2, 50)
        screen.blit(text, textRect)

        # the best score of the game
        text = font.render('Highscore: ' + str(ship.highscore), False, Red)
        textRect = text.get_rect()
        textRect.center = (750 // 2, 750 // 2)
        screen.blit(text, textRect)

        # message for the start
        text = font.render('Apasa Space', False, Green)
        textRect = text.get_rect()
        textRect.center = (750 // 2, 700)
        screen.blit(text, textRect)

    # Refresh screen

    pygame.display.update()
running = True
playing = False
while running:
    pygame.time.delay(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if playing:
        # controlling keys
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            ship.rect.x += -10
        if key[pygame.K_d]:
            ship.rect.x += 10
        if key[pygame.K_SPACE]:
            if len(laser_list) < 500:
                laser = Laser()
                laser.rect.x = ship.rect.x + 25
                laser.rect.y = ship.rect.y
                laser_list.add(laser)
        # Shooting Enemy Bombs
        shoot_chance = random.randint(1, 100)
        bomb_chance = ship.level * 10
        if shoot_chance < bomb_chance:
            if len(enemy_list) > 0:
                random_enemy = random.choice(enemy_list.sprites())
                bomb = Bomb()
                bomb.rect.x = random_enemy.rect.x + 12
                bomb.rect.y = random_enemy.rect.y + 25
                bomb_list.add(bomb)
        # Shooting of the laser 
        for laser in laser_list:
            if laser.rect.y < -10:
                laser_list.remove(laser)
            for enemy in enemy_list:
                if laser.rect.colliderect(enemy.rect):
                    ship.score += 1
                    laser_list.remove(laser)
                    enemy.lives -= 1
                    if enemy.lives <= 0:
                        enemy_list.remove(enemy)

            for bunker in bunker_list:
                if laser.rect.colliderect(bunker.rect):
                    laser_list.remove(laser)
                    bunker_list.remove(bunker)
        # bomb blows
        for bomb in bomb_list:
            if bomb.rect.y > 750:
                bomb_list.remove(bomb)
            if bomb.rect.colliderect(ship.rect):
                bomb_list.remove(bomb)
                ship.lives -= 1
            for bunker in bunker_list:
                if bomb.rect.colliderect(bunker.rect):
                    bomb_list.remove(bomb)
                    bunker_list.remove(bunker)
        # collision check
        for enemy in enemy_list:
            for bunker in bunker_list:
                if enemy.rect.colliderect(bunker.rect):
                    playing = False
                    if ship.score > ship.highscore:
                        ship.highscore = ship.score
      # check score
        if ship.lives < 0:
            playing = False
            if ship.score > ship.highscore:
                ship.highscore = ship.score
            ship.lives = 5
            enemy.lives = 1
        # check enemies
        if len(enemy_list) == 0:
            ship.level += 1
            make_enemies()
    else:
        bomb_list.empty()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            playing = True
            ship.level = 1
            ship.score = 0
            bunker_list.empty()
            make_bunkers()
            enemy_list.empty()
            make_enemies()
    redraw_function()
pygame.quit()
			
