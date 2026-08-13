'''
Method 3 — I can regenerate it as a downloadable PNG file
The better option is for me to create the icon again as a proper PNG file attachment rather than just an image displayed in the chat. Then you can save it directly into your Wordle folder.
I can do that next.
# Sean J Fennell
# 12 Aug 2026 @ 2142
'''
import tkinter as tk
from tkinter import font
import random
import os
import json


    
class WordleGame:
    def __init__(self, master):
        self.master = master

        self.master.title("Wordle Game")
        self.master.configure(bg="oldlace")
        self.master.geometry("1070x950")
       
        self.create_menu()

        self._cells = {}
        self.grid = {}
        
        self.current_row = 0
        self.current_col = 0
        self.game_over = False
        self.current_game_won = False
        
        
        self.current_guesses = 0
        
        self.share_results = []

        self.stats_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "wordle_stats.json"
        )
 
        self.games_played = 0
        self.games_won = 0
        self.current_streak = 0
        self.best_streak = 0
        self.gave_up = 0


        

        self.guess_distribution = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0
        }
        
        self.load_statistics()
        
        self.answer_list = self.load_words("wordle_answers.txt")
        self.guess_list = self.load_words("wordle_guesses.txt")
        #  print("Answers loaded:", len(self.answer_list))
        #  print("Guesses loaded:", len(self.guess_list))

        self.secret_word = random.choice(self.answer_list)
            
        self.main_frame = tk.Frame(self.master,bg="oldlace",)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.main_frame.columnconfigure(0, weight=1, )  # Statistics
        self.main_frame.columnconfigure(1, weight=0)  # Game
        self.main_frame.columnconfigure(2, weight=1)  # Distribution

        self.game_frame = tk.Frame(self.main_frame,bg="oldlace" )
        self.game_frame.grid(row=0, column=1, sticky="n")

        self.title_label = tk.Label(
            self.game_frame,
            text="WORDLE",
            font=("Helvetica", 18, "bold"),
            bg="oldlace",
            fg="black"
        )
        self.title_label.pack(pady=(0, 5))

        self.message_label = tk.Label(
            self.game_frame,
            text=" ",
            font=("Helvetica", 16, "bold"),
            bg="oldlace",
            fg="black",
            width=35,
            wraplength=550,
            justify="center"
        )
        self.message_label.pack(pady=(0,5))
             
        self.stats_column = tk.Frame(self.main_frame, bg="oldlace")
        self.stats_column.grid(row=0, column=0, sticky="n")

        self.distribution_column = tk.Frame(self.main_frame, bg="oldlace")
        self.distribution_column.grid(row=0, column=2, sticky="n")

        self.stats_heading = tk.Label(
            self.stats_column,
            text="STATISTICS",
            font=("Menlo", 16, "bold"),
            bg="oldlace",
            fg="black",
            justify="left"
        )

        self.stats_heading.grid(
            row=0,
            column=0,
            padx=20,
            sticky="w"
        )

        self.stats_label = tk.Label(
            self.stats_column,
            text="",
            font=("Menlo", 16),
            bg="oldlace",
            fg="black",
            justify="left",
            anchor="nw",
        )

        self.stats_label.grid(
            row=1,
            column=0,
            padx=20,
            sticky="w"
        )


        self.distribution_heading = tk.Label(
            self.distribution_column,
            text="DISTRIBUTION",
            font=("Menlo", 16, "bold"),
            bg="oldlace",
            fg="black",
            justify="left"
        )
        self.distribution_heading.grid(
            row=0, column=0, padx=20, sticky="w")


      
     
        self.distribution_label = tk.Label(
            self.distribution_column,
            text="",
            font=("Menlo", 16,),
            bg="oldlace",
            fg="black",
            justify="left", anchor="nw",
        )
        self.distribution_label.grid(
            row=1,  column=0, padx=(20), sticky="w")
        
        self.update_distribution_display()

        self.update_statistics_display()
        self._create_board_grid()
        self._create_keyboard()
        
        self.master.bind("<Key>", self.physical_key)


    def create_menu(self):
        menubar = tk.Menu(self.master)

        help_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        help_menu.add_command(
            label="How to Play",
            command=self.show_help
        )

        help_menu.add_command(
            label="About Wordle Game",
            command=self.show_about
        )

        help_menu.add_command(
            label="Helpful Tactics",
            command=self.show_tactics
        )
        menubar.add_cascade(
            label="Help",
            menu=help_menu
        )

        self.master.config(menu=menubar)


    def show_help(self):
        help_window = tk.Toplevel(self.master)

        help_window.title("How to Play")
        help_window.geometry("450x350")
        help_window.configure(bg="oldlace")

        text = (
            "WORDLE RULES\n\n"
            "Guess the hidden five-letter word in six attempts.\n\n"
            "Green = correct letter in the correct position.\n"
            "Yellow = correct letter in the wrong position.\n"
            "Grey = letter not in the word.\n\n\n"
            
            "Type letters using the keyboard or click the on-screen keys.\n\n"
            "Press ENTER to check your guess.\n"
            "Use BACKSPACE to delete a letter.\n"
            "Press the NEW GAME button to start a new game.\n"
            "Press the GIVE UP button to give up.\n"
        )

        label = tk.Label(
            help_window,
            text=text,
            font=("Helvetica", 14),
            bg="oldlace",
            justify="left",
            padx=20,
            pady=20
        )

        label.pack()


    def show_about(self):
        about_window = tk.Toplevel(self.master)

        about_window.title("About Wordle Game")
        about_window.geometry("400x250")
        about_window.configure(bg="oldlace")

        text = (
            "WORDLE GAME\n\n"
            "A five-letter word puzzle game.\n\n"
            "Created using Python and tkinter.\n\n"
            "Features:\n"
            "- Statistics tracking\n"
            "- Guess distribution\n"
            "- Share result function\n"
            "- Separate word lists\n"
        )

        label = tk.Label(
            about_window,
            text=text,
            font=("Helvetica", 14),
            bg="oldlace",
            justify="left",
            padx=20,
            pady=20,)
        label.pack()

    def show_tactics(self):
        tactics_window = tk.Toplevel(self.master)

        tactics_window.title("Helpful Tactics")
        tactics_window.geometry("500x300")
        tactics_window.configure(bg="oldlace")

        text = (
            "HELPFUL TACTICS\n\n"
            
            "First find a file named 'wordle_answers.txt' and study it.\n"
            "It contains all the possible answers, and studying the list\n"
            "might help you when you are stuck.\n\n"
            
            "For your first choice of a word ADIEU and AUDIO can help you\n"
            "narrow down your choice of vowels because each contain four vowels.\n\n"

            "Similarly, the words STARE, RAISE, SLATE and CRANE balance\n"
            "commonly occurring patterns of consonants with vowels which can\n"
            "be helpful.\n\n"

            "Also, note that the letters 'E', 'T', 'A', 'O', 'I', and 'N' are very\n"
            "common in 5-letter words.\n\n"
        )

        label = tk.Label(
            tactics_window,
            text=text,
            font=("Helvetica", 14),
            bg="oldlace",
            justify="left",
            anchor="nw",
            wraplength=450,
            padx=20,
            pady=20
        )
        label.pack(fill="both", expand=True)







    def load_words(self, filename):
        folder = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(folder, filename)

        with open(filepath, "r", encoding="utf-8-sig") as file:
            words = {
                line.strip().upper()
                for line in file
                if len(line.strip()) == 5
            }

        return sorted(words)
    

    def _create_board_grid(self):

        grid_frame = tk.Frame(self.game_frame, bg="oldlace")
        grid_frame.pack(pady=(2,10))

        for row in range(6):
            grid_frame.rowconfigure(row, weight=1, minsize=20)

            for col in range(5):
                grid_frame.columnconfigure(col, weight=1, minsize=75)

                label = tk.Label(
                    master=grid_frame, borderwidth=1, relief='solid',
                    text="",
                    font=font.Font(size=30, weight="bold"),
                    fg="black", bg="oldlace",
                    width=3, height=2,
                )

                self._cells[label] = (row, col)
                self.grid[(row, col)] = label
                
                label.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5
                )

                
    def _create_keyboard(self):
        self.letter_buttons = {}

        button_bg = "azure2"
        button_fg = "black"
        button_font = ("Menlo", 14, "bold")

        self.buttons_frame = tk.Frame(self.game_frame, bg="oldlace")
        self.buttons_frame.pack()

        upper_frame = tk.Frame(self.buttons_frame, bg="oldlace")
        upper_frame.pack()

        middle_frame = tk.Frame(self.buttons_frame, bg="oldlace")
        middle_frame.pack()

        lower_frame = tk.Frame(self.buttons_frame, bg="oldlace")
        lower_frame.pack()

        upper_row = "QWERTYUIOP"
        middle_row = "ASDFGHJKL"
        lower_row = "ZXCVBNM"
        for letter in upper_row:
            button = tk.Label(
                upper_frame,
                text=letter,
                width=6,
                height=2,
                font=button_font,
                bg=button_bg,
                fg=button_fg,
                relief="raised",
                borderwidth=2
            )

            button.bind(
                "<ButtonPress-1>",
                    lambda event, l=letter: (
                     self.guess_letter(l),
                     event.widget.config(relief="sunken")
                     )
            )

            button.bind(
                "<ButtonRelease-1>",
                lambda event: event.widget.config(relief="raised")
            )
            
            button.pack(side="left", padx=2, pady=3)
            self.letter_buttons[letter] = button

        for letter in middle_row:
            button = tk.Label(
                    middle_frame,
                text=letter,
                width=5,
                height=2,
                font=button_font,
                bg=button_bg,
                fg=button_fg,
                relief= "raised",
                borderwidth=2
            )

            button.bind(
                "<ButtonPress-1>",
                    lambda event, l=letter: (
                    self.guess_letter(l),
                    event.widget.config(relief="sunken")
                )
            )

            button.bind(
                "<ButtonRelease-1>",
                    lambda event: event.widget.config(relief="raised")
            )

            button.pack(side="left", padx=2, pady=3)
            self.letter_buttons[letter] = button

        for letter in lower_row:
            button = tk.Label(
                lower_frame,
                text=letter,
                width=5,
                height=2,
                font=button_font,
                bg=button_bg,
                fg=button_fg,
                relief="raised",
                borderwidth=2
            )

            button.bind(
                "<ButtonPress-1>",
                    lambda event, l=letter: (
                    self.guess_letter(l),
                    event.widget.config(relief="sunken")
                )
            )

            button.bind(
                "<ButtonRelease-1>",
                lambda event: event.widget.config(relief="raised")
            )
            button.pack(side="left", padx=2, pady=3)
            self.letter_buttons[letter] = button

        self.enter_button = tk.Button(
            lower_frame, text="ENTER",  width=7, height=2, font=button_font,
            bg=button_bg, fg=button_fg,relief="raised", borderwidth=2,
            command=self.enter_guess,
        )
        self.enter_button.pack(side="left", padx=2, pady=3)      

        self.delete_button = tk.Button(
            lower_frame,  text="⌫", width=5, height=2,
            font=button_font, bg=button_bg, fg=button_fg,relief="raised",
              borderwidth=2,
            command=self.delete_letter,
        )
        self.delete_button.pack(side="left", padx=2, pady=3)


        self.buttons_bottom_frame = tk.Frame(
            self.buttons_frame,
            bg="oldlace"
        )
        self.buttons_bottom_frame.pack(pady=5)

        self.new_game_button = tk.Button(
            self.buttons_bottom_frame,
            text="NEW GAME",
            width=12,
            height=2,
            font=button_font,
            bg=button_bg,
            fg=button_fg,
            command=self.new_game,
        )
        self.new_game_button.pack(side="left", padx=5)

        self.copy_button = tk.Button(
            self.buttons_bottom_frame,
            text="COPY RESULT",
            width=12,
            height=2,
            font=button_font,
            bg=button_bg,
            fg=button_fg,
            command=self.copy_result,
        )
        self.copy_button.pack(side="left", padx=5)
        self.copy_button.config(state="disabled")

        self.give_up_button = tk.Button(
                    self.buttons_bottom_frame,
                    text="GIVE UP",
                    width=12,
                    height=2,
                    font=button_font,
                    bg=button_bg,
                    fg=button_fg,
                    command=self.give_up,
                )
        self.give_up_button.pack(side="left", padx=5)

     
    def delete_letter(self):
        #  if game over don't allow any further input
        if self.game_over:
            return
    
        if self.current_col > 0:
            self.current_col -= 1
    
        for label, position in self._cells.items():
            if position == (self.current_row, self.current_col):
                label.config(text="")
                break


    def enter_guess(self):
        #  if game over don't allow any further input
        if self.game_over:
            return
        if self.current_col == 5:
            guess = ""
            for label, position in self._cells.items():
                if position[0] == self.current_row:
                    guess += label.cget("text")
            
            if guess not in self.guess_list:
                self.message_label.config(text="Not a valid word")
                return
            
            self.check_guess(guess)
            self.current_guesses += 1
            
            if guess == self.secret_word:
                # print("You got it")
                guesses = self.current_row + 1
                self.guess_distribution[guesses] += 1
                       
                self.update_distribution_display()
                
               # print(self.guess_distribution)
                if guesses == 1:
                    word = "guess"
                else:
                    word = "guesses"

                self.master.after(
                    1500,
                    lambda: self.show_end_message(True, guesses)
                )
        
                
                self.games_played += 1
                self.games_won += 1
                self.current_streak += 1
                if self.current_streak > self.best_streak:
                    self.best_streak = self.current_streak
    
                self.save_statistics()
                self.update_statistics_display()

                self.current_game_won = True
                self.copy_button.config(state="normal")
                self.master.after(
                    1000,
                    self.end_game_win
                )
                return


                
                #self.game_over = True
                #self.disable_keyboard()
                
                #return
                self.master.after(
                    1000,
                    self.end_game_win
                )
                return






            
         #   else:
            #   pass
               # print("Not correct")

            #  go to start of next row
            #  but stop if we are on the last row
            if self.current_row < 5:
                self.current_row += 1
                
                self.current_col = 0
            else:
                self.games_played += 1
                self.current_streak = 0
                self.save_statistics()
                print("Current streak:", self.current_streak)

                self.update_statistics_display()
                
                self.game_over = True
                print("Game over")
                print("The word was:", self.secret_word)
                
                self.show_end_message(False)

                self.disable_keyboard()

                self.copy_button.config(state="normal")
                return
            
        else:
            print("You need five letters")

    
    def update_keyboard_button(self, letter, colour):
        button = self.letter_buttons[letter]
        current_colour = button.cget("bg")

        if colour == "green":
            button.config(
                bg="green2",
                fg="white"
            )

        elif colour == "yellow":
            # Don't change a green button back to yellow
            if current_colour != "green2":
                button.config(
                    bg="yellow",
                    fg="black"
                )

        elif colour == "grey":
            # Don't change a green or yellow button to grey
            if current_colour not in ("green2", "yellow"):
                button.config(
                    bg="grey",
                    fg="white"
                )

                # Prevent the letter from being clicked again
                button.unbind("<Button-1>")


    def flip_tile(self, label, final_bg, final_fg, letter, step=0):

        heights = [2, 1, 0, 1, 2]

        if step < len(heights):

            if step == 2:
                # halfway point - change the face of the tile
                label.config(
                    text="",
                    bg=final_bg,
                    fg=final_fg
                )

            label.config(height=heights[step])

            self.master.after(
                70,
                lambda: self.flip_tile(
                    label,
                    final_bg,
                    final_fg,
                    letter,
                    step + 1
                )
            )


        else:
            label.config(
                text=letter,
                height=2
            )

          















    def check_guess(self, guess):
                
        remaining = list(self.secret_word)
        row_result = []
        tile_results = [None, None, None, None, None]
        
        # First pass: correct letter in correct position
        for col in range(5):
            label = self.grid[(self.current_row, col)]

            if guess[col] == self.secret_word[col]:
                tile_results[col] = ("green")
                self.update_keyboard_button(guess[col], "green")
                row_result.append("🟩")
                remaining[col] = None
                

                

        # Second pass: correct letter in wrong position,
        # or letter not in the word
        for col in range(5):
            label = self.grid[(self.current_row, col)]

            if guess[col] == self.secret_word[col]:
                continue

            if guess[col] in remaining:
                # Letter is in the word, but in the wrong position
                tile_results[col]=("yellow")
                self.update_keyboard_button(guess[col], "yellow")


                #  label.config(bg="yellow", fg="black")
                
                
                
                row_result.append("🟨")
                remaining[remaining.index(guess[col])] = None

            else:
                # Letter is not in the word
                tile_results[col]=("grey")


                # label.config(bg="grey", fg="white")

                self.update_keyboard_button(guess[col], "grey")

                row_result.append("⬜")
        
        for col in range(5):
            label = self.grid[(self.current_row, col)]

            if tile_results[col] == "green":
                self.master.after(
                    col * 250,
                    lambda l=label, c=col: self.flip_tile(
                        l, "green2", "white", guess[c]
                    )
                )

            elif tile_results[col] == "yellow":
                self.master.after(
                    col * 200,
                    lambda l=label, c=col: self.flip_tile(
                        l, "yellow", "black", guess[c]
                    )
                )

            else:
                self.master.after(
                    col * 200,
                    lambda l=label, c=col: self.flip_tile(
                        l, "grey", "white", guess[c]
                    )
                )
        self.share_results.append("".join(row_result))


    def physical_key(self, event):
        if self.game_over:
            return
        
        letter = event.char.upper()

        if letter in self.letter_buttons:
            self.guess_letter(letter)
        elif event.keysym == "BackSpace":
            self.delete_letter()
        elif event.keysym == "Return":
            self.enter_guess()


    def guess_letter(self, letter):
        #  if correct 
        if self.game_over:
            return
        
        self.message_label.config(text="")
        
        for label, position in self._cells.items():
            if position == (self.current_row, self.current_col):
                label.config(text=letter)
                break

        if self.current_col < 5:
            self.current_col += 1


    def update_statistics_display(self):
        if self.games_played > 0:
            win_percent = (self.games_won / self.games_played) * 100
        else:
            win_percent = 0

        percentage_text = f"{win_percent:.0f}%"

        if self.games_won > 0:
            total_guesses = 0

            for guesses, count in self.guess_distribution.items():
                total_guesses += guesses * count

            average_guesses = total_guesses / self.games_won
            average_text = f"{average_guesses:.1f}"
        else:
            average_text = "--"

        games_lost = self.games_played - self.games_won

        self.stats_label.config(
            text=f"Games played:    {self.games_played:>5}\n"
                 f"Games won:       {self.games_won:>5}\n"
                 f"Games lost:      {games_lost:>5}\n\n"

                 f"Win percentage:  {percentage_text:>5}\n"
                 f"Average guesses: {average_text:>5}\n\n"

                 f"Current streak:  {self.current_streak:>5}\n"
                 f"Best streak:     {self.best_streak:>5}\n\n"

                 f"Gave up:         {self.gave_up:>5}\n"
        )

    def update_distribution_display(self):

        distribution_text = ""

        for number in range(1, 7):
            word = "guess" if number == 1 else "guesses"

            distribution_text += (
                f"{number} {word:<8} {self.guess_distribution[number]:>3}\n\n"
            )

        self.distribution_label.config(text=distribution_text)


        

    def show_end_message(self, won, guesses=None):
        if won:
            if guesses == 1:
                word = "guess"
            else:
                word = "guesses"

            message = (
                f"🎉 Well done!  " +  f"You got it in {guesses} {word}."
            )

        else:
            message = (f"Game over!  The word was {self.secret_word}.")

        self.message_label.config(text=message)


    def copy_result(self):
        result = self.generate_share_result()

        self.master.clipboard_clear()
        self.master.clipboard_append(result)

        self.message_label.config(
            text="Result copied!"
        )


    def give_up(self):
        self.games_played += 1
        self.gave_up += 1
        self.current_streak = 0

        self.save_statistics()
        self.update_statistics_display()

        message = f"Oh Dear!  The word was {self.secret_word}."

        self.message_label.config(text=message)

        self.game_over = True
        self.disable_keyboard()

        self.copy_button.config(state="normal")








    def generate_share_result(self):
        if self.current_game_won:
            guesses = self.current_guesses

            result = (
                f"WORDLE\n\n"
                f"Solved in {guesses} guesses\n\n"
            )

            for row in self.share_results:
                result += row + "\n"

        else:
            result = (
                f"WORDLE\n\n"
                f"Game over\n\n"
            )

            for row in self.share_results:
                result += row + "\n"

        return result


    def load_statistics(self):
        try:
            with open(self.stats_file, "r") as file:
                statistics = json.load(file)

            self.games_played = statistics.get("games_played", 0)
            self.games_won = statistics.get("games_won", 0)
            self.current_streak = statistics.get("current_streak", 0)
            self.best_streak = statistics.get("best_streak", 0)
            self.gave_up = statistics.get("gave_up", 0)
            self.guess_distribution = {
                int(k): v for k, v in statistics.get(
                    "guess_distribution",
                    {
                        "1": 0,
                        "2": 0,
                        "3": 0,
                        "4": 0,
                        "5": 0,
                        "6": 0
                    }
                ).items()
            }
          
        except (FileNotFoundError, json.JSONDecodeError):
            self.games_played = 0
            self.games_won = 0
            self.current_streak = 0
            self.best_streak = 0
            self.guess_distribution = {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0
            }


    def save_statistics(self):
        statistics = {
        "games_played": self.games_played,
        "games_won": self.games_won,
        "current_streak": self.current_streak,
        "best_streak": self.best_streak,
        "gave_up": self.gave_up,
        "guess_distribution": self.guess_distribution
        }

        with open(self.stats_file, "w") as file:
            json.dump(statistics, file)

    def end_game_win(self):
        self.game_over = True
        self.disable_keyboard()



    def new_game(self):
        old_word= self.secret_word
        self.secret_word = random.choice(self.answer_list)

        while self.secret_word == old_word:
            self.secret_word = random.choice(self.answer_list)

       # print("Secret word:", self.secret_word)
        
        self.current_row = 0
        self.current_col = 0
        self.game_over = False
        self.current_game_won = False
        self.current_guesses = 0
        self.share_results = []
        
        self.message_label.config(text="")

        for label in self._cells:
            label.config(text="", bg="oldlace", fg="black")
        
        for letter, button in self.letter_buttons.items():
            button.config(
                bg="azure2",
                fg="black"
            )

            button.bind(
                "<ButtonPress-1>",
                lambda event, l=letter: (
                    self.guess_letter(l),
                    event.widget.config(relief="sunken")
                )
            )

            button.bind(
                "<ButtonRelease-1>",
                lambda event: event.widget.config(relief="raised")
            )

        self.enter_button.config(state="normal")
        self.delete_button.config(state="normal")


    def disable_keyboard(self):
        for button in self.letter_buttons.values():
            button.unbind("<ButtonPress-1>")
            button.unbind("<ButtonRelease-1>")

        self.enter_button.config(state="disabled")
        self.delete_button.config(state="disabled")


def main():
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

'''

The next logical stages, when you come back, would probably be:
Design the icon
Something simple like:
five Wordle squares,
a highlighted letter,
maybe "W" or "WORDLE" styling,
suitable for a macOS .icns file.

Final polish
check window size on smaller screens/iPads
adjust spacing/padding
maybe add a small version number in About

Packaging
create the .app
add the icon
test opening from Finder
possibly create a .dmg

I would avoid adding major new features now. The game already has the feel of a finished application rather than just a programming exercise.
When you return, we can pick up with the icon design. I think a custom icon would be a nice finishing touch.
























Auto
















Sources






















 if self.games_won > 0:
            total_guesses = 0

            for guesses, count in self.guess_distribution.items():
                total_guesses += guesses * count

            average_guesses = total_guesses / self.games_won
            average_text = f"{average_guesses:.1f}"
        else:
            average_text = "   --"

        games_lost = self.games_played - self.games_won

        self.stats_label.config(
            text=f"STATISTICS\n\n"
                 f"Games played:    {self.games_played:>5}\n"
                 f"Games won:       {self.games_won:>5}\n"
                 f"Games lost:      {games_lost:>5}\n\n"

                 f"Win percentage:  {win_percent:>4.0f}%\n"
                 f"Average guesses: {average_text:>5}\n\n"

                 f"Current streak:  {self.current_streak:>5}\n"
                 f"Best streak:     {self.best_streak:>5}\n\n"

                 f"Gave up:         {self.gave_up:>5}\n"
        )



3. Make one final observation
Play a few games and check:
A normal win on guesses 2–6
A first-guess win
A loss after six rows
COPY RESULT
Statistics
New Game
The reason I suggest this is that animation introduces timing, and timing can sometimes expose small issues in buttons or game-over handling.
After that, I think the next worthwhile improvement would be the application icon and Mac .app packaging, because the program itself is now very close to finished.
You have come a long way from the first version where the board, keyboard, statistics, and word checking were still being built. This is now a proper little game. 👍










Using Label is actually a good choice for Wordle because the squares are display areas rather than controls. You can now concentrate on the game itself.
A sensible order for building it would be:
6 × 5 grid — done.
Keyboard underneath the grid.
Allow the player to type a five-letter word.
Put each letter into the current row.
Press Enter to submit the guess.
Check the guess against the hidden five-letter word.
Change each square's background:green = correct letter and position
yellow = correct letter, wrong position
grey = letter not in the word

Move to the next row.
Detect win or six unsuccessful guesses.
I would tackle these one at a time, rather than trying to write the whole Wordle game at once.
The next logical step is probably getting keyboard input into the five squares of the first row.

This is a good milestone because now your program is actually evaluating the guess visually.
After this works, the next step will be:
make ENTER move to the next row;
then add the yellow "correct letter, wrong place" logic;
finally add a random word list.
You're progressing through exactly the same stages that a professional developer would use: get the mechanics working first, then add complexity.


That sounds like a very good place to stop. 👍
You have actually achieved a lot in one evening:
✅ Built the Wordle board
✅ Built the on-screen keyboard
✅ Connected buttons to the game logic
✅ Entered letters into the correct squares
✅ Implemented backspace correctly
✅ Limited guesses to five letters
✅ Added the ENTER function
✅ Built a guess string from the row
✅ Compared the guess with the secret word
✅ Added the first stage of colour feedback  
The program has now moved from being a GUI layout exercise into a working game engine.
When you come back tomorrow, I suggest we continue in this order:
Move to the next row after ENTER
reset current_col
increase current_row
prevent going beyond row 5

Improve the colour checking
green: correct letter and position
yellow: correct letter but wrong position
grey: letter not present

Add a random secret word
replace "HELLO" with a word chosen from a list

Add game endings
"You won!"
"Game over — the word was..."

One thing I would mention before you close it tonight: save a copy of this working version. You have reached a good checkpoint, and it is always worth keeping a version that works before adding the next layer.
Enjoy the rest — you made very good progress today. I look forward to continuing with it tomorrow. 🙂

















'''
