#!/usr/bin/env python3

import threading
import random
import os
import time
import vlc

media = vlc.MediaPlayer("audio.mp4")
media.play()

tree = list(open('tree.txt').read().rstrip())

mutex = threading.Lock()

def colored_dot(color):
    if color == 'red':
        return f'\033[91m●\033[0m'
    if color == 'green':
        return f'\033[92m●\033[0m'
    if color == 'yellow':
        return f'\033[93m●\033[0m'
    if color == 'blue':
        return f'\033[94m●\033[0m'
    pass

def lights(color, indexes):
    off = True
    while True:
        for i in indexes:
            tree[i] = colored_dot(color) if not off else '●'
        
        mutex.acquire()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(''.join(tree))
        mutex.release()

        off = not off

        time.sleep(random.uniform(.5, 1.5))

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

ty = threading.Thread(target=lights, args=('yellow', yellow))
tr = threading.Thread(target=lights, args=('red', red))
tg = threading.Thread(target=lights, args=('green', green))
tb = threading.Thread(target=lights, args=('blue', blue))

for t in [ty, tr, tg, tb]:
    t.start()

for t in [ty, tr, tg, tb]:
    t.join()
