import curses

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_row = 0
        self.current_menu = "main"
        self.menus = {
            "main": ["Start Game", "View Statistics", "Exit Game"],
            "start_game": ["Classic Mode", "Timed Mode", "Back"],
            "classic_mode": ["Easy", "Hard", "Expert", "Back"]
        }

    def print_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        menu = self.menus[self.current_menu]
        for idx, row in enumerate(menu):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(menu) // 2 + idx
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

            if key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif key == curses.KEY_DOWN and self.current_row < len(self.menus[self.current_menu]) - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.handle_enter()
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                menu_start_y = h // 2 - len(self.menus[self.current_menu]) // 2
                menu_end_y = menu_start_y + len(self.menus[self.current_menu])
                if menu_start_y <= my < menu_end_y:
                    self.current_row = my - menu_start_y
                    if button_state & curses.BUTTON1_CLICKED:
                        self.handle_enter()

            self.print_menu()

    def handle_enter(self):
        menu = self.menus[self.current_menu]
        if self.current_menu == "main":
            if self.current_row == 0:
                self.current_menu = "start_game"
                self.current_row = 0
            elif self.current_row == 1:
                self.view_statistics()
            elif self.current_row == 2:
                exit()
        elif self.current_menu == "start_game":
            if self.current_row == 0:
                self.current_menu = "classic_mode"
                self.current_row = 0
            elif self.current_row == 1:
                self.timed_mode()
            elif self.current_row == 2:
                self.current_menu = "main"
                self.current_row = 0
        elif self.current_menu == "classic_mode":
            if self.current_row == 0:
                self.start_game("Easy")
            elif self.current_row == 1:
                self.start_game("Hard")
            elif self.current_row == 2:
                self.start_game("Expert")
            elif self.current_row == 3:
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