from button import Button
import pygame
import random

class Game:
    def __init__(self, screen, user, level):
        self.screen = screen
        self.user = user
        self.level = level
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        # Load assets
        self.car_image = pygame.image.load("assets/car.png").convert_alpha()
        self.obstacle_image = pygame.image.load("assets/obstacle.png").convert_alpha()
        self.coin_image = pygame.image.load("assets/coin.png").convert_alpha()
        self.gem_image = pygame.image.load("assets/gem.png").convert_alpha()

        # Scale assets for consistency
        self.car_image = pygame.transform.scale(self.car_image, (40, 80))
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (40, 80))
        self.coin_image = pygame.transform.scale(self.coin_image, (20, 20))
        self.gem_image = pygame.transform.scale(self.gem_image, (20, 20))

        # Initialize game objects
        self.car = pygame.Rect(230, 400, 40, 80)  # Car's initial position and size
        self.obstacles = []  # List to hold obstacle positions
        self.collectibles = []  # List to hold collectible positions
        self.score = 0  # Initialize score

    def spawn_obstacle(self):
        """Spawn obstacles randomly."""
        if random.randint(1, 30) == 1:
            self.obstacles.append(pygame.Rect(random.randint(0, 460), -80, 40, 80))

    def spawn_collectible(self):
        """Spawn collectibles randomly (coin or gem)."""
        if random.randint(1, 50) == 1:
            collectible_type = random.choice(["coin", "gem"])
            image = self.coin_image if collectible_type == "coin" else self.gem_image
            self.collectibles.append({"rect": pygame.Rect(random.randint(0, 460), -20, 20, 20), "type": collectible_type, "image": image})

    def check_collisions(self):
        """Check for collisions between the car and obstacles/collectibles."""
        for obstacle in self.obstacles:
            if self.car.colliderect(obstacle):
                self.running = False
                return "game_over"
        for collectible in self.collectibles[:]:
            if self.car.colliderect(collectible["rect"]):
                self.score += 1 if collectible["type"] == "coin" else 2  # Coin = 1, Gem = 2 points
                self.collectibles.remove(collectible)

    def run(self):
        """Main game loop."""
        while self.running:
            self.screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Pause button
            pause_button = Button(
                image=None, pos=(450, 50),
                text_input="Pause", font=self.font, base_color="#d7fcd4", hovering_color="black")
            pause_button.changeColor(mouse_pos)
            pause_button.update(self.screen)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and pause_button.checkForInput(mouse_pos):
                    return "pause"

            # Handle car movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.car.x > 0:
                self.car.x -= 10
            if keys[pygame.K_RIGHT] and self.car.x < 460:
                self.car.x += 10

            # Spawn obstacles and collectibles
            self.spawn_obstacle()
            self.spawn_collectible()

            # Move and draw obstacles
            for obstacle in self.obstacles[:]:
                obstacle.y += 10  # Move obstacle downward
                if obstacle.y > 500:  # Remove obstacle if it goes off-screen
                    self.obstacles.remove(obstacle)
                else:
                    self.screen.blit(self.obstacle_image, (obstacle.x, obstacle.y))

            # Move and draw collectibles
            for collectible in self.collectibles[:]:
                collectible["rect"].y += 8  # Move collectible downward
                if collectible["rect"].y > 500:  # Remove collectible if it goes off-screen
                    self.collectibles.remove(collectible)
                else:
                    self.screen.blit(collectible["image"], (collectible["rect"].x, collectible["rect"].y))

            # Check for collisions
            collision_result = self.check_collisions()
            if collision_result == "game_over":
                return collision_result

            # Draw car
            self.screen.blit(self.car_image, (self.car.x, self.car.y))

            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(30)
