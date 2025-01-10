from base_screen import BaseScreen
from button import Button
from utils import get_font
import pygame
import tkinter
from tkinter import messagebox
bg=pygame.image.load("assets/level.png")
class LevelSelection(BaseScreen):
    def __init__(self, screen, player_data):
        super().__init__(screen)
        self.user = player_data
        self.level_buttons = [
            {"label": "Level 1", "unlocked": True, "required_score": 0, "max_score": 15},
            {"label": "Level 2", "unlocked": False, "required_score": 10, "max_score": 20},
            {"label": "Level 3", "unlocked": False, "required_score": 30, "max_score": None},  # No max limit
        ]
        self.current_score = player_data.get("score", 0)

        # Debug: Initialization State
        print(f"Debug: Initialized LevelSelection with score: {self.current_score}")
        print(f"Debug: Initial unlock statuses: {[button['unlocked'] for button in self.level_buttons]}")

    def update_unlocks(self):
        """Unlock levels based on the player's score and sequential progression."""
        # Ensure Level 1 is always unlocked
        self.level_buttons[0]["unlocked"] = True

        for i in range(1, len(self.level_buttons)):
            previous_level = self.level_buttons[i - 1]
            current_level = self.level_buttons[i]

            # Unlock the current level only if the previous level is completed AND the score meets the requirement
            if (
                previous_level["label"].lower() in self.user.get("completed_levels", [])
                and self.current_score >= current_level["required_score"]
            ):
                current_level["unlocked"] = True
            else:
                current_level["unlocked"] = False

            # Debug: Unlock status
            print(
                f"Debug: Level {current_level['label']} unlock status: {'Unlocked' if current_level['unlocked'] else 'Locked'}"
            )


    def show_locked_level_popup(self, required_score):
        """Display a popup message for locked levels."""
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo(
            "Level Locked",
            f"This level will unlock after achieving a score of {required_score} in the previous level."
        )
        root.destroy()

    def run(self):
        """Run the level selection screen."""
        self.update_unlocks()

        while True:
            self.screen.blit(bg,(0, 0))
            mouse_pos = pygame.mouse.get_pos()

          

            # Display current score
            score_text = get_font(25).render(f"Your Score: {self.current_score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(250, 100))
            self.screen.blit(score_text, score_rect)

            # Level Buttons
            buttons = []
            for idx, level in enumerate(self.level_buttons):
                button_color = "#d7fcd4" if level["unlocked"] else "gray"
                level_button = Button(
                    None,
                    (250, 150 + idx * 100),
                    level["label"],
                    get_font(30),
                    button_color,
                    "black",
                )
                buttons.append(level_button)

            # Back Button
            back_button = Button(None, (50, 50), "Back", get_font(20), "#d7fcd4", "black")
            buttons.append(back_button)

            for button in buttons:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_pos):
                        return "back"
                    for idx, level in enumerate(self.level_buttons):
                        if buttons[idx].checkForInput(mouse_pos):
                            if level["unlocked"]:
                                return {"level": level["label"].lower(), "max_score": level["max_score"]}
                            else:
                                self.show_locked_level_popup(level["required_score"])

            pygame.display.flip()
