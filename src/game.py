import pygame
import random
from pause_menu import PauseMenu    
from button import Button

class Game:
    def __init__(self, screen, player_data, level, max_score=None):
        self.screen = screen
        self.player_data = player_data
        self.level = level
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/font.ttf", 25)
        self.collected_coins = 0
        self.collected_gems = 0
        self.power_up_active = False
        self.power_up_timer = 0
        self.font=pygame.font.Font("assets/font.ttf", 25)

        # Level-specific settings
        self.settings = {
            "level_1": {
                "speed_multiplier": 1,
                "background": "assets/level_1_bg.png",
                "car": "assets/car_level_1.png",
                "obstacle": "assets/obstacle_level_1.png",
                "power_up": None,
            },
            "level_2": {
                "speed_multiplier": 1.5,
                "background": "assets/level_2_bg.png",
                "car": "assets/car_level_2.png",
                "obstacle": "assets/obstacle_level_2.png",
                "power_up": "assets/power_up.png",
            },
            "level_3": {
                "speed_multiplier": 2,
                "background": "assets/level_3_bg.png",
                "car": "assets/car_level_3.png",
                "obstacle": "assets/obstacle_level_3.png",
                "power_up": "assets/power_up.png",
            },
        }

        self.level_config = self.settings[f"level_{level}"]
        self.obstacle_speed = 5 * self.level_config["speed_multiplier"]
        self.collectible_speed = 3 * self.level_config["speed_multiplier"]

        # Load assets
        self.background = pygame.image.load(self.level_config["background"]).convert()
        self.car_image = pygame.image.load(self.level_config["car"]).convert_alpha()
        self.obstacle_image = pygame.image.load(self.level_config["obstacle"]).convert_alpha()
        self.coin_image = pygame.image.load("assets/coin.png").convert_alpha()
        self.gem_image = pygame.image.load("assets/gem.png").convert_alpha()
        self.power_up_image = (
            pygame.image.load(self.level_config["power_up"]).convert_alpha()
            if self.level_config["power_up"]
            else None
        )
        self.collision_sound = pygame.mixer.Sound("assets/collision.wav")
        self.coin_sound = pygame.mixer.Sound("assets/coin_collect.wav")  # Added coin sound
        self.explosion_images = [pygame.image.load(f"assets/tile00{i}.png").convert_alpha() for i in range(7)]
        self.power_up_sound=pygame.mixer.Sound("assets/power_up.wav")
        self.car = pygame.Rect(230, 400, 40, 80)

        # Background positions for scrolling
        self.background_y1 = 0
        self.background_y2 = -self.screen.get_height()

        # Pause Menu
        self.pause_menu = PauseMenu(self.screen)

        # Background music
        pygame.mixer.music.load("assets/background_music.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # Pause button in top-right corner
        self.pause_button = Button(
            None,  # No background for the button
            (350, 20),  # Position (top-right corner)
            "Pause",  # Button text
            self.font,  # Font for the text
            "#FFFFFF",  # Text color (white)
            "black"  # Hover color
        )

        


        # Game objects
        self.obstacles = []
        self.coins = []
        self.gems = []
        self.power_ups = []

    def draw_explosion(self, position):
        """Play explosion animation at the given position."""
        for frame in self.explosion_images:
            self.screen.blit(frame, position)
            pygame.display.flip()
            self.clock.tick(10)  # Adjust the speed of the animation


    def spawn_objects(self):
        """Spawn obstacles, coins, gems, and power-ups."""
        if random.randint(1, 30) == 1:
            x = random.randint(50, 450)
            self.obstacles.append(pygame.Rect(x, -80, 40, 80))

        if random.randint(1, 50) == 1:
            x = random.randint(50, 450)
            self.coins.append(pygame.Rect(x, -20, 20, 20))

        if random.randint(1, 100) == 1:
            x = random.randint(50, 450)
            self.gems.append(pygame.Rect(x, -20, 25, 25))

        if self.level_config["power_up"] and random.randint(1, 150) == 1:
            x = random.randint(50, 450)
            self.power_ups.append(pygame.Rect(x, -20, 30, 30))

    def move_background(self):
        """Scroll the background to create the illusion of forward motion."""
        self.background_y1 += self.obstacle_speed
        self.background_y2 += self.obstacle_speed

        if self.background_y1 >= self.screen.get_height():
            self.background_y1 = -self.screen.get_height()
        if self.background_y2 >= self.screen.get_height():
            self.background_y2 = -self.screen.get_height()

        self.screen.blit(self.background, (0, self.background_y1))
        self.screen.blit(self.background, (0, self.background_y2))

    def move_objects(self, objects, speed):
        """Move objects downward."""
        for obj in objects[:]:
            obj.y += speed
            if obj.y > self.screen.get_height():
                objects.remove(obj)

    def check_collisions(self):
        """Check for collisions with obstacles, coins, gems, and power-ups."""
        for obstacle in self.obstacles[:]:
            if self.car.colliderect(obstacle):
                if not self.power_up_active:
                    self.collision_sound.play()
                    self.draw_explosion(self.car.topleft)
                    return "game_over"

        for coin in self.coins[:]:
            if self.car.colliderect(coin):
                self.collected_coins += 1
                self.coins.remove(coin)
                self.coin_sound.play()  # Play coin collection sound

        for gem in self.gems[:]:
            if self.car.colliderect(gem):
                self.collected_gems += 1
                self.gems.remove(gem)
                self.coin_sound.play()

        for power_up in self.power_ups[:]:
            if self.car.colliderect(power_up):
                self.power_up_active = True
                self.power_up_timer = pygame.time.get_ticks()
                self.power_ups.remove(power_up)
                self.power_up_sound.play()

    def update_power_up(self):
        """Deactivate power-ups after 5 seconds and display timer."""
        if self.power_up_active:
            elapsed_time = (pygame.time.get_ticks() - self.power_up_timer) // 1000
            remaining_time = 5 - elapsed_time

            if remaining_time <= 0:
                self.power_up_active = False
            else:
                immunity_text = self.font.render(f"Immune: {remaining_time}s", True, (0, 255, 0))
                self.screen.blit(immunity_text, (250, 250))

    def run(self):
        while self.running:
            self.spawn_objects()
            self.screen.fill((0, 0, 0))
            self.move_background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.mixer.music.stop()  # Stop music on quit
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button.checkForInput(mouse_pos):
                        action = self.pause_menu.run()
                        if action == "resume":
                            continue
                        elif action == "restart":
                            pygame.mixer.music.stop()  # Stop music on restart
                            return "restart"
                        elif action == "main menu":
                            pygame.mixer.music.stop()  # Stop music on main menu transition
                            return "main menu"

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.car.x > 0:
                self.car.x -= 5
            if keys[pygame.K_RIGHT] and self.car.x < 460:
                self.car.x += 5

            self.move_objects(self.obstacles, self.obstacle_speed)
            self.move_objects(self.coins, self.collectible_speed)
            self.move_objects(self.gems, self.collectible_speed)
            self.move_objects(self.power_ups, self.collectible_speed)

            result = self.check_collisions()
            if result == "game_over":
                pygame.mixer.music.stop()  # Stop music on game over
                return self.collected_coins + self.collected_gems

            self.update_power_up()

            # Draw game elements
            self.screen.blit(self.car_image, self.car.topleft)

            for obstacle in self.obstacles:
                self.screen.blit(self.obstacle_image, obstacle.topleft)
            for coin in self.coins:
                self.screen.blit(self.coin_image, coin.topleft)
            for gem in self.gems:
                self.screen.blit(self.gem_image, gem.topleft)
            for power_up in self.power_ups:
                self.screen.blit(self.power_up_image, power_up.topleft)

            # Draw coin and gem counts
            coins_text = self.font.render(f"Coins: {self.collected_coins}", True, (255, 255, 255))
            gems_text = self.font.render(f"Gems: {self.collected_gems}", True, (255, 255, 255))
            self.screen.blit(coins_text, (10, 10))
            self.screen.blit(gems_text, (10, 40))

            # Draw pause button
            # Draw the pause button
            mouse_pos = pygame.mouse.get_pos()
            self.pause_button.changeColor(mouse_pos)  # Handle hover effect
            self.pause_button.update(self.screen)  # Render the button


            pygame.display.flip()
            self.clock.tick(30)
