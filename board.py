import curses
import random

class Board:
    def __init__(self, stdscr, size=7):
        self.stdscr = stdscr
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.covered = [[True for _ in range(size)] for _ in range(size)]
        self.hints = [[' ' for _ in range(size)] for _ in range(size)]  # Initialize hints matrix
        self.words = [
            "PYTHON", "CODE", "DEBUG", "ALGORITHM", "FUNCTION",
            "VARIABLE", "LOOP", "CONDITION", "ARRAY", "STRING",
            "COMPUTER", "PROGRAM", "LANGUAGE", "DEVELOPER", "SOFTWARE",
            "HARDWARE", "NETWORK", "DATABASE", "SECURITY", "ENCRYPTION"
        ]
        self.selected_words = []
        self.revealed_words = set()
        self.word_reveal_status = {}  # Track the reveal status of each word
        self.common_letters = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
        self.word_complexity = {
            "PYTHON": 3, "CODE": 2, "DEBUG": 2, "ALGORITHM": 4, "FUNCTION": 3,
            "VARIABLE": 3, "LOOP": 1, "CONDITION": 3, "ARRAY": 2, "STRING": 2,
            "COMPUTER": 3, "PROGRAM": 2, "LANGUAGE": 3, "DEVELOPER": 3, "SOFTWARE": 3,
            "HARDWARE": 2, "NETWORK": 2, "DATABASE": 3, "SECURITY": 3, "ENCRYPTION": 4
        }
        self.fill_board()
        self.exit_prompt = False
        self.menu_button_clicked = False
        self.game_won = False
        self.move_count = 0  # Initialize move counter
        self.last_revealed = None  # Track the last revealed cell
        self.current_word = None  # Track the current word being revealed
        self.score = 0  # Initialize score

    def fill_board(self):
        # Reset the board and related variables
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.covered = [[True for _ in range(self.size)] for _ in range(self.size)]
        self.hints = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.selected_words = []
        self.revealed_words = set()
        self.word_reveal_status = {}
        self.move_count = 0
        self.last_revealed = None
        self.current_word = None
        self.score = 0

        # Filter out words longer than the board size
        valid_words = [word for word in self.words if len(word) <= self.size]

        # Randomly select 3 words to place on the board
        self.selected_words = random.sample(valid_words, 3)

        # Initialize the reveal status for each selected word
        for word in self.selected_words:
            self.word_reveal_status[word] = []

        # Randomly place words on the board
        placed_letters = set()
        word_positions = []
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
                            word_positions.append((row, col + i))
                        placed = True
                elif direction == 'V' and self.size - len(word) >= 0:
                    row = random.randint(0, self.size - len(word))
                    col = random.randint(0, self.size - 1)
                    if all(self.board[row + i][col] == ' ' for i in range(len(word))):
                        for i in range(len(word)):
                            self.board[row + i][col] = word[i]
                            placed_letters.add(word[i])
                            word_positions.append((row + i, col))
                        placed = True

        # Randomly fill some of the remaining empty cells with common letters
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ' and random.random() < 0.3:  # 30% chance to fill the cell
                    # Avoid using letters that are already placed in words
                    available_letters = [letter for letter in self.common_letters if letter not in placed_letters]
                    self.board[i][j] = random.choice(available_letters)  # Randomly choose a common letter

        # Randomly place mines around the words, but not on the edges
        mines_count = 0
        while mines_count < 5:
            for (row, col) in word_positions:
                for i in range(max(1, row - 1), min(self.size - 1, row + 2)):
                    for j in range(max(1, col - 1), min(self.size - 1, col + 2)):
                        if self.board[i][j] == ' ' and random.random() < 0.5:  # 50% chance to place a mine
                            self.board[i][j] = '*'
                            mines_count += 1
                            if mines_count >= 5:
                                break
                    if mines_count >= 5:
                        break
                if mines_count >= 5:
                    break

        # Calculate hints for each cell
        for i in range(self.size):
            for j in range(self.size):
                self.hints[i][j] = self.calculate_mine_hint(i, j)

    def calculate_mine_hint(self, row, col):
        hint = [' ', ' ']
        top_left = top_right = bottom_left = bottom_right = False

        for i in range(max(0, row - 1), min(self.size, row + 2)):
            for j in range(max(0, col - 1), min(self.size, col + 2)):
                if self.board[i][j] == '*':
                    if i < row and j < col:
                        top_left = True
                    elif i < row and j > col:
                        top_right = True
                    elif i > row and j < col:
                        bottom_left = True
                    elif i > row and j > col:
                        bottom_right = True

        if top_left and bottom_left:
            hint[0] = '⡁' if row > 0 else '⡀'
        elif top_left:
            hint[0] = '⠁'
        elif bottom_left:
            hint[0] = '⡀'

        if top_right and bottom_right:
            hint[1] = '⢈' if row < self.size - 1 else '⢀'
        elif top_right:
            hint[1] = '⠈'
        elif bottom_right:
            hint[1] = '⢀'

        return hint

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
            if word in self.revealed_words:
                self.stdscr.addstr(hint_start_y + idx + 1, 2, word)
            else:
                hint = " ".join("_" * len(word))
                self.stdscr.addstr(hint_start_y + idx + 1, 2, hint)

        # Draw move counter below the hint section
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 2, 2, f"Moves: {self.move_count}")

        # Draw score below the move counter
        self.stdscr.addstr(hint_start_y + len(self.selected_words) + 3, 2, f"Score: {self.score}")

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
                    if self.covered[i][j]:
                        self.stdscr.addstr(y + 1, x, '|▒▒▒')  # Do not change this line
                    else:
                        hint = self.hints[i][j]
                        cell_content = f'{hint[0]}{self.board[i][j]}{hint[1]}'
                        self.stdscr.addstr(y + 1, x, f'|{cell_content}')
                if i < self.size and j == self.size - 1:
                    self.stdscr.addstr(y + 1, x + 4, '|')

        # Ensure the bottom line is drawn correctly
        for j in range(self.size):
            x = start_x + j * 4
            y = start_y + self.size * 2
            self.stdscr.addstr(y, x, '+---')
        self.stdscr.addstr(y, x + 4, '+')

        # Draw the menu button and exit prompt on the same line
        if self.menu_button_clicked:
            self.stdscr.addstr(h - 2, w - 20, "[Click again to quit]", curses.A_REVERSE)
        else:
            self.stdscr.addstr(h - 2, w - 12, "[ Menu ]", curses.A_REVERSE)

        if self.exit_prompt:
            self.stdscr.addstr(h - 2, w - 50, "*Wanna quit? Press esc again to quit.")
        else:
            self.stdscr.addstr(h - 2, w - 50, "* Press 'esc' to quit")

        # Draw the winning message if the game is won
        if self.game_won:
            win_msg_y = h // 2 - 2
            self.stdscr.addstr(win_msg_y, w - 30, "Congratulations!")
            self.stdscr.addstr(win_msg_y + 1, w - 30, "You found all the words!")
            self.stdscr.addstr(win_msg_y + 3, w - 30, "Press N for New Game")
            self.stdscr.addstr(win_msg_y + 4, w - 30, "Press Q to Quit")

        self.stdscr.refresh()

    def calculate_base_score(self, word):
        word_length = len(word)
        word_complexity = self.word_complexity.get(word, 1)
        base_score = word_length * word_complexity
        return base_score

    def calculate_clean_reveal_bonus(self, clean_reveal):
        bonus_score = 0
        if clean_reveal:
            bonus_score = 10  # Example bonus for clean reveal
        return bonus_score

    def calculate_total_score(self, word, clean_reveal):
        base_score = self.calculate_base_score(word)
        clean_bonus = self.calculate_clean_reveal_bonus(clean_reveal)
        total_score = base_score + clean_bonus
        return total_score

    def check_revealed_words(self):
        for word in self.selected_words:
            revealed = True
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == word[0]:
                        if self.check_word_revealed(i, j, word, 'H') or self.check_word_revealed(i, j, word, 'V'):
                            if word not in self.revealed_words:
                                self.revealed_words.add(word)
                                self.word_reveal_status[word] = []  # Reset word reveal status
                                self.current_word = None  # Reset current word
                                clean_reveal = len(self.word_reveal_status[word]) == len(word)  # Ensure no redundant reveals
                                self.score += self.calculate_total_score(word, clean_reveal)

    def check_word_revealed(self, row, col, word, direction):
        if direction == 'H':
            if col + len(word) > self.size:
                return False
            for i in range(len(word)):
                if self.board[row][col + i] != word[i] or self.covered[row][col + i]:
                    return False
        elif direction == 'V':
            if row + len(word) > self.size:
                return False
            for i in range(len(word)):
                if self.board[row + i][col] != word[i] or self.covered[row + i][col]:
                    return False
        return True

    def check_all_words_revealed(self):
        return all(word in self.revealed_words for word in self.selected_words)

    def run(self):
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        self.draw_board()
        while True:
            key = self.stdscr.getch()
            if key == 27:  # ESC key
                if self.exit_prompt:
                    curses.endwin()
                    break
                else:
                    self.exit_prompt = True
                    self.draw_board()
            elif key == curses.KEY_MOUSE and not self.game_won:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                start_x = (w - (self.size * 4 + 1)) // 2
                start_y = (h - (self.size * 2 + 1)) // 2
                if start_y <= my < start_y + self.size * 2 and start_x <= mx < start_x + self.size * 4:
                    cell_x = (mx - start_x) // 4
                    cell_y = (my - start_y) // 2
                    if self.covered[cell_y][cell_x]:
                        self.covered[cell_y][cell_x] = False
                        self.move_count += 1  # Increment move counter
                        if self.board[cell_y][cell_x] == '*':
                            self.score -= 20  # Decrease score for revealing a mine
                            for word in self.selected_words:
                                self.word_reveal_status[word] = []  # Reset word reveal status for all words
                            self.current_word = None  # Reset current word
                        else:
                            self.last_revealed = (cell_y, cell_x)
                            # Check if the revealed cell is part of a selected word
                            for word in self.selected_words:
                                if self.board[cell_y][cell_x] in word:
                                    if self.current_word is None:
                                        self.current_word = word
                                    if self.current_word == word:
                                        self.word_reveal_status[word].append((cell_y, cell_x))
                            self.check_revealed_words()  # This will now only score for full word reveals
                        self.draw_board()
                        if self.check_all_words_revealed():
                            self.game_won = True
                            self.draw_board()
            elif key == ord('n') and self.game_won:
                self.__init__(self.stdscr, self.size)
                self.run()
            elif key == ord('q') and self.game_won:
                curses.endwin()
                break
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                if my == h - 2 and w - 12 <= mx < w - 5:
                    if self.menu_button_clicked:
                        curses.endwin()
                        break
                    else:
                        self.menu_button_clicked = True
                        self.draw_board()
                else:
                    self.menu_button_clicked = False
                    self.exit_prompt = False
                    self.draw_board()
            else:
                self.menu_button_clicked = False
                self.exit_prompt = False
                self.draw_board()

if __name__ == "__main__":
    curses.wrapper(Board)