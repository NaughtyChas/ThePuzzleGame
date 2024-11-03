import curses
from menu import Menu

def main(stdscr):
    menu = Menu(stdscr)
    menu.run()

if __name__ == "__main__":
    curses.wrapper(main)