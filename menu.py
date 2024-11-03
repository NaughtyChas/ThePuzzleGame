import curses

class Menu:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_row = 0
        self.menu = ["Start Game", "Select difficulty", "Exit"]

    def print_menu(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        for idx, row in enumerate(self.menu):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(self.menu) // 2 + idx
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
            elif key == curses.KEY_DOWN and self.current_row < len(self.menu) - 1:
                self.current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if self.current_row == len(self.menu) - 1:
                    break
                elif self.current_row == 0:
                    self.start_game()
                elif self.current_row == 1:
                    self.select_difficulty()
            elif key == curses.KEY_MOUSE:
                _, mx, my, _, button_state = curses.getmouse()
                h, w = self.stdscr.getmaxyx()
                menu_start_y = h // 2 - len(self.menu) // 2
                menu_end_y = menu_start_y + len(self.menu)
                if menu_start_y <= my < menu_end_y:
                    self.current_row = my - menu_start_y
                    if button_state & curses.BUTTON1_CLICKED:
                        if self.current_row == len(self.menu) - 1:
                            break
                        elif self.current_row == 0:
                            self.start_game()
                        elif self.current_row == 1:
                            self.select_difficulty()

            self.print_menu()

    def start_game(self):
        # start game logic
        pass

    def select_difficulty(self):
        # select difficulty logic
        pass

if __name__ == "__main__":
    curses.wrapper(Menu)