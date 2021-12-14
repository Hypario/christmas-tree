import time
import curses
import os
import threading
import random
import vlc

def colored_dot(color):
    if color == 'red':
        return 1
    if color == 'green':
        return 2
    if color == 'yellow':
        return 3
    if color == 'blue':
        return 4
    pass

class StoppableThread(threading.Thread):
    
    def __init__(self, stdscr, tree, color, indexes):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.stdscr = stdscr
        self.tree = tree
        self.color = color
        self.indexes = indexes
    
    def stop(self):
        self._stop_event.set()
    
    def run(self):
        off = True
        while not self._stop_event.is_set():
            for i in self.indexes:
                if not off:
                    self.stdscr.attron(curses.color_pair(colored_dot(self.color)))
                    self.tree[i] = '●'
                    self.stdscr.attroff(curses.color_pair(colored_dot(self.color)))
                else:
                    self.tree[i] = '●'
            
            mutex.acquire()
            self.stdscr.clear()
            os.system('cls' if os.name == 'nt' else 'clear')
            self.stdscr.addstr(0, 0, ''.join(self.tree))
            self.stdscr.refresh()
            mutex.release()

            off = not off

            time.sleep(random.uniform(.5, 1.5))

songs = []
mutex = threading.Lock()

tree = []

stopped = False

# init screen
stdscr = curses.initscr()

curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

def clear():
    stdscr.clear()

# def print(str):
#    stdscr.addstr(str + "\n")

def write(str, *color):
    stdscr.addstr(str, curses.color_pair(color[0] if len(color) > 0 else 1))

refresh = stdscr.refresh()

clear()

# This prevents the program from having to wait for enter to be pressed
curses.cbreak()

def render():
    clear()

    # do the work

    refresh()

curses.noecho()

if os.path.exists(".\\songs"):
    for root, dirs, files in os.walk('.\\songs'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                songs.append(filename)
else:
    os.mkdir("songs")


# vlc_instance = vlc.Instance()
# player = vlc_instance.media_player_new()

# turn off cursor blinking
curses.curs_set(0)

# got a y coordinate, now need X coordinate
tree = open('tree.txt').read().rstrip().split("\n")  # todo : loop through all of those, and make a list of the string to get the X coordinates
print(tree)
"""
yellow = []
red = []
green = []
blue = []

for i, char in enumerate(tree):
    if char == 'Y':
        yellow.append(i)
        tree[i] = '●'
    if char == 'R':
        red.append(i)
        tree[i] = '●'
    if char == 'G':
        green.append(i)
        tree[i] = '●'
    if char == 'B':
        blue.append(i)
        tree[i] = '●'

ty = StoppableThread(stdscr, tree, 'yellow', yellow)
tr = StoppableThread(stdscr, tree, 'red', red)
tg = StoppableThread(stdscr, tree, 'green', green)
tb = StoppableThread(stdscr, tree, 'blue', blue)

for t in [ty, tr, tg, tb]:
    t.start()

while True:
    render()

    key = stdscr.getch()
    if key:
        for t in [ty, tr, tg, tb]:
            t.stop()
        break

    clear()
    refresh()

for t in [ty, tr, tg, tb]:
    t.join()

"""

# Reverse changes and return terminal to normal
curses.nocbreak()
curses.echo()
curses.endwin()