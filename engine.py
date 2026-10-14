import random
from datetime import datetime


class GameEngine:
    def __init__(self):
        self.secret_word = ""
        self.hint = ""
        self.guessed_letters = []
        self.lives = 6
        self.score = 0
        self.difficulty = ""

    def load_word(self, difficulty):
        self.difficulty = difficulty.lower()
        filename = self.difficulty + ".txt"

        try:
            with open(filename, "r") as file:
                lines = file.readlines()

            words = []

            for line in lines:
                line = line.strip()

                if "|" in line:
                    word, hint = line.split("|", 1)
                    words.append((word.upper(), hint))

            if not words:
                raise ValueError("No valid words found.")

            self.secret_word, self.hint = random.choice(words)
            self.guessed_letters = []
            self.lives = 6
            self.score = 0

            return True

        except (FileNotFoundError, ValueError):
            return False

    def guess_letter(self, letter):
        letter = letter.upper()

        if len(letter) != 1 or not letter.isalpha():
            return "invalid"

        if letter in self.guessed_letters:
            return "repeated"

        self.guessed_letters.append(letter)

        if letter in self.secret_word:
            self.score += 10
            return "correct"

        self.lives -= 1
        return "wrong"

    def get_hidden_word(self):
        result = ""

        for letter in self.secret_word:
            if letter in self.guessed_letters:
                result += letter + " "
            else:
                result += "_ "

        return result.strip()

    def is_won(self):
        for letter in self.secret_word:
            if letter not in self.guessed_letters:
                return False

        return True

    def is_lost(self):
        return self.lives <= 0

    def save_history(self, result):
        with open("game_history.txt", "a") as file:
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            file.write(
                f"{date} | {self.difficulty} | "
                f"{self.secret_word} | {result} | Score: {self.score}\n"
            )