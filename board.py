import curses
import random

class Board:
    def __init__(self, stdscr, size=7):
        self.stdscr = stdscr
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.words = [
            "PYTHON", "CODE", "DEBUG", "ALGORITHM", "FUNCTION",
            "VARIABLE", "LOOP", "CONDITION", "ARRAY", "STRING",
            "COMPUTER", "PROGRAM", "LANGUAGE", "DEVELOPER", "SOFTWARE",
            "HARDWARE", "NETWORK", "DATABASE", "SECURITY", "ENCRYPTION"
        ]
        self.selected_words = []
        self.common_letters = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        self.fill_board()

    def fill_board(self):
        # Filter out words longer than the board size
        valid_words = [word for word in self.words if len(word) <= self.size]

        # Randomly select 3 words to place on the board
        self.selected_words = random.sample(valid_words, 3)

        # Randomly place words on the board
        placed_letters = set()
        for word in self.selected_words:
            placed = False
            while not placed:
                direction = random.choice(['H', 'V'])  # H: Horizontal, V: Vertical
                if direction == 'H' and self.size - len(word) >= 0:
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - len(word))
                    if all(self.board[row][col + i] == ' ' for i in range(len(word))):
                        for i in range(len(word)):
                            self.board[row][col + i] = word[i]
                            placed_letters.add(word[i])
                        placed = True
                elif direction == 'V' and self.size - len(word) >= 0:
                    row = random.randint(0, self.size - len(word))
                    col = random.randint(0, self.size - 1)
                    if all(self.board[row + i][col] == ' ' for i in range(len(word))):
                        for i in range(len(word)):
                            self.board[row + i][col] = word[i]
                            placed_letters.add(word[i])
                        placed = True

        # Randomly fill some of the remaining empty cells with common letters
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ' and random.random() < 0.3:  # 30% chance to fill the cell
                    # Avoid using letters that are already placed in words
                    available_letters = [letter for letter in self.common_letters if letter not in placed_letters]
                    self.board[i][j] = random.choice(available_letters)  # Randomly choose a common letter

    def draw_board(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        board_width = self.size * 4 + 1
        board_height = self.size * 2 + 1
        start_x = (w - board_width) // 2
        start_y = (h - board_height) // 2

        # Draw hints on the left-hand side
        hint_start_y = start_y
        self.stdscr.addstr(hint_start_y, 2, "Words left:")
        for idx, word in enumerate(self.selected_words):
            hint = " ".join("_" * len(word))
            self.stdscr.addstr(hint_start_y + idx + 1, 2, hint)

        for i in range(self.size + 1):
            for j in range(self.size):
                x = start_x + j * 4
                y = start_y + i * 2
                if i < self.size:
                    self.stdscr.addstr(y, x, '+---')
                else:
                    self.stdscr.addstr(y, x, '+---')
                if j == self.size - 1:
                    self.stdscr.addstr(y, x + 4, '+')
                if i < self.size:
                    self.stdscr.addstr(y + 1, x, f'| {self.board[i][j]} ')
                if i < self.size and j == self.size - 1:
                    self.stdscr.addstr(y + 1, x + 4, '|')

        # Ensure the bottom line is drawn correctly
        for j in range(self.size):
            x = start_x + j * 4
            y = start_y + self.size * 2
            self.stdscr.addstr(y, x, '+---')
        self.stdscr.addstr(y, x + 4, '+')

        # Draw the menu button
        self.stdscr.addstr(h - 2, w - 12, "[ Menu ]", curses.A_REVERSE)

        self.stdscr.refresh()

    def show_exit_popup(self):
        h, w = self.stdscr.getmaxyx()
        popup_width = 40
        popup_height = 10
        start_x = (w - popup_width) // 2
        start_y = (h - popup_height) // 2

        # Draw the popup window
        popup_win = curses.newwin(popup_height, popup_width, start_y, start_x)
        popup_win.box()
        popup_win.addstr(2, 2, "Do you really want to exit this game?")
        popup_win.addstr(4, 2, "[ Yes ]")
        popup_win.addstr(4, 12, "[ No ]")
        popup_win.refresh()

        current_selection = 0
        while True:
            if current_selection == 0:
                popup_win.addstr(4, 2, "[ Yes ]", curses.A_REVERSE)
                popup_win.addstr(4, 12, "[ No ]")
            else:
                popup_win.addstr(4, 2, "[ Yes ]")
                popup_win.addstr(4, 12, "[ No ]", curses.A_REVERSE)
            popup_win.refresh()

            key = popup_win.getch()
            if key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
                current_selection = 1 - current_selection
            elif key == ord('\n') or key == curses.KEY_ENTER:
                if current_selection == 0:
                    curses.endwin()
                    exit()
                else:
                    break
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                if start_y + 4 == my and start_x + 2 <= mx < start_x + 8:
                    curses.endwin()
                    exit()
                elif start_y + 4 == my and start_x + 12 <= mx < start_x + 16:
                    break

    def run(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        self.draw_board()
        while True:
            key = self.stdscr.getch()
            if key == 27:  # ESC key
                self.show_exit_popup()
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                if my == h - 2 and w - 12 <= mx < w - 5:
                    self.show_exit_popup()

if __name__ == "__main__":
    curses.wrapper(Board)