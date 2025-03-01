import pygame
from pygame.locals import *

pygame.init()

# Screen dimensions
screen_width = 864
screen_height = 936

# Create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

# Load background image
bg = pygame.image.load('bg.png')
ground = pygame.image.load('ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.mouse = mouse
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 0
        self.clicked = False


    def update(self):

        if flying:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        if not game_over:
            #jump
            if pygame.mouse.get_pressed()[self.mouse] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[self.mouse] == 0:
                self.clicked = False
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2), 0)
flappy1 = Bird(100, int(screen_height / 4), 2)
bird_group.add(flappy)
bird_group.add(flappy1)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game loop
run = True
while run:
    clock.tick(60)  # Limit frame rate to 60 FPS


    # Draw background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    # Draw the ground
    screen.blit(ground, (ground_scroll, 768))

    #check if bird has hit the ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False
    # Draw and scroll the ground

    if game_over == False:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
    # Update display
    pygame.display.update()

pygame.quit()
