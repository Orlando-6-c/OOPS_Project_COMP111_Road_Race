import sys
import pygame
from splash_screen import SplashScreen  # Import the SplashScreen class
from login_screen import LoginScreen
from main_menu import MainMenu
from level_selection import LevelSelection
from game import Game
from leaderboard import Leaderboard
from login_system import LoginSystem


def main():
    pygame.init()  # Initialize Pygame
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Road Race")

    # Show Splash Screen
    splash_screen = SplashScreen(screen)  #Composition happening here
    splash_screen.run()

    login_system = LoginSystem() 

    while True:
        # Display Login Screen
        login_screen = LoginScreen(screen, login_system)
        action = login_screen.run()

        if action == "main_menu":
            while True:
                # Display Main Menu
                main_menu = MainMenu(screen) #COMPOSITION
                menu_action = main_menu.run() 

                if menu_action == "start_game":
                    while True:
                        # Fetch Player Data
                        player_data = login_system.get_logged_in_player_data()

                        # Display Level Selection Screen
                        level_selection = LevelSelection(screen, player_data)
                        selected_level = level_selection.run()

                        if selected_level == "back":
                            break  # Return to the main menu

                        while True:  # Allow level restart
                            # Start the Game
                            game = Game(
                                screen,
                                player_data,
                                int(selected_level["level"].split()[-1]),  # Extract the level number from the dictionary
                                selected_level["max_score"],  # Access max_score directly
                            )
                            result = game.run()  # Play the game

                            # Handle the result
                            if result == "quit":  # Handle close window
                                pygame.quit()
                                sys.exit()
                            elif isinstance(result, int):  # If the result is a valid score
                                # Update player's score
                                player_data["score"] = max(int(player_data.get("score", 0)), result)

                                # Mark the level as completed if it isn't already
                                if selected_level["level"] not in player_data.get("completed_levels", []):
                                    player_data.setdefault("completed_levels", []).append(selected_level["level"])

                                # Save updated player data
                                login_system.save_logged_in_player_data(player_data)
                                break  # Exit the level loop after finishing the level
                            elif result == "restart":  # Restart the current level
                                continue  # Re-run the level
                            elif result == "main menu":  # Return to the main menu
                                break  # Exit the level loop

                elif menu_action == "leaderboard":
                    # Display Leaderboard
                    leaderboard = Leaderboard(screen, login_system)
                    leaderboard.run()

                elif menu_action == "quit":
                    pygame.quit()
                    sys.exit()  # Ensure the program exits cleanly

        elif action == "quit":
            pygame.quit()
            sys.exit()  # Exit when quitting from the login screen


if __name__ == "__main__":
    main()