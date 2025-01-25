from base_screen import BaseScreen
from button import Button
from utils import get_font
import pygame
bg=pygame.image.load("../assets/bg_login.png")
class LoginScreen(BaseScreen):
    def __init__(self, screen, login_system):
        super().__init__(screen)
        self.login_system = login_system
        self.username = ""
        self.password = ""
        self.active_field = None
        self.mode = "login"  # "login" or "register"
        self.error_message = ""

    def run(self):
        while True:
            self.screen.blit(bg,(0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Title
            title_text = get_font(40).render(
                "LOGIN" if self.mode == "login" else "REGISTER", True, (255, 255, 255)
            )
            title_rect = title_text.get_rect(center=(250, 50))
            self.screen.blit(title_text, title_rect)

            # Username and Password Fields
            username_text = get_font(20).render("Username:", True, (255, 255, 255))
            self.screen.blit(username_text, (40, 120))
            username_box = pygame.Rect(220, 120, 200, 30)
            pygame.draw.rect(self.screen, (255, 255, 255), username_box, 2)
            username_input = get_font(20).render(self.username, True, (255, 255, 255))
            self.screen.blit(username_input, (username_box.x + 5, username_box.y + 5))

            password_text = get_font(20).render("Password:", True, (255, 255, 255))
            self.screen.blit(password_text, (40, 180))
            password_box = pygame.Rect(220, 180, 200, 30)
            pygame.draw.rect(self.screen, (255, 255, 255), password_box, 2)
            password_input = get_font(20).render("*" * len(self.password), True, (255, 255, 255))
            self.screen.blit(password_input, (password_box.x + 5, password_box.y + 5))

            # Error Message
            if self.error_message:
                error_text = get_font(10).render(self.error_message, True, (255, 0, 0))
                self.screen.blit(error_text, (50, 250))

            # Buttons
            login_button = Button(
                None, (250, 300), "Login", get_font(20), "#d7fcd4", "black"
            )
            register_button = Button(
                None, (250, 360), "Create Account", get_font(20), "#d7fcd4", "black"
            )
            quit_button = Button(None, (250, 420), "Quit", get_font(20), "#d7fcd4", "black")
            self.buttons = [login_button, register_button, quit_button]
            self.draw_buttons(mouse_pos)

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_box.collidepoint(event.pos):
                        self.active_field = "username"
                    elif password_box.collidepoint(event.pos):
                        self.active_field = "password"
                    elif login_button.checkForInput(mouse_pos):
                        if not self.username or not self.password:
                            self.error_message = "Please enter both username and password."
                        else:
                            success, message = self.login_system.login(self.username, self.password)
                            if success:
                                return "main_menu"
                            else:
                                self.error_message = message
                    elif register_button.checkForInput(mouse_pos):
                        if not self.username or not self.password:
                            self.error_message = "Please enter both username and password."
                        else:
                            success, message = self.login_system.register(self.username, self.password)
                            if success:
                                self.mode = "login"
                                self.error_message = "Account created successfully. Please log in."
                            else:
                                self.error_message = message
                    elif quit_button.checkForInput(mouse_pos):
                        return "quit"
                if event.type == pygame.KEYDOWN:
                    if self.active_field == "username":
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            self.username += event.unicode
                    elif self.active_field == "password":
                        if event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                        else:
                            self.password += event.unicode

            pygame.display.flip()
