import threading
import random
import time

from src.DriverInterface import DriverInterface


class MusicPlayer(threading.Thread):
    def __init__(self, driver: DriverInterface, songs, debug=False):
        super().__init__()
        self.driver = driver
        self.songs = songs # List of songs

        self.stop_flag = False # Flag to stop the thread gracefully
        self.debug = debug

    def run(self):
        random.shuffle(self.songs)
        for song in self.songs:
            if self.stop_flag: break

            self.driver.set_media("songs\\" + song)
            if self.debug: print(f"[MusicPlayer]: play songs\\{song}")

            if not self.driver.play():
                if self.debug: print(f"[MusicPlayer]: a problem occurred while trying to play {song}, stopping player")
                break

            while self.driver.is_playing():
                if self.stop_flag:
                    self.__force_stop()
                    break
                time.sleep(1.5)

    def stop(self):
        self.stop_flag = True

    def __force_stop(self):
        self.driver.stop()
        if self.debug: print("[MusicPlayer]: Player stopped")

    def is_running(self):
        return not self.stop_flag
