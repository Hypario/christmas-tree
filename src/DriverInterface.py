from abc import ABC

class DriverInterface(ABC):

    def __init__(self, quiet=False):
        self.quiet = quiet

    def set_media(self, file_path) -> None:
        pass

    def play(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def is_playing(self) -> bool:
        pass
