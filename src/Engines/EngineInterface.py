from abc import ABC

from . import Color


class EngineInterface(ABC):

    def init(self) -> None:
        pass

    def hide_cursor(self) -> None:
        pass

    def addstr(self, string: str, color: Color = None) -> None:
        pass

    def addch(self, char: str, color: Color = None) -> None:
        pass

    def refresh(self) -> None:
        pass

    def clear(self) -> None:
        pass

    def exit(self) -> None:
        pass
