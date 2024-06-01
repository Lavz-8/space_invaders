import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 457

# Colors
WHITE = (255, 255, 255)            
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Define the path to the images directory
image_dir = os.path.join(os.path.dirname(__file__), 'image')

# Load your background image
background_image = pygame.image.load(os.path.join(image_dir, 'background.jpg'))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load spaceship image
spaceship_image = pygame.image.load(os.path.join(image_dir, 'spaceship.png'))
spaceship_width = 64
spaceship_height = 64
spaceship_x = (SCREEN_WIDTH - spaceship_width) / 2
spaceship_y = SCREEN_HEIGHT - spaceship_height - 10
spaceship_speed = 5

# Load alien image
alien_image = pygame.image.load(os.path.join(image_dir, 'alien.png'))
alien_width = 64
alien_height = 64
alien_speed = 3
alien_drop_speed = 30
aliens = []

# Define the path to the audio directory
audio_dir = os.path.join(os.path.dirname(__file__), 'audio')

# Load shooting sound
shooting_sound = pygame.mixer.Sound(os.path.join(audio_dir, 'shooting.mp3'))

# Bullet settings  
bullet_width = 5
bullet_height = 20
bullet_speed = 10
bullets = []

# Create font
font = pygame.font.SysFont(None, 55)

# Function to create a new alien
def create_alien():
    x = random.randint(0, SCREEN_WIDTH - alien_width)
    y = random.randint(-100, -40)
    return pygame.Rect(x, y, alien_width, alien_height)

# Add initial aliens
for _ in range(5):
    aliens.append(create_alien())

# Function to draw text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Game loop
running = True
score = 0

while running:
    screen.fill((0, 0, 0))  # Fill the screen with black color

    # Draw background
    screen.blit(background_image, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship_x < SCREEN_WIDTH - spaceship_width:
        spaceship_x += spaceship_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 3:  # Limit the number of bullets on screen
            bullet_x = spaceship_x + spaceship_width / 2 - bullet_width / 2
            bullet_y = spaceship_y
            bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
            shooting_sound.play()  # Play shooting sound

    # Move bullets
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Move aliens
    for alien in aliens:
        alien.y += alien_speed
        if alien.y > SCREEN_HEIGHT:
            aliens.remove(alien)
            aliens.append(create_alien())
        if alien.colliderect(pygame.Rect(spaceship_x, spaceship_y, spaceship_width, spaceship_height)):
            running = False

    # Check for collisions
    for alien in aliens:
        for bullet in bullets:
            if alien.colliderect(bullet):
                bullets.remove(bullet)
                aliens.remove(alien)
                aliens.append(create_alien())
                score += 1
                break

    # Draw spaceship
    screen.blit(spaceship_image, (spaceship_x, spaceship_y))

    # Draw aliens
    for alien in aliens:
        screen.blit(alien_image, alien.topleft)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

    # Draw score
    draw_text(f"Score: {score}", font, GREEN, screen, 10, 10)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
