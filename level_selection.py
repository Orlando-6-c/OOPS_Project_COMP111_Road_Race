from button import Button
import pygame
from utils import get_font

bg = pygame.image.load("assets/level.png")

class LevelSelection:
    def __init__(self, screen, user):
        self.screen = screen
        self.user = user
        self.font = get_font(30)
        self.level_buttons = [
            {"label": "Level 1", "unlocked": True},
            {"label": "Level 2", "unlocked": False},
            {"label": "Level 3", "unlocked": False},
        ]

    def update_unlocks(self, score):
        """Unlock levels based on the player's score."""
        if score >= 10:
            self.level_buttons[1]["unlocked"] = True
        if score >= 20:
            self.level_buttons[2]["unlocked"] = True

    def run(self, score):
        """Run the level selection screen."""
        self.update_unlocks(score)

        while True:
            self.screen.blit(bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Back button
            back_button = Button(
                image=None, pos=(50, 50),
                text_input="Back", font=get_font(20), base_color="#d7fcd4", hovering_color="black")

            back_button.changeColor(mouse_pos)
            back_button.update(self.screen)

            # Level buttons
            level_buttons_instances = []  # Track level button instances
            for idx, level in enumerate(self.level_buttons):
                button_color = "#d7fcd4" if level["unlocked"] else "gray"
                level_button = Button(
                    image=None, pos=(250, 150 + idx * 50),
                    text_input=level["label"], font=get_font(30), base_color=button_color, hovering_color="black")
                level_button.changeColor(mouse_pos)
                level_button.update(self.screen)
                level_buttons_instances.append((level_button, level))  # Store button and level info

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_pos):
                        return "back"
                    for button_instance, level in level_buttons_instances:
                        if button_instance.checkForInput(mouse_pos) and level["unlocked"]:
                            return level["label"].lower().replace(" ", "_")

            pygame.display.flip()
