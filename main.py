import pygame
import random

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

# Load background image
background_image = pygame.image.load('game_background.jpg')

# Fonts
menu_font = pygame.font.Font(None, 36)
score_font = pygame.font.Font(None, 24)

clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

# FallingObject class
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, obj_type):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 2

    def update(self):
        self.rect.y += self.speed

# Function to show main menu
def show_main_menu():
    screen.fill(BLACK)
    title_text = menu_font.render("Catch the Falling Objects", True, WHITE)
    screen.blit(title_text, (200, 200))
    start_text = menu_font.render("1. Start Game", True, WHITE)
    screen.blit(start_text, (300, 300))
    high_scores_text = menu_font.render("2. High Scores", True, WHITE)
    screen.blit(high_scores_text, (300, 350))
    exit_text = menu_font.render("3. Exit", True, WHITE)
    screen.blit(exit_text, (300, 400))
    pygame.display.flip()

# Function to show high scores
def show_high_scores():
    screen.fill(BLACK)
    title_text = menu_font.render("High Scores", True, WHITE)
    screen.blit(title_text, (350, 50))

    # Example high scores (replace with your logic to load actual high scores)
    high_scores = [
        ("Player1", 0),
        ("Player2", 0),
        ("Player3", 0),
    ]

    y_offset = 150
    for i, (player, score) in enumerate(high_scores):
        score_text = score_font.render(f"{i + 1}. {player}: {score}", True, WHITE)
        screen.blit(score_text, (300, y_offset))
        y_offset += 50

    return_text = menu_font.render("Press any key to return to main menu", True, WHITE)
    screen.blit(return_text, (200, 500))
    pygame.display.flip()

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
    all_sprites = pygame.sprite.Group()
    falling_objects = pygame.sprite.Group()
    power_ups = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    score = 0
    missed = 0
    max_missed = 40
    level = 1
    level_speed_increase = 0.5

    running = True
    spawn_counter = 0

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
            falling_object = FallingObject(obj_type)
            falling_objects.add(falling_object)
            all_sprites.add(falling_object)

        # Create power-ups
        if random.randint(1, 500) == 1 and len(power_ups) == 0:
            power_up = PowerUp()
            power_ups.add(power_up)
            all_sprites.add(power_up)

        spawn_counter += 1

        # Update sprites
        all_sprites.update()

        # Check collisions with player
        collisions = pygame.sprite.spritecollide(player, falling_objects, True)
        for obj in collisions:
            score += 1

        # Check collisions with power-ups
        power_up_collisions = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in power_up_collisions:
            # Implement power-up effects here
            pass

        # Check missed objects
        for obj in falling_objects:
            if obj.rect.y > SCREEN_HEIGHT:
                missed += 1
                obj.kill()

        # Increase level difficulty
        if missed >= max_missed:
            running = False

        # Draw everything
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        score_text = score_font.render(f"Score: {score}  Missed: {missed}  Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    screen.fill(BLACK)
    game_over_text = menu_font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (350, 250))
    final_score_text = menu_font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(final_score_text, (325, 300))
    return_text = menu_font.render("Press any key to return to main menu", True, WHITE)
    screen.blit(return_text, (200, 350))
    pygame.display.flip()

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
    show_main_menu()
    high_scores_updated = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    start_game()
                    if not high_scores_updated:
                        show_high_scores()
                        high_scores_updated = True
                    show_main_menu()
                elif event.key == pygame.K_2:
                    show_high_scores()
                    show_main_menu()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()

if __name__ == "__main__":
    main()

pygame.quit()
