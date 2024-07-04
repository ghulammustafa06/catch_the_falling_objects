import pygame
import random

pygame.init()

# Load background image or set background color
background_image = pygame.image.load('game_background.jpg')  
# background_color = (135, 206, 235)  # Sky blue color

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catch the Falling Objects")

player = pygame.Rect(375, 500, 50, 50)  # Player as a rectangle
player_speed = 0  # Initial speed
player_acceleration = 0.5  # Acceleration rate

class FallingObject:
    def __init__(self, obj_type):
        self.rect = pygame.Rect(random.randint(0, 750), 0, 50, 50)
        self.type = obj_type
        self.speed = self.set_speed(obj_type)
    
    def set_speed(self, obj_type):
        if obj_type == 'normal':
            return 2 
        elif obj_type == 'fast':
            return 3  
        elif obj_type == 'slow':
            return 1  
        elif obj_type == 'big':
            return 1
        elif obj_type == 'small':
            return 2  
    
    def update(self):
        self.rect.y += self.speed

class PowerUp:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, 750), 0, 30, 30)
        self.type = random.choice(['score_up', 'speed_up', 'slow_down'])
        self.speed = 2  # Fixed speed for power-ups
    
    def update(self):
        self.rect.y += self.speed

def apply_power_up(type):
    global player_speed, falling_objects_speed
    if type == 'score_up':
        global score
        score += 5 
    elif type == 'speed_up':
        player_speed += 2  
    elif type == 'slow_down':
        for obj in falling_objects:
            obj.speed -= 1  

falling_objects = []
power_ups = []
score = 0
missed = 0
max_missed = 40 

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
    global player, player_speed, falling_objects, power_ups, score, missed
    player = pygame.Rect(375, 500, 50, 50)
    player_speed = 0
    falling_objects = []
    power_ups = []
    score = 0
    missed = 0

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
            player_speed -= player_acceleration
        if keys[pygame.K_RIGHT]:
            player_speed += player_acceleration

        # Apply friction to slow down gradually when no key is pressed
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if player_speed > 0:
                player_speed -= player_acceleration
            elif player_speed < 0:
                player_speed += player_acceleration

        player.x += player_speed

        # Ensure player stays within screen bounds
        if player.x < 0:
            player.x = 0
            player_speed = 0
        elif player.x > 750:
            player.x = 750
            player_speed = 0

        # Create falling objects
        if random.randint(1, 20) == 1 and len(falling_objects) < 5:  # Limit to 5 objects at a time
            obj_type = random.choice(['normal', 'fast', 'slow', 'big', 'small'])
            falling_objects.append(FallingObject(obj_type))

        # Create power-ups
        if random.randint(1, 500) == 1 and len(power_ups) == 0:  # Chance to spawn a power-up
            power_ups.append(PowerUp())

        # Update power-ups
        for power_up in power_ups:
            power_up.update()
            if player.colliderect(power_up.rect):
                apply_power_up(power_up.type)
                power_ups.remove(power_up)
        
        # Update falling objects
        for obj in falling_objects:
            obj.update()
            if player.colliderect(obj.rect):
                score += 1
                catch_sound.play()
                falling_objects.remove(obj)
            elif obj.rect.y > 600:
                missed += 1
                falling_objects.remove(obj)

        # Check game over condition
        if missed >= max_missed:
            show_game_over_screen(score)
            reset_game()
            show_start_screen()

        # Draw background image or fill with color
        screen.blit(background_image, (0, 0))  # Comment this line if using a solid color
        # screen.fill(background_color)  # Uncomment this line if using a solid color

        # Draw player
        pygame.draw.rect(screen, (0, 255, 0), player)

        # Draw falling objects
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

        # Draw power-ups
        for power_up in power_ups:
            if power_up.type == 'score_up':
                color = (255, 255, 0)  # Yellow for score up
            elif power_up.type == 'speed_up':
                color = (0, 255, 0)  # Green for speed up
            elif power_up.type == 'slow_down':
                color = (0, 0, 255)  # Blue for slow down
            pygame.draw.rect(screen, color, power_up.rect)

        # Display score and missed count
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score} Missed: {missed}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

pygame.quit()
