from .EngineInterface import EngineInterface
from .Color import Color

def get_curse_engine() -> EngineInterface:
    from .CursesEngine import CursesEngine

    return CursesEngine()
