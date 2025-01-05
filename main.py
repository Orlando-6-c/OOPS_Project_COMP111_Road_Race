import pygame
from main_menu import MainMenu
from start_game import StartGame
from level_selection import LevelSelection
from game import Game
from leaderboard import Leaderboard
from pause_menu import PauseMenu

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create the screen
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Road Race")

    # Create MainMenu
    menu = MainMenu(screen)

    running = True

    while running:
        choice = menu.run()

        if choice == "start_game":
            # Handle New User or Existing User
            start_game = StartGame(screen)
            user = start_game.run()
            if user and user != "back":
                level_selection = LevelSelection(screen, user)

                # Initialize user's score to 0 for a new session
                user_score = 0

                while True:
                    level = level_selection.run(user_score)  # Pass the current score to unlock levels
                    if level and level != "back":
                        game = Game(screen, user, level)
                        while True:
                            game_result = game.run()
                            if game_result == "pause":
                                # Pause Menu
                                pause_menu = PauseMenu(screen)
                                pause_choice = pause_menu.run()
                                if pause_choice == "main_menu":
                                    break
                                elif pause_choice == "restart":
                                    game = Game(screen, user, level)
                            elif game_result == "game_over":
                                # Update leaderboard and score
                                leaderboard = Leaderboard(screen)
                                leaderboard.update_leaderboard(user, game.score)
                                user_score = max(user_score, game.score)  # Update user's score if it's higher
                                break
                            else:
                                break
                    else:
                        break

        elif choice == "leaderboard":
            # Show Leaderboard
            leaderboard = Leaderboard(screen)
            if leaderboard.run() == "back":
                continue

        elif choice == "quit":
            running = False

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
