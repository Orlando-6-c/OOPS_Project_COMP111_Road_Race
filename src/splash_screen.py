import pygame
import time
from base_screen import BaseScreen

class SplashScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.logo = pygame.image.load("../assets/splash_logo.png").convert_alpha()  # Your splash logo
        self.bg = pygame.image.load("../assets/splash_bg.png") # Background color (black)
        self.duration = 3  # Splash screen duration in seconds
        self.fade_speed = 5  # Fade-in/out speed

    def fade_in(self):
        """Fade in the splash logo."""
        for alpha in range(0, 256, self.fade_speed):
            self.screen.blit(self.bg,(0,0))
            self.logo.set_alpha(alpha)
            self.screen.blit(self.logo, self.logo.get_rect(center=(250, 250)))
            pygame.display.flip()
            pygame.time.delay(10)

    def fade_out(self):
        """Fade out the splash logo."""
        for alpha in range(255, -1, -self.fade_speed):
            self.screen.blit(self.bg,(0,0))
            self.logo.set_alpha(alpha)
            self.screen.blit(self.logo, self.logo.get_rect(center=(250, 250)))
            pygame.display.flip()
            pygame.time.delay(10)

    def run(self):
        """Display the splash animation."""
        self.fade_in()
        time.sleep(self.duration)  # Keep the splash screen visible for the duration
        self.fade_out()
