import pygame

class BaseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.small_font = pygame.font.Font(None, 30)

    def draw_back_button(self):
        """Draw a back button on the screen."""
        back_button = pygame.Rect(10, 10, 80, 30)  # Back button size and position
        pygame.draw.rect(self.screen, (255, 255, 255), back_button)
        back_text = self.small_font.render("Back", True, (0, 0, 0))
        self.screen.blit(back_text, (back_button.x + 10, back_button.y + 5))
        return back_button

    def handle_back_event(self, event, back_button):
        """Handle clicks on the back button."""
        if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
            return "back"
        return None
