#  _   _ _    _ __  __  _____ _    _ ______  _____ _____ ______ _____  
# | \ | | |  | |  \/  |/ ____| |  | |  ____|/ ____/ ____|  ____|  __ \ 
# |  \| | |  | | \  / | |  __| |  | | |__  | (___| (___ | |__  | |__) |
# | . ` | |  | | |\/| | | |_ | |  | |  __|  \___ \\___ \|  __| |  _  / 
# | |\  | |__| | |  | | |__| | |__| | |____ ____) |___) | |____| | \ \ 
# |_| \_|\____/|_|  |_|\_____|\____/|______|_____/_____/|______|_|  \_\
# 

"""Easy terminal-based number-guessing game NUMGUESSER. Local scoreboard included. Estonian version."""


__author__ = "Oscar Robin"
__copyright__ = "Copyright (c) 2022 Oscar Robin"
__license__ = "Open-Source, free to use"
__version__ = "1.0"


import csv
import datetime
import os
import time
from random import *


GAME_SESSION = True
SCOREBOARD_ENABLED = True
SCOREBOARD_LENGTH = 15
SCOREBOARD_CSV_FILE = "numguesser_scoreboard.csv" # make sure that the file has heading "name,score,hit,date" and is in .csv extension
PLAYER_NAME = ""


class colors:
    """Color constants to use in text printouts."""
    WHITE = '\033[7m' #WHITE
    GREEN = '\033[32m' #GREEN
    YELLOW = '\033[33m' #YELLOW
    ORANGE = '\033[91m' #ORANGE
    RED = '\033[92m' #RED
    BLACK = '\033[93m' #BLACK
    RESET = '\033[0m' #RESET COLOR
    NUMGUESSER = '\033[1m' #Slightly purple


class ScoreboardRow:
    """Holds information about a certain scoreboard row obtained from the scoreboard .csv file."""
    def __init__(self, name, score, hit, date):
        self.name = name
        self.score = int(score)
        self.hit = hit + "%"
        self.date = date


class Game:
    """Best game engine ever."""
    def __init__(self):
        self.levels = 7
        self.score = 0
        self.guess_count = 0
        self.guesses_left = 0
        self.total_guesses = 0
        self.levels_completed = 0
        self.max_possible_points = 0
        self.break_line = "-------"
        self.guess_text = "Paku arv: "
        self.fibonacci = [1, 2, 3, 5, 8, 13, 21, 34]

    def start_game(self):
        """Starts the game and finally calls the came ending."""
        for level in range(self.levels):
            real_level = level + 1
            self.start_level(real_level)
        self.end_game()
        input("\nVajuta enter, et uuesti mängida...")
        
    def end_game(self):
        """Literally ends the game."""
        self.hit = str(round((self.levels_completed/self.total_guesses) * 100, 2))
        if str(self.hit)[-2] == ".":
            self.hit += "0"
        self.clear_screen()
        self.display_end_message()
        if SCOREBOARD_ENABLED:
            self.add_score_to_scoreboard()
            self.display_scoreboard()

    def start_level(self, level):
        """Starts the level inside the game."""
        self.guess_count = 0
        self.guesses_left = 8 - level
        self.screen_history = ""
        self.clear_screen()
        self.display_header_message()
        self.display_level_message(level, False)
        self.start_guessing(level)

    def start_guessing(self, level):
        """Abracadabra."""
        level_over = False
        secret_number = randint(0, 100)
        while not level_over:
            if self.guesses_left < 1:
                level_over = True
                self.clear_screen()
                self.display_header_message()
                self.display_level_message(level, True)
                print(self.screen_history)
                print(f"Selle leveli sa {colors.RED + 'feilisid' + colors.RESET}! Õige arv oli {secret_number}!")
                input("\nVajuta enter, et jätkata...")
                break
            print(self.break_line)
            if self.guess_count == 0:
                self.screen_history += f"{self.break_line}"
            else:
                self.screen_history += f"\n{self.break_line}"
            guess_valid = False
            while not guess_valid:
                self.clear_screen()
                self.display_header_message()
                self.display_level_message(level, True)
                print(self.screen_history)
                guess = input(self.guess_text)
                only_numbers = True
                for char in guess:
                    if not char.isdigit():
                        only_numbers = False
                if len(guess) < 1:
                    guess_valid = False
                elif only_numbers:
                    if int(guess) < 101:
                        guess_valid = True
            guess = int(guess)
            self.screen_history += f"\n{self.guess_text}{guess}"
            self.guesses_left -= 1
            self.guess_count += 1
            self.total_guesses += 1
            if guess == secret_number:
                added_score = round((8 - self.guess_count) * self.fibonacci[level - 1] * 10)
                self.score += added_score
                self.levels_completed += 1
                self.clear_screen()
                self.display_header_message()
                self.display_level_message(level, True)
                print(self.screen_history)
                print(f"{colors.GREEN + 'Pihtas-põhjas!' + colors.RESET} Arvasid õige arvu {self.guess_count}. korraga ja said {colors.NUMGUESSER + str(added_score) + colors.RESET} punkti!")
                input("\nVajuta enter, et jätkata...")
                break
            else:
                self.clear_screen()
                self.display_header_message()
                self.display_level_message(level, False)
                print(self.screen_history)
                radius = abs(secret_number - guess)
                if radius > 40:
                    black_area_text = f"Oled {colors.BLACK + 'mustas' + colors.RESET} alas!"
                    print(black_area_text)
                    self.screen_history += f"\n{black_area_text}"
                elif radius > 20:
                    red_area_text = f"Oled {colors.RED + 'punases' + colors.RESET} alas!"
                    print(red_area_text)
                    self.screen_history += f"\n{red_area_text}"
                elif radius > 10:
                    orange_area_text = f"Oled {colors.ORANGE + 'oranžis' + colors.RESET} alas!"
                    print(orange_area_text)
                    self.screen_history += f"\n{orange_area_text}"
                elif radius > 3:
                    yellow_area_text = f"Oled {colors.YELLOW + 'kollases' + colors.RESET} alas!"
                    print(yellow_area_text)
                    self.screen_history += f"\n{yellow_area_text}"
                elif radius > 1:
                    green_area_text = f"Oled {colors.GREEN + 'rohelises' + colors.RESET} alas!"
                    print(green_area_text)
                    self.screen_history += f"\n{green_area_text}"
                else:
                    white_area_text = f"Oled {colors.WHITE + 'valges' + colors.RESET} alas!"
                    print(white_area_text)
                    self.screen_history += f"\n{white_area_text}"

    def display_header_message(self):
        """Displays the informative header message."""
        print(f"Tere tulemast arvu-arvamise mängu {colors.NUMGUESSER + 'NUMGUESSER' + colors.RESET}")
        print(f"Sinu eesmärk, {PLAYER_NAME}, on arvata ära arv vahemikus 0-100.")
        print("Iga arvamisega saad sa vihje, millises alas oled.")
        print(f"{colors.BLACK + 'Must' + colors.RESET} ala: oled õigest arvust rohkem, kui 40 arvu kaugusel")
        print(f"{colors.RED + 'Punane' + colors.RESET} ala: õige arv on 40 raadiuses")
        print(f"{colors.ORANGE + 'Oranž' + colors.RESET} ala: õige arv on 20 raadiuses")
        print(f"{colors.YELLOW + 'Kollane' + colors.RESET} ala: õige arv on 10 raadiuses")
        print(f"{colors.GREEN + 'Roheline' + colors.RESET} ala: õige arv on 3 raadiuses")
        print(f"{colors.WHITE + 'Valge' + colors.RESET} ala: õige arv on 1 raadiuses")

    def display_level_message(self, level, level_completed):
        """Displays the information about the current level."""
        self.update_max_possible_points(level)
        print(self.break_line)
        print(f"LEVEL {level}/{self.levels}")
        if level_completed:
            print(f"SKOOR {self.score}")
        else:
            print(f"SKOOR {self.score} (+{self.max_possible_points})")
        print(f"Pakkumisi alles: {self.guesses_left}")

    def display_end_message(self):
        """Displays the ending message with the game summary."""
        print("MÄNG ON LÄBI!")
        print(f"SINU SKOOR {self.score}")
        print(f"Läbisid kokku {self.levels_completed} levelit 7-st.")
        print(f"Kokku pakkusid {self.total_guesses} korda.")
        print(f"Sinu tabamuse protsent on {self.hit}%.")

    def display_scoreboard(self):
        """Displays the local scoreboard. Information is obtained from the sorted list that contains ScoreboardRow objects."""
        scoreboard_rows_sorted = self.generate_scoreboard_rows_sorted()
        max_rank_len = len(str(SCOREBOARD_LENGTH))
        max_name_len = 15
        max_score_len = 4
        max_tabamus_len = 7
        max_aeg_len = 10
        print("\nSKOORITABEL")
        title = f"{'KOHT':10}{'NIMI':25}{'SKOOR':10}{'TABAMUS':10}{'AEG':10}"
        print(title)
        print(f'{"-" * len(title)}')
        counter = 0
        match_found = False
        for row in scoreboard_rows_sorted:
            if counter > SCOREBOARD_LENGTH:
                break
            if PLAYER_NAME == row.name and self.score == row.score and self.hit == row.hit[:-1] and self.get_current_formatted_time() == row.date and not match_found:
                match_found = True
                print(f"{colors.NUMGUESSER}{str(counter):10}{row.name:25}{str(row.score):10}{row.hit:10}{row.date:10}{colors.RESET}")
            else:
                print(f"{str(counter):10}{row.name:25}{str(row.score):10}{row.hit:10}{row.date:10}")
            counter += 1

    def generate_scoreboard_rows_sorted(self):
        """Generates sorted list that contains ScoreboardRow objects."""
        scoreboard_rows = []
        with open(SCOREBOARD_CSV_FILE, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                new_scoreboard_row = ScoreboardRow(row[0], row[1], row[2], row[3])
                scoreboard_rows.append(new_scoreboard_row)
        hit_sorted = sorted(scoreboard_rows, key=lambda x: x.hit, reverse=True)
        return sorted(hit_sorted, key=lambda x: x.score, reverse=True)

    def update_max_possible_points(self, level):
        """Score has the (+X) suffix in the level message and in represents number of points obtained when answered correctly."""
        self.max_possible_points = round((8 - self.guess_count - 1) * self.fibonacci[level - 1] * 10)

    def add_score_to_scoreboard(self):
        """Creates new entry into .csv file based on the game summary."""
        with open(SCOREBOARD_CSV_FILE, "a") as scoreboard_file:
            scoreboard_file.write(f"{PLAYER_NAME},{self.score},{self.hit},{self.get_current_formatted_time()}\n")

    def get_current_formatted_time(self):
        """Obtains current time and formats it into DD-MM-YYYY format."""
        current_time = datetime.datetime.now()
        day = str(current_time.day)
        if len(day) == 1:
            day = "0" + day
        month = str(current_time.month)
        if len(month) == 1:
            month = "0" + month
        return f"{day}-{month}-{current_time.year}"

    def clear_screen(self):
        """Clears the terminal screen."""
        os.system("clear")


if __name__ == "__main__":
    if not os.path.exists(SCOREBOARD_CSV_FILE) and SCOREBOARD_ENABLED:
        with open(SCOREBOARD_CSV_FILE, 'w') as f:
            f.write("name,score,date\nmaximum,3710,100.00,01-01-1979\n")
    PLAYER_NAME = input("Mis on sinu nimi?: ")
    while GAME_SESSION:
        game_instance = Game()
        game_instance.start_game()
