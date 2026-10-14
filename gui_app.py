import tkinter as tk
from tkinter import messagebox
from engine import GameEngine


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Guessing Game")
        self.root.geometry("550x650")

        self.game = GameEngine()

        # Game title
        tk.Label(
            root,
            text="WORD GUESSING GAME",
            font=("Arial", 24, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Difficulty
        tk.Label(
            root,
            text="Choose Difficulty:",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=20, pady=10)

        self.difficulty = tk.StringVar(value="easy")

        tk.OptionMenu(
            root,
            self.difficulty,
            "easy",
            "medium",
            "hard"
        ).grid(row=1, column=1, padx=20, pady=10)

        # Start button
        tk.Button(
            root,
            text="Start Game",
            command=self.start_game
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Hint
        self.hint_label = tk.Label(
            root,
            text="Hint: Press Start Game",
            font=("Arial", 14)
        )
        self.hint_label.grid(
            row=3, column=0, columnspan=2, pady=15
        )

        # Hidden word
        self.word_label = tk.Label(
            root,
            text="_ _ _ _ _",
            font=("Arial", 26, "bold")
        )
        self.word_label.grid(
            row=4, column=0, columnspan=2, pady=15
        )

        # Lives and score
        self.info_label = tk.Label(
            root,
            text="Lives: 6 | Score: 0",
            font=("Arial", 14)
        )
        self.info_label.grid(
            row=5, column=0, columnspan=2, pady=10
        )

        # Letter entry
        tk.Label(
            root,
            text="Enter one letter:",
            font=("Arial", 14)
        ).grid(row=6, column=0, padx=20, pady=10)

        self.entry = tk.Entry(
            root,
            font=("Arial", 18),
            width=8,
            justify="center"
        )
        self.entry.grid(
            row=6, column=1, padx=20, pady=10
        )

        # A-Z letter buttons
        self.letter_frame = tk.Frame(root)
        self.letter_frame.grid(
            row=7, column=0, columnspan=2, pady=10
        )

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            button = tk.Button(
                self.letter_frame,
                text=letter,
                width=3,
                command=lambda l=letter: self.guess_from_button(l)
            )
            button.grid(
                row=i // 9,
                column=i % 9,
                padx=2,
                pady=2
            )

        # Guess button
        tk.Button(
            root,
            text="Guess Letter",
            command=self.make_guess
        ).grid(
            row=8,
            column=0,
            columnspan=2,
            pady=10
        )

        # Message
        self.message_label = tk.Label(
            root,
            text="",
            font=("Arial", 14)
        )
        self.message_label.grid(
            row=9,
            column=0,
            columnspan=2,
            pady=10
        )

    def start_game(self):
        if self.game.load_word(self.difficulty.get()):
            self.hint_label.config(
                text="Hint: " + self.game.hint
            )

            self.word_label.config(
                text=self.game.get_hidden_word()
            )

            self.update_info()
            self.message_label.config(
                text="Game started!"
            )

        else:
            messagebox.showerror(
                "Error",
                "Could not load word file."
            )

    def update_info(self):
        self.info_label.config(
            text=f"Lives: {self.game.lives} | "
                 f"Score: {self.game.score}"
        )

    def guess_from_button(self, letter):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, letter)
        self.make_guess()

    def make_guess(self):
        if not self.game.secret_word:
            self.message_label.config(
                text="Please start the game first."
            )
            return

        guess = self.entry.get()
        self.entry.delete(0, tk.END)

        result = self.game.guess_letter(guess)

        if result == "invalid":
            self.message_label.config(
                text="Please enter one letter only."
            )
            return

        if result == "repeated":
            self.message_label.config(
                text="You already guessed that letter."
            )
            return

        if result == "correct":
            self.message_label.config(
                text="Correct!"
            )
        else:
            self.message_label.config(
                text="Wrong guess!"
            )

        self.word_label.config(
            text=self.game.get_hidden_word()
        )

        self.update_info()

        if self.game.is_won():
            self.game.save_history("WIN")

            messagebox.showinfo(
                "You Win!",
                f"Congratulations!\n"
                f"Word: {self.game.secret_word}\n"
                f"Score: {self.game.score}"
            )

        elif self.game.is_lost():
            self.game.save_history("LOSS")

            messagebox.showinfo(
                "Game Over",
                f"The word was: {self.game.secret_word}"
            )


root = tk.Tk()
app = GameGUI(root)
root.mainloop()