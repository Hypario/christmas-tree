import time
import curses
import os
import sys
import threading
import random

try:
    import vlc
except:
    print("VLC is not installed, please install the module or the software")
    sys.exit(-1)

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

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

def pick_song():
    media = vlc_instance.media_new("songs\\" + songs[random.randint(0, len(songs) - 1)])
    player.set_media(media)
    player.play()
    time.sleep(1.5)
    duration = player.get_length() / 1000
    time.sleep(duration)
    pick_song()

class StoppableThread(threading.Thread):
    
    def __init__(self, stdscr, color, indexes):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.stdscr = stdscr
        self.color = color
        self.indexes = indexes
    
    def stop(self):
        self._stop_event.set()
    
    def run(self):
        off = True
        while not self._stop_event.is_set():
            for coords in self.indexes:
                if not off:
                    self.stdscr.attron(curses.color_pair(colored_dot(self.color)))
                    self.stdscr.addstr(coords[0], coords[1], '●')
                    self.stdscr.attroff(curses.color_pair(colored_dot(self.color)))
                else:
                    self.stdscr.addstr(coords[0], coords[1], '●')
            
            mutex.acquire()
            self.stdscr.refresh()
            mutex.release()

            off = not off

            time.sleep(random.uniform(.5, 1.5))

songs = []
mutex = threading.Lock()

if os.path.exists(".\\songs"):
    for root, dirs, files in os.walk('.\\songs'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                songs.append(filename)
else:
    os.mkdir("songs")

# init screen
stdscr = curses.initscr()

curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

def clear():
    stdscr.clear()

def write(str, *color):
    stdscr.addstr(str, curses.color_pair(color[0] if len(color) > 0 else 1))

def refresh():
    stdscr.refresh()

clear()

# This prevents the program from having to wait for enter to be pressed
curses.cbreak()

# turn off cursor blinking
curses.curs_set(0)

# avoid waiting for a key
stdscr.nodelay(True)

stdscr.move(0, 0)

yellow = []
red = []
green = []
blue = []


tree = open('tree.txt').read().rstrip().split("\n")

# print the tree
stdscr.addstr(0, 0, '\n'.join(tree))

for y, line in enumerate(tree):
    for x, char in enumerate(line):
        if char == 'Y':
            yellow.append((y, x))
            stdscr.addstr(y, x, '●')
        if char == 'R':
            red.append((y, x))
            stdscr.addstr(y, x, '●')
        if char == 'G':
            green.append((y, x))
            stdscr.addstr(y, x, '●')
        if char == 'B':
            blue.append((y, x))
            stdscr.addstr(y, x, '●')

curses.noecho()

if os.path.exists(".\\songs"):
    for root, dirs, files in os.walk('.\\songs'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                songs.append(filename)
else:
    os.mkdir("songs")



ty = StoppableThread(stdscr, 'yellow', yellow)
tr = StoppableThread(stdscr, 'red', red)
tg = StoppableThread(stdscr, 'green', green)
tb = StoppableThread(stdscr, 'blue', blue)

if (len(songs) > 0):
    tsong = threading.Thread(target=pick_song)
    tsong.start()

for t in [ty, tr, tg, tb]:
    t.start()

while True:
    key = stdscr.getch()

    if key != -1:
        if key == 114:
            stdscr.clear()
            stdscr.move(0, 0)
            # print the tree
            stdscr.addstr(0, 0, '\n'.join(tree))

            for y, line in enumerate(tree):
                for x, char in enumerate(line):
                    if char == 'Y':
                        stdscr.addstr(y, x, '●')
                    if char == 'R':
                        stdscr.addstr(y, x, '●')
                    if char == 'G':
                        stdscr.addstr(y, x, '●')
                    if char == 'B':
                        stdscr.addstr(y, x, '●')

            stdscr.refresh()
        else:
            for t in [ty, tr, tg, tb]:
                t.stop()
            break

for t in [ty, tr, tg, tb]:
    t.join()

if (len(songs) > 0):
    tsong.join()

# Reverse changes and return terminal to normal
curses.nocbreak()
curses.echo()
stdscr.clear()
curses.endwin()
