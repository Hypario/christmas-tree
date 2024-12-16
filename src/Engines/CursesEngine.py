from.EngineInterface import EngineInterface

import curses

from . import Color


class CursesEngine(EngineInterface):

    def __init__(self):
        # Initialize curses
        self.stdscr = curses.initscr()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        self.stdscr.keypad(True)

        # Start color, too.  Harmless if the terminal doesn't have
        # color; user can test with has_color() later on.  The try/catch
        # works around a minor bit of over-conscientiousness in the curses
        # module -- the error return from C start_color() is ignorable.
        try:
            curses.start_color()

            for color in Color:
                curses.init_pair(color.value, getattr(curses, f'COLOR_{color.name}'), curses.COLOR_BLACK)
        except:
            pass

    def hide_cursor(self) -> None:
        curses.curs_set(0)

    def addstr(self, string: str, color: Color = None) -> None:
        if color is not None:
            self.stdscr.addstr(string, curses.color_pair(color.value))
        else:
            self.stdscr.addstr(string)

    def addch(self, char: str, color: Color = None) -> None:
        if color is not None:
            self.stdscr.addch(char, curses.color_pair(color.value))
        else:
            self.stdscr.addch(char)

    def refresh(self) -> None:
        self.stdscr.refresh()

    def clear(self) -> None:
        self.stdscr.clear()

    def exit(self) -> None:
        # Set everything back to normal
        self.stdscr.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
