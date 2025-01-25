from base_screen import BaseScreen
from button import Button
from utils import get_font
import pygame
bg=pygame.image.load("../assets/leaderboard.png")
class Leaderboard(BaseScreen):
    def __init__(self, screen, login_system):
        super().__init__(screen)
        self.login_system = login_system

    def run(self):
        """Display the leaderboard screen."""
        leaderboard_data = self.login_system.get_leaderboard()

        while True:
            self.screen.blit(bg,(0, 0))
            mouse_pos = pygame.mouse.get_pos()

            

            # Display top 5 scores
            for idx, entry in enumerate(leaderboard_data[:5]):
                score_text = get_font(25).render(
                    f"{idx + 1}. {entry['player']} - {entry['score']} pts", True, (255, 255, 255)
                )
                self.screen.blit(score_text, (70, 120 + idx * 40))

            # Back button
            back_button = Button(None, (250, 450), "Back", get_font(25), "#d7fcd4", "black")
            back_button.changeColor(mouse_pos)
            back_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_pos):
                        return "back"

            pygame.display.flip()
