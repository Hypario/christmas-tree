#!/usr/bin/env python3

import threading
import random
import os
import time

from src import get_driver, MusicPlayer, get_engine, Color

debug = False

driver = get_driver(debug=debug)
engine = get_engine()

COLOR_MAP = {
    "Y": Color.YELLOW,
    "R": Color.RED,
    "G": Color.GREEN,
    "B": Color.BLUE,
}

# RESET_TERMINAL = "\033[0m"


def light_positions(tree):
    """
    Parses the tree to find the coordinates of lights (Y, R, G, B).
    Replaces lights with '●' in the original tree and returns coordinates.
    Returns:
        - Dictionary of {color: [(row, col)]} for lights grouped by color.
        - Updated tree with lights replaced by '●'.
    """
    light_coords = {"Y": [], "R": [], "G": [], "B": []}
    updated_tree = []

    for row, line in enumerate(tree):
        updated_line = ""
        for col, char in enumerate(line):

            if char in "YRGB":
                light_coords[char].append((row, col))
                updated_line += '●'  # Replace the light with a ball
            else:
                updated_line += char
        updated_tree.append(updated_line)

    return updated_tree, light_coords


def flicker_color(color_state, color):
    """
    Toggles the on/off state of all lights of a specific color.
    """
    while True:
        color_state[color] = not color_state[color]
        time.sleep(random.uniform(0.5, 1.5))  # Flicker at random intervals


def draw_tree(tree, light_coords, color_state):
    """
    Draws the tree with lights at specific coordinates, dynamically flickering by color.
    """
    for row, line in enumerate(tree):
        for col, char in enumerate(line.rstrip("\n")):
            light = next(
                (color for color, coords in light_coords.items() if (row, col) in coords),
                None,
            )
            if light:
                if color_state[light]:
                    engine.addstr('●', COLOR_MAP[light])
                else:
                    engine.addstr('●')
            else:
                engine.addch(char)
        engine.addch("\n")
    engine.refresh()

def main():
    engine.hide_cursor()

    tree = open('tree.txt').readlines()
    tree, light_coords = light_positions(tree)

    # Initialize the color states (every light of same colors light up at the same time)
    color_state = {color: False for color in COLOR_MAP.keys()}

    # Start threads for each light
    threads = []
    for color in COLOR_MAP.keys():
        thread = threading.Thread(target=flicker_color, args=(color_state, color), daemon=True)
        threads.append(thread)
        thread.start()

    # Get all songs
    songs = []

    if os.path.exists(".\\songs"):
        for root, dirs, files in os.walk('.\\songs'):
            for filename in files:
                if os.path.splitext(filename)[1] == ".mp3":
                    songs.append(filename)
    else:
        os.mkdir("songs")

    engine.clear()

    music_thread = MusicPlayer(driver, songs, debug=debug)
    music_thread.start()

    try:
        while True:
            if not debug:
                engine.clear()
                draw_tree(tree, light_coords, color_state)
            time.sleep(0.1)
    except KeyboardInterrupt:
        music_thread.stop()
        music_thread.join()

    engine.exit()

if __name__ == '__main__':
    main()
