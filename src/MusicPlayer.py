import threading
import random
import time

from src.DriverInterface import DriverInterface


class MusicPlayer(threading.Thread):
    def __init__(self, driver: DriverInterface, songs):
        super().__init__()
        self.driver = driver
        self.songs = songs # List of songs

        self.stop_flag = False # Flag to stop the thread gracefully

    def run(self):
        random.shuffle(self.songs)
        for song in self.songs:
            if self.stop_flag: break

            self.driver.set_media("songs\\" + song)

            self.driver.play()

            while self.driver.is_playing():
                if self.stop_flag:
                    self.stop()
                    break
                time.sleep(1.5)

    def stop(self):
        self.stop_flag = True
        self.driver.stop()
