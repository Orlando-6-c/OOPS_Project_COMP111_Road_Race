from button import Button
import pygame
from utils import get_font
class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)

    def run(self):
        while True:
            self.screen.fill((50, 50, 50))
            mouse_pos = pygame.mouse.get_pos()

            resume_button = Button(
                image=None, pos=(250, 150),
                text_input="Resume", font=get_font(40), base_color="#d7fcd4", hovering_color="black")
            restart_button = Button(
                image=None, pos=(250, 250),
                text_input="Restart", font=get_font(40), base_color="#d7fcd4", hovering_color="black")
            main_menu_button = Button(
                image=None, pos=(250, 350),
                text_input="Main Menu", font=get_font(40), base_color="#d7fcd4", hovering_color="black")

            for button in [resume_button, restart_button, main_menu_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.checkForInput(mouse_pos):
                        return "resume"
                    elif restart_button.checkForInput(mouse_pos):
                        return "restart"
                    elif main_menu_button.checkForInput(mouse_pos):
                        return "main_menu"

            pygame.display.flip()
