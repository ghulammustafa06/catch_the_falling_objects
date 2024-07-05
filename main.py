import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Fonts
menu_font = pygame.font.Font(None, 36)  # Font for menu texts
score_font = pygame.font.Font(None, 24)  # Font for score display

clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load('game_background.jpg')

# Load sounds
catch_sound = pygame.mixer.Sound('catch.mp3')  # Sound for catching objects
game_over_sound = pygame.mixer.Sound('game_over.wav')  # Sound for game over
power_up_sound = pygame.mixer.Sound('power_up.wav')  # Sound for power-ups

# Load music
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.3)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Player image surface
        self.image.fill(GREEN)  # Player color (can be replaced with image)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2  # Starting position
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8  # Movement speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed  # Move left
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed  # Move right

# FallingObject class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, obj_type):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Object image surface
        self.image.fill(RED)  # Object color (can be replaced with image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  # Random x position
        self.rect.y = -self.rect.height  # Start above the screen
        self.speed = random.randint(2, 4)  # Falling speed

    def update(self):
        self.rect.y += self.speed  # Move object down

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Power-up image surface
        self.image.fill(YELLOW)  # Power-up color (can be replaced with image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)  # Random x position
        self.rect.y = -self.rect.height  # Start above the screen
        self.speed = 2  # Falling speed

    def update(self):
        self.rect.y += self.speed  # Move power-up down

# Function to show main menu
def show_main_menu():
    screen.fill(BLACK)  # Clear screen with black
    title_text = menu_font.render("Catch the Falling Objects", True, WHITE)  # Title text
    screen.blit(title_text, (200, 200))  # Position title text
    start_text = menu_font.render("1. Start Game", True, WHITE)  # Start game option
    screen.blit(start_text, (300, 300))  # Position start text
    high_scores_text = menu_font.render("2. High Scores", True, WHITE)  # High scores option
    screen.blit(high_scores_text, (300, 350))  # Position high scores text
    exit_text = menu_font.render("3. Exit", True, WHITE)  # Exit option
    screen.blit(exit_text, (300, 400))  # Position exit text
    pygame.display.flip()  # Update display

# Function to show high scores
def show_high_scores():
    screen.fill(BLACK)  # Clear screen with black
    title_text = menu_font.render("High Scores", True, WHITE)  # Title text
    screen.blit(title_text, (350, 50))  # Position title text

    # Example high scores (replace with actual high scores logic)
    high_scores = [
        ("Player1", 0),
        ("Player2", 0),
        ("Player3", 0),
    ]

    y_offset = 150
    for i, (player, score) in enumerate(high_scores):
        score_text = score_font.render(f"{i + 1}. {player}: {score}", True, WHITE)  # Format high score text
        screen.blit(score_text, (300, y_offset))  # Position high score text
        y_offset += 50

    return_text = menu_font.render("Press any key to return to main menu", True, WHITE)  # Return instruction
    screen.blit(return_text, (200, 500))  # Position return text
    pygame.display.flip()  # Update display

    # Wait for user input to return to main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Function to start the game
def start_game():
    all_sprites = pygame.sprite.Group()  # Sprite group for all game objects
    falling_objects = pygame.sprite.Group()  # Sprite group for falling objects
    power_ups = pygame.sprite.Group()  # Sprite group for power-ups

    player = Player()  # Create player object
    all_sprites.add(player)  # Add player to all sprites group

    score = 0  # Initial score
    missed = 0  # Initial missed count
    max_missed = 40  # Maximum misses allowed before game over
    level = 1  # Initial game level
    level_speed_increase = 0.5  # Speed increase per level

    pygame.mixer.music.play(loops=-1)  # Play background music

    running = True
    spawn_counter = 0  # Counter for object spawning

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    return

        # Create falling objects
        if spawn_counter % 60 == 0 and len(falling_objects) < 5 + level:
            obj_type = random.choice(['normal', 'fast', 'slow', 'big', 'small'])
            falling_object = FallingObject(obj_type)  # Create falling object
            falling_objects.add(falling_object)  # Add to falling objects group
            all_sprites.add(falling_object)  # Add to all sprites group

        # Create power-ups
        if random.randint(1, 500) == 1 and len(power_ups) == 0:
            power_up = PowerUp()  # Create power-up object
            power_ups.add(power_up)  # Add to power-ups group
            all_sprites.add(power_up)  # Add to all sprites group

        spawn_counter += 1  # Increment spawn counter

        # Update sprites
        all_sprites.update()

        # Check collisions with player
        collisions = pygame.sprite.spritecollide(player, falling_objects, True)
        for obj in collisions:
            score += 1  # Increase score
            catch_sound.play()  # Play catch sound effect

        # Check collisions with power-ups
        power_up_collisions = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in power_up_collisions:
            # Implement power-up effects here (if any)
            power_up_sound.play()  # Play power-up sound effect

        # Check missed objects
        for obj in falling_objects:
            if obj.rect.y > SCREEN_HEIGHT:
                missed += 1  # Increase missed count
                obj.kill()  # Remove object from sprites

        # End game conditions
        if missed >= max_missed:
            running = False

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw background image
        all_sprites.draw(screen)  # Draw all sprites on screen

        # Display score and game stats
        score_text = score_font.render(f"Score: {score}  Missed: {missed}  Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()  # Update display
        clock.tick(60)  # Cap frame rate at 60 FPS

    pygame.mixer.music.stop()  # Stop background music

    # Game over screen
    screen.fill(BLACK)  # Clear screen with black
    game_over_text = menu_font.render("Game Over", True, WHITE)  # Game over text
    screen.blit(game_over_text, (350, 250))  # Position game over text
    final_score_text = menu_font.render(f"Final Score: {score}", True, WHITE)  # Final score text
    screen.blit(final_score_text, (325, 300))  # Position final score text
    return_text = menu_font.render("Press any key to return to main menu", True, WHITE)  # Return instruction
    screen.blit(return_text, (200, 350))  # Position return text
    pygame.display.flip()  # Update display

    # Wait for user input to return to main menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Main game loop
def main():
    show_main_menu()  # Show main menu initially
    high_scores_updated = False  # Flag to track if high scores have been updated
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    start_game()  # Start game option
                    if not high_scores_updated:
                        show_high_scores()  # Show high scores if not updated yet
                        high_scores_updated = True  # Update high scores flag
                    show_main_menu()  # Return to main menu
                elif event.key == pygame.K_2:
                    show_high_scores()  # Show high scores option
                    show_main_menu()  # Return to main menu
                elif event.key == pygame.K_3:
                    pygame.quit()  # Exit game option
                    exit()

if __name__ == "__main__":
    main()

pygame.quit()  # Quit Pygame
