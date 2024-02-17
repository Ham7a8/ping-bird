import time
import pygame
import sys
import math
import os
import random

pygame.init()

clock = pygame.time.Clock()

WINDOW_SIZE = (500, 300)
DISPLAY = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Flapping Bird')

bird_animation = []
bird_folder = "bird_animation"
for i in range(0, 7):
    bird_image = pygame.image.load(os.path.join(bird_folder, f"bird_frame_{i}.png"))
    bird_image = pygame.transform.scale(bird_image, (50, 50))
    bird_animation.append(bird_image)
    

coin_animation = []
coin_folder = "coin_animation"
for i in range(0, 4):
    coin_image = pygame.image.load(os.path.join(coin_folder, f"coin_frame_{i}.png"))
    coin_image = pygame.transform.scale(coin_image, (30, 30))
    coin_animation.append(coin_image)

spike_R_image = pygame.image.load("spike_R.png")
spike_R_image = pygame.transform.scale(spike_R_image, (30, 30))

spike_L_image = pygame.image.load("spike_L.png")
spike_L_image = pygame.transform.scale(spike_L_image, (30, 30))

start_button_img = pygame.image.load("start.png")
start_button_rect = start_button_img.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 +80))

# Load the custom font
font_path = "font.otf"
font_size = 24
font_small = pygame.font.Font(font_path, font_size)

# Load the name.png image
name_img = pygame.image.load("name.png")
name_img_rect = name_img.get_rect(center=(WINDOW_SIZE[0] // 2, start_button_rect.top - 100))

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_sequence = coin_animation
        self.frame_index = 0
        self.collected = False
        self.rect = self.image_sequence[0].get_rect(topleft=(x, y))
        self.last_frame_time = time.time()
        self.frame_delay = 0.2

    def draw(self, surface):
        if not self.collected:
            current_time = time.time()
            if current_time - self.last_frame_time >= self.frame_delay:
                self.frame_index = (self.frame_index + 1) % len(self.image_sequence)
                self.last_frame_time = current_time
            surface.blit(self.image_sequence[self.frame_index], self.rect)

coin_distance = 80  # Minimum distance between coins
prev_coin_pos = (WINDOW_SIZE[0] // 2, random.randint(50, WINDOW_SIZE[1] - 50))
coin = Coin(*prev_coin_pos)

x = 100
y = 100
velocity_y = 0
acceleration = 0.2
jump_strength = -5
jumping = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

shrink_speed = 2  # adjust the speed of shrinking
expand_speed = 2  # adjust the speed of expanding
shrinking = False
expanding = False

circle_radius = 200
original_radius = circle_radius
circle_thickness = 5
circle_color = RED

velocity_x = -3
flip = False
animation_frame = 0

rotOffset = 3
frame_delay = 0.05

bird_hitbox_width = 40
bird_hitbox_height = 40

last_frame_time = time.time()

spikes = []



def generate_spikes():
    spikes.clear()
    last_y = -100
    while last_y + 100 < WINDOW_SIZE[1] - 50:
        spike_x = random.randint(0, 1) * (WINDOW_SIZE[0] - spike_R_image.get_width())
        spike_y = random.randint(last_y + 100, min(WINDOW_SIZE[1] - 50, last_y + 200))
        spikes.append((spike_x, spike_y))
        last_y = spike_y

generate_spikes()

def shrinking_circle_transition(screen, bird_rect, color, speed):
    radius = bird_rect.width // 2
    center = bird_rect.center

# Game state flags
start_menu = True
playing = False
game_over = False
score = 0

DISPLAY.fill((231, 205, 183))

startMessage = font_small.render("Hamza", True, (171, 145, 123))
DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, DISPLAY.get_height()/2 - startMessage.get_height()/2))

pygame.display.update()

        # Wait for 3 seconds
pygame.time.delay(2000)


# Main game loop
while True:
    DISPLAY.fill((231, 205, 183))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start_menu:
                    start_menu = False
                    playing = True
                elif game_over:
                    game_over = False
                    playing = True
                    # Reset game state
                    x = 100
                    y = 100
                    velocity_y = 0
                    coin.collected = False
                    score = 0
                    generate_spikes()
        if event.type == pygame.MOUSEBUTTONDOWN and start_menu:
            if start_button_rect.collidepoint(event.pos):
                start_menu = False
                playing = True
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if start_button_rect.collidepoint(event.pos):
                game_over = False
                playing = True
                # Reset game state
                x = 100
                y = 100
                velocity_y = 0
                coin.collected = False
                score = 0
                generate_spikes()

    if start_menu:
        # Draw start button


        DISPLAY.blit(start_button_img, start_button_rect)
        start_text = font_small.render("Start", True, (0, 0, 0))
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        DISPLAY.blit(start_text, start_text_rect)
        
        # Draw name.png image above the start button
        DISPLAY.blit(name_img, name_img_rect)

    elif playing:
        # Game logic and rendering while playing
        if coin.collected:
            prev_coin_pos = (coin.x, coin.y)
            coin_x = prev_coin_pos[0] + coin_distance
            if coin_x + 30 < WINDOW_SIZE[0]:
                coin_y = random.randint(50, WINDOW_SIZE[1] - 50)
                coin = Coin(coin_x, coin_y)
            else:
                coin_y = random.randint(50, WINDOW_SIZE[1] - 50)
                coin_x = random.randint(0, WINDOW_SIZE[0] - 30)
                coin = Coin(coin_x, coin_y)
            generate_spikes()
            score += 1  # Increment score when a coin is collected

        coin.draw(DISPLAY)

        bird_hitbox = pygame.Rect(x + 10, y + 10, bird_hitbox_width, bird_hitbox_height)

        for spike_pos in spikes:
            if spike_pos[0] == 0:
                DISPLAY.blit(spike_L_image, spike_pos)
            else:
                DISPLAY.blit(spike_R_image, spike_pos)

        for spike_pos in spikes:
            spike_rect = pygame.Rect(spike_pos[0], spike_pos[1], spike_R_image.get_width(),
                                     spike_R_image.get_height())
            if bird_hitbox.colliderect(spike_rect):
                game_over = True
                playing = False
                break

        if coin.rect.colliderect(bird_hitbox) and not coin.collected:
            coin.collected = True

        if x + bird_animation[animation_frame].get_width() >= DISPLAY.get_width() or x <= 0:
            flip = not flip

        rotated_bird = pygame.transform.rotate(bird_animation[animation_frame], velocity_y * rotOffset)
        if not flip:
            DISPLAY.blit(rotated_bird, (x, y))
        else:
            flipped_bird = pygame.transform.flip(rotated_bird, True, False)
            DISPLAY.blit(flipped_bird, (x, y))

        current_time = time.time()
        if current_time - last_frame_time >= frame_delay:
            animation_frame = (animation_frame + 1) % len(bird_animation)
            last_frame_time = current_time

        x += velocity_x

        if x + bird_animation[animation_frame].get_width() >= DISPLAY.get_width():
            velocity_x = -3
        elif x <= 0:
            velocity_x = 3

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not jumping:
                velocity_y = jump_strength
                jumping = True
        else:
            jumping = False

        velocity_y += acceleration
        y += velocity_y

        # Display score in the upper left corner
        score_text = font_small.render(f"Score: {score}", True, (0, 0, 0))
        DISPLAY.blit(score_text, (10, 10))


    elif game_over:
        # Draw retry button
        DISPLAY.blit(start_button_img, start_button_rect)
        retry_text = font_small.render("Retry", True, (0, 0, 0))
        retry_text_rect = retry_text.get_rect(center=start_button_rect.center)
        DISPLAY.blit(retry_text, retry_text_rect)
        
        # Draw game over message and score
        big_font = pygame.font.Font(font_path, 70) 
        gameOverMessage = big_font.render("Game Over!", True, (171, 145, 123))
        
        DISPLAY.blit(gameOverMessage,
                      (DISPLAY.get_width() / 2 - gameOverMessage.get_width() / 2,
                       20))
        scoreMessage = font_small.render(f"Score: {score}", True, (171, 145, 123))
        DISPLAY.blit(scoreMessage, (DISPLAY.get_width() / 2 - scoreMessage.get_width() / 2,
                                    90))

    pygame.display.update()
    clock.tick(60)
