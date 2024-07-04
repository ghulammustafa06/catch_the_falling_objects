import pygame
import random

pygame.init()

# Load background image or set background color
background_image = pygame.image.load('game_background.jpg')  
# background_color = (135, 206, 235)  # Sky blue color

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Falling Objects")

player = pygame.Rect(375, 500, 50, 50)  # Player as a rectangle

class FallingObject:
    def __init__(self, obj_type):
        self.rect = pygame.Rect(random.randint(0, 750), 0, 50, 50)
        self.type = obj_type
        self.speed = self.set_speed(obj_type)
    
    def set_speed(self, obj_type):
        if obj_type == 'normal':
            return 2  # Slowed down
        elif obj_type == 'fast':
            return 3  # Slowed down
        elif obj_type == 'slow':
            return 1  # Slowed down
        elif obj_type == 'big':
            return 1
        elif obj_type == 'small':
            return 2  # Slowed down
    
    def update(self):
        self.rect.y += self.speed

falling_objects = []

# Placeholder sounds using Pygame's built-in beep functionality
pygame.mixer.init()
catch_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00@\x1f\x00\x00@\x1f\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00'))
game_over_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00@\x1f\x00\x00@\x1f\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00'))

def show_start_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Catch the Falling Objects", True, (255, 255, 255))
    screen.blit(text, (50, 250))
    font = pygame.font.Font(None, 36)
    text = font.render("Press any key to start", True, (255, 255, 255))
    screen.blit(text, (250, 350))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(final_score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (300, 250))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    screen.blit(text, (300, 350))
    text = font.render("Press any key to restart", True, (255, 255, 255))
    screen.blit(text, (300, 400))
    pygame.display.flip()
    game_over_sound.play()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

def reset_game():
    global player, falling_objects, score, missed, max_missed
    player = pygame.Rect(375, 500, 50, 50)
    falling_objects = []
    score = 0
    missed = 0
    max_missed = 40  

reset_game()
show_start_screen()

running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5

        if random.randint(1, 20) == 1:  # Randomly create falling objects
            obj_type = random.choice(['normal', 'fast', 'slow', 'big', 'small'])
            falling_objects.append(FallingObject(obj_type))

        for obj in falling_objects:
            obj.update()
            if player.colliderect(obj.rect):
                score += 1
                catch_sound.play()
                falling_objects.remove(obj)
            elif obj.rect.y > 600:
                missed += 1
                falling_objects.remove(obj)

        if missed >= max_missed:
            show_game_over_screen(score)
            reset_game()
            show_start_screen()

        # Draw background image or fill with color
        screen.blit(background_image, (0, 0))  
        # screen.fill(background_color)  

        pygame.draw.rect(screen, (0, 255, 0), player)
        for obj in falling_objects:
            if obj.type == 'normal':
                color = (255, 0, 0)
            elif obj.type == 'fast':
                color = (0, 0, 255)
            elif obj.type == 'slow':
                color = (255, 255, 0)
            elif obj.type == 'big':
                color = (0, 255, 255)
            elif obj.type == 'small':
                color = (255, 0, 255)
            pygame.draw.rect(screen, color, obj.rect)

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score} Missed: {missed}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

pygame.quit()
