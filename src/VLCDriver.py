from src.DriverInterface import DriverInterface

try:
    import vlc
except ModuleNotFoundError:
    raise ModuleNotFoundError("VLC or the python module is not installed.")

class VLCDriver(DriverInterface):
    def __init__(self, quiet=False):
        super().__init__(quiet)
        self.driver_instance = vlc.Instance("--quiet" if quiet else "")
        self.player = self.driver_instance.media_player_new()

    def set_media(self, file_path) -> None:
        self.player.set_media(self.driver_instance.media_new(file_path))

    def play(self) -> None:
        self.player.play()

    def stop(self) -> None:
        self.player.stop()

    def is_playing(self) -> bool:
        return self.player.is_playing()
