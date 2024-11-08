import curses
from board import Board

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_row = 0
        self.current_menu = "main"
        self.menus = {
            "main": ["Start Game", "View Statistics", "", "Exit Game"],
            "start_game": ["Classic Mode", "Timed Mode", "", "Back"],
            "classic_mode": ["Easy", "Hard", "Expert", "", "Back"]
        }
        self.descriptions = {
            "Start Game": "* Play some Wordweeper!",
            "View Statistics": "* Check data and statistics",
            "Exit Game": "* Exit the game",
            "Classic Mode": "* Play the classic mode",
            "Timed Mode": "* Play the timed mode",
            "Back": "* Go back to the previous menu",
            "Easy": "* Easy difficulty",
            "Hard": "* Hard difficulty",
            "Expert": "* Expert difficulty"
        }
        self.ascii_art = [
            "  __          __           _                                   ",
            "  \\ \\        / /          | |                                  ",
            "   \\ \\  /\\  / /__  _ __ __| |_      _____  ___ _ __   ___ _ __ ",
            "    \\ \\/  \\/ / _ \\| '__/ _` \\ \\ /\\ / / _ \\/ _ \\ '_ \\ / _ \\ '__|",
            "     \\  /\\  / (_) | | | (_| |\\ V  V /  __/  __/ |_) |  __/ |   ",
            "      \\/  \\/ \\___/|_|  \\__,_| \\_/\\_/ \\___|\\___| .__/ \\___|_|   ",
            "                                              | |                ",
            "                                              |_|                "
        ]

    def print_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        
        # Print ASCII art
        for i, line in enumerate(self.ascii_art):
            if len(line) > w:
                line = line[:w-1]  # Truncate line if it's too long
            self.stdscr.addstr(i, 0, line)
        
        menu = self.menus[self.current_menu]
        menu_start_y = (h - len(self.ascii_art) - len([item for item in menu if item != ""])) // 2 + len(self.ascii_art)
        for idx, row in enumerate(menu):
            x = 2  # Left-hand side with some padding
            y = menu_start_y + idx
            if row == "":
                self.stdscr.addstr(y, x, row)
                continue  # Skip empty lines for spacing
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        
        # Display description on the right-hand side
        description = self.descriptions.get(menu[self.current_row], "")
        description_x = w - len(description) - 2  # Right-hand side with some padding
        description_y = menu_start_y
        self.stdscr.addstr(description_y, description_x, description)
        
        self.stdscr.refresh()

    def run(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        self.print_menu()

        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.move_up()
                self.print_menu()
            elif key == curses.KEY_DOWN:
                self.move_down()
                self.print_menu()
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.handle_enter()
                self.print_menu()
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                menu_start_y = (h - len(self.ascii_art) - len([item for item in self.menus[self.current_menu] if item != ""])) // 2 + len(self.ascii_art)
                for idx, row in enumerate(self.menus[self.current_menu]):
                    if row == "":
                        continue  # Skip empty lines for spacing
                    y = menu_start_y + idx
                    if y == my:
                        self.current_row = idx
                        if button_state & curses.BUTTON1_CLICKED:
                            self.handle_enter()
                        self.print_menu()
                        break
            elif key == 27:  # ESC key
                self.handle_esc()
                self.print_menu()

    def move_up(self):
        menu = self.menus[self.current_menu]
        while True:
            self.current_row = (self.current_row - 1) % len(menu)
            if menu[self.current_row] != "":
                break

    def move_down(self):
        menu = self.menus[self.current_menu]
        while True:
            self.current_row = (self.current_row + 1) % len(menu)
            if menu[self.current_row] != "":
                break

    def handle_enter(self):
        menu = self.menus[self.current_menu]
        if self.current_menu == "main":
            if menu[self.current_row] == "Start Game":
                self.current_menu = "start_game"
                self.current_row = 0
            elif menu[self.current_row] == "View Statistics":
                self.view_statistics()
            elif menu[self.current_row] == "Exit Game":
                exit()
        elif self.current_menu == "start_game":
            if menu[self.current_row] == "Classic Mode":
                self.current_menu = "classic_mode"
                self.current_row = 0
            elif menu[self.current_row] == "Timed Mode":
                self.timed_mode()
            elif menu[self.current_row] == "Back":
                self.current_menu = "main"
                self.current_row = 0
        elif self.current_menu == "classic_mode":
            if menu[self.current_row] == "Easy":
                self.start_game("Easy")
            elif menu[self.current_row] == "Hard":
                self.start_game("Hard")
            elif menu[self.current_row] == "Expert":
                self.start_game("Expert")
            elif menu[self.current_row] == "Back":
                self.current_menu = "start_game"
                self.current_row = 0

    def handle_esc(self):
        if self.current_menu == "main":
            exit()
        else:
            self.current_menu = "main"
            self.current_row = 0

    def start_game(self, difficulty):
        if difficulty == "Easy":
            board = Board(self.stdscr, size=7)
            board.run()

    def timed_mode(self):
        # timed mode logic
        pass

    def view_statistics(self):
        # view statistics logic
        pass

if __name__ == "__main__":
    curses.wrapper(Menu)