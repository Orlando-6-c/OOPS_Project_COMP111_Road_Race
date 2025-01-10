import pickle

class LoginSystem:
    def __init__(self):
        self.data_file = "user_data.pkl"
        self.logged_in_user = None
        self.load_data()

    def load_data(self):
        """Load user data from the data file."""
        try:
            with open(self.data_file, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def save_data(self):
        """Save user data to the data file."""
        with open(self.data_file, "wb") as file:
            pickle.dump(self.data, file)

    def register(self, username, password):
        """Register a new user."""
        if username in self.data:
            return False, "Username already exists!"
        self.data[username] = {"password": password, "score": 0, "leaderboard": []}
        self.save_data()
        return True, "Account created successfully!"

    def login(self, username, password):
        """Log in an existing user."""
        if username in self.data and self.data[username]["password"] == password:
            self.logged_in_user = username
            return True, "Login successful!"
        return False, "Invalid username or password!"

    def get_logged_in_player_data(self):
        """Get data of the currently logged-in user."""
        if self.logged_in_user:
            return self.data[self.logged_in_user]
        return None

    def save_logged_in_player_data(self, player_data):
        """Save the logged-in user's data."""
        if self.logged_in_user:
            self.data[self.logged_in_user] = player_data
            self.save_data()

    def get_leaderboard(self):
        """Retrieve the global leaderboard."""
        leaderboard = []
        for username, user_data in self.data.items():
            leaderboard.append({"player": username, "score": user_data["score"]})
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        return leaderboard
