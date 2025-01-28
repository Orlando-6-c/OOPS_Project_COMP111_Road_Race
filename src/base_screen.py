import pygame
from button import Button

class BaseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []

    def draw_buttons(self, mouse_pos):
        """Draws and updates all buttons."""
        for button in self.buttons:
            button.changeColor(mouse_pos)
            button.update(self.screen)

    def handle_events(self, mouse_pos):
        """Handles button click events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.checkForInput(mouse_pos):
                        return button.text_input.lower()
        return None

    def run(self):
        """Run method to be overridden by derived classes."""
        raise NotImplementedError("Subclasses must implement the run method.")
