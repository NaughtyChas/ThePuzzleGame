import curses

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
        self.ascii_art = [
            "  __          __           _                                   ",
            "  \\ \\        / /          | |                                  ",
            "   \\ \\  /\\  / /__  _ __ __| |_      _____  ___ _ __   ___ _ __ ",
            "    \\ \\/  \\/ / _ \\| '__/ _` \\ \\ /\\ / / _ \\/ _ \\ '_ \\ / _ \\ '__|",
            "     \\  /\\  / (_) | | | (_| |\\ V  V /  __/  __/ |_) |  __/ |   ",
            "      \\/  \\/ \\___/|_|  \\__,_| \\_/\\_/ \\___|\\___| .__/ \\___|_|   ",
            "                                           | |                ",
            "                                           |_|                "
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
        for idx, row in enumerate(menu):
            if row == "":
                continue  # Skip empty lines for spacing
            x = w // 2 - len(row) // 2
            y = len(self.ascii_art) + 1 + idx
            if idx == self.current_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
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
            elif key == curses.KEY_DOWN:
                self.move_down()
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.handle_enter()
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                menu_start_y = len(self.ascii_art) + 1
                menu_end_y = menu_start_y + len([item for item in self.menus[self.current_menu] if item != ""])
                if menu_start_y <= my < menu_end_y:
                    self.current_row = my - menu_start_y
                    if button_state & curses.BUTTON1_CLICKED:
                        self.handle_enter()

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
            if self.current_row == 0:
                self.current_menu = "start_game"
                self.current_row = 0
            elif self.current_row == 1:
                self.view_statistics()
            elif self.current_row == 3:
                exit()
        elif self.current_menu == "start_game":
            if self.current_row == 0:
                self.current_menu = "classic_mode"
                self.current_row = 0
            elif self.current_row == 1:
                self.timed_mode()
            elif self.current_row == 3:
                self.current_menu = "main"
                self.current_row = 0
        elif self.current_menu == "classic_mode":
            if self.current_row == 0:
                self.start_game("Easy")
            elif self.current_row == 1:
                self.start_game("Hard")
            elif self.current_row == 2:
                self.start_game("Expert")
            elif self.current_row == 4:
                self.current_menu = "start_game"
                self.current_row = 0

    def start_game(self, difficulty):
        # start game logic with difficulty
        pass

    def timed_mode(self):
        # timed mode logic
        pass

    def view_statistics(self):
        # view statistics logic
        pass

if __name__ == "__main__":
    curses.wrapper(Menu)