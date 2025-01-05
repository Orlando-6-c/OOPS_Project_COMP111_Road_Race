import pygame
import json
from button import Button
from utils import get_font
bg=pygame.image.load("assets/leaderboard.png")
class Leaderboard:
    def __init__(self, screen):
        self.screen = screen
        self.font = get_font(20)
        self.leaderboard_file = "leaderboard.json"
        self.scores = self.load_leaderboard()

    def load_leaderboard(self):
        """Load leaderboard data from a JSON file."""
        try:
            with open(self.leaderboard_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_leaderboard(self):
        """Save leaderboard data to a JSON file."""
        with open(self.leaderboard_file, "w") as file:
            json.dump(self.scores, file)

    def update_leaderboard(self, player, score):
        """Update the leaderboard with the player's new score."""
        # Check if the player already exists on the leaderboard
        for entry in self.scores:
            if entry["player"] == player:
                # Update the score if the new score is higher
                if score > entry["score"]:
                    entry["score"] = score
                break
        else:
            # Add the player if they are not already in the leaderboard
            self.scores.append({"player": player, "score": score})

        # Sort the leaderboard in descending order of scores
        self.scores = sorted(self.scores, key=lambda x: x["score"], reverse=True)[:5]

        # Save the updated leaderboard
        self.save_leaderboard()

    def run(self):
        """Display the leaderboard screen."""
        while True:
            self.screen.blit(bg,(0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Back button
            back_button = Button(
                image=None, pos=(50, 50),
                text_input="Back", font=get_font(20), base_color="#d7fcd4", hovering_color="black")
            back_button.changeColor(mouse_pos)
            back_button.update(self.screen)

            # Draw leaderboard entries
            for idx, entry in enumerate(self.scores):
                score_text = self.font.render(
                    f"{idx + 1}. {entry['player']} - {entry['score']} pts", True, (255, 255, 255))
                text_rect = score_text.get_rect(center=(250, 150 + idx * 30))  # Centered horizontally
                self.screen.blit(score_text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_pos):
                        return "back"

            pygame.display.flip()
