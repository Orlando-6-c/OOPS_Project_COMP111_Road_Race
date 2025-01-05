import pickle
import os

class FileHandling:
    def __init__(self, data_file="game_data.pkl"):
        self.data_file = data_file
        if not os.path.exists(self.data_file):
            self._initialize_data_file()

    def _initialize_data_file(self):
        initial_data = {
            "leaderboard": {},
            "game_progress": {},
        }
        with open(self.data_file, "wb") as file:
            pickle.dump(initial_data, file)

    def _load_data(self):
        try:
            with open(self.data_file, "rb") as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            self._initialize_data_file()
            return self._load_data()

    def _save_data(self, data):
        with open(self.data_file, "wb") as file:
            pickle.dump(data, file)

    def get_leaderboard(self):
        data = self._load_data()
        return data["leaderboard"]

    def add_user(self, username):
        data = self._load_data()
        if username not in data["leaderboard"]:
            data["leaderboard"][username] = 0  # Default score is 0
            self._save_data(data)

    def update_leaderboard(self, username, score):
        """Update the leaderboard with the user's score."""
        data = self._load_data()
        if username in data["leaderboard"]:
            data["leaderboard"][username] = score
            self._save_data(data)
        else:
            raise ValueError(f"User {username} not found in leaderboard")

    def get_registered_users(self):
        return list(self.get_leaderboard().keys())
