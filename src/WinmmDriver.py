from src import MP3Player
from src.DriverInterface import DriverInterface


class WinmmDriver(DriverInterface):

    def __init__(self, quiet=False):
        super().__init__(quiet)
        self.player = MP3Player.MP3Player(quiet=self.quiet)

    def set_media(self, file_path):
        self.player.set_media(file_path)

    def play(self):
        self.player.play()

    def stop(self):
        self.player.stop()

    def is_playing(self) -> bool:
        return self.player.is_playing()
