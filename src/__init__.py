import platform

from .Engines import EngineInterface, Color
from .MusicPlayer import MusicPlayer

def get_driver(debug=False):
    try:
        from src.MusicDrivers import get_vlc_driver
        return get_vlc_driver(debug)
    except (ModuleNotFoundError, FileNotFoundError):
        if platform.system() == "Windows":
            # use the Winmm driver
            from src.MusicDrivers import get_winmm_driver
            return get_winmm_driver(debug)
        else:
            print("VLC is not installed, please install the module or the software, or use Windows")
            exit(-1)

def get_engine() -> EngineInterface:
    try:
        from .Engines import get_curse_engine

        return get_curse_engine()
    except ModuleNotFoundError:
        print("Curses not found, no alternative implemented yet, please install windows-curses")
        exit(-1)
