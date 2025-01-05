from utils import get_font
from button import Button
import pygame
bg_main_menu=pygame.image.load("assets/bg.png")
class MainMenu:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        while True:
            self.screen.blit(bg_main_menu, (0,0))
            mouse_pos = pygame.mouse.get_pos()

            menu_text = get_font(50).render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(250, 100))
            self.screen.blit(menu_text, menu_rect)

            create_player_button = Button(
                image=None, pos=(250, 200),
                text_input="Start", font=get_font(30), base_color="#d7fcd4", hovering_color="black")
            leaderboard_button = Button(
                image=None, pos=(250, 300),
                text_input="Leader Board", font=get_font(30), base_color="#d7fcd4", hovering_color="black")
            quit_button = Button(
                image=None, pos=(250, 400),
                text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="black")

            for button in [create_player_button, leaderboard_button, quit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if create_player_button.checkForInput(mouse_pos):
                        return "start_game"
                    elif leaderboard_button.checkForInput(mouse_pos):
                        return "leaderboard"
                    elif quit_button.checkForInput(mouse_pos):
                        return "quit"

            pygame.display.flip()
