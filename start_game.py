from button import Button
import pygame
import json
from utils import get_font

bg = pygame.image.load("assets/bg.png")

class StartGame:
    def __init__(self, screen):
        self.screen = screen
        self.font = get_font(20)
        self.title_font = get_font(40)
        self.existing_users = self.load_users()
        self.text_active = False
        self.username = ""

    def load_users(self):
        try:
            with open("leaderboard.json", "r") as file:
                leaderboard = json.load(file)
                return [entry["player"] for entry in leaderboard]
        except FileNotFoundError:
            return []

    def run(self):
        while True:
            self.screen.blit(bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Title text
            title_text = self.title_font.render("START GAME", True, "#b68f40")
            title_rect = title_text.get_rect(center=(250, 50))
            self.screen.blit(title_text, title_rect)

            # Buttons for new user, existing user, and back
            new_user_button = Button(
                image=None, pos=(250, 120),
                text_input="New User", font=get_font(30), base_color="#d7fcd4", hovering_color="black")
            existing_user_button = Button(
                image=None, pos=(250, 200),
                text_input="Existing User", font=get_font(30), base_color="#d7fcd4", hovering_color="black")
            back_button = Button(
                image=None, pos=(250, 450),
                text_input="Back", font=get_font(20), base_color="#d7fcd4", hovering_color="black")

            # Draw buttons
            for button in [new_user_button, existing_user_button, back_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            # Text input for new user
            if self.text_active:
                pygame.draw.rect(self.screen, (255, 255, 255), (150, 300, 200, 50), 2)
                user_text = self.font.render(self.username, True, (255, 255, 255))
                self.screen.blit(user_text, (160, 310))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                # Mouse click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if new_user_button.checkForInput(mouse_pos):
                        self.text_active = True  # Activate text input
                        self.username = ""  # Reset username field
                    elif existing_user_button.checkForInput(mouse_pos):
                        self.text_active = False
                    elif back_button.checkForInput(mouse_pos):
                        return "back"

                    # Handle clicks on existing user buttons
                    for idx, user in enumerate(self.existing_users):
                        user_button = Button(
                            image=None, pos=(250, 260 + idx * 20),
                            text_input=user, font=get_font(20), base_color="#d7fcd4", hovering_color="black")
                        if user_button.checkForInput(mouse_pos):
                            return user  # Return the selected user's name

                # Keyboard events for new user input
                if event.type == pygame.KEYDOWN and self.text_active:
                    if event.key == pygame.K_RETURN:  # Confirm username
                        if self.username.strip():  # Ensure the name is not empty
                            return self.username  # Proceed with the entered username
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode

            # Display existing user buttons
            if not self.text_active and self.existing_users:
                for idx, user in enumerate(self.existing_users):
                    user_button = Button(
                        image=None, pos=(250, 260 + idx * 20),
                        text_input=user, font=get_font(20), base_color="#d7fcd4", hovering_color="black")
                    user_button.changeColor(mouse_pos)
                    user_button.update(self.screen)

            pygame.display.flip()
