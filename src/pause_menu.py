from base_screen import BaseScreen
from button import Button
from utils import get_font
import pygame

class PauseMenu(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            Button(None, (250, 200), "Resume", get_font(30), "#d7fcd4", "black"),
            Button(None, (250, 300), "Restart", get_font(30), "#d7fcd4", "black"),
            Button(None, (250, 400), "Main Menu", get_font(30), "#d7fcd4", "black"),
        ]

    def run(self):
        """Run the pause menu screen."""
        while True:
            self.screen.fill((0, 0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Title
            title = get_font(40).render("PAUSED", True, (255, 255, 255))
            title_rect = title.get_rect(center=(250, 100))
            self.screen.blit(title, title_rect)

            self.draw_buttons(mouse_pos)

            action = self.handle_events(mouse_pos)
            if action in ["resume", "restart", "main menu"]:
                return action

            pygame.display.flip()
