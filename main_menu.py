import pygame
from utils import get_font
from button import Button
from base_screen import BaseScreen

class MainMenu(BaseScreen):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg = pygame.image.load("assets/bg.png")

    def run(self):
        while True:
            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Title
            title = get_font(40).render("Main Menu", True, (255, 255, 255))
            title_rect = title.get_rect(center=(250, 50))
            self.screen.blit(title, title_rect)

            # Buttons
            start_button = Button(None, (250, 200), "Start Game", get_font(30), "#d7fcd4", "black")
            leaderboard_button = Button(None, (250, 300), "Leaderboard", get_font(30), "#d7fcd4", "black")
            quit_button = Button(None, (250, 400), "Quit", get_font(30), "#d7fcd4", "black")

            buttons = [start_button, leaderboard_button, quit_button]
            for button in buttons:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.checkForInput(mouse_pos):
                        return "start_game"
                    elif leaderboard_button.checkForInput(mouse_pos):
                        return "leaderboard"
                    elif quit_button.checkForInput(mouse_pos):
                        return "quit"

            pygame.display.flip()
