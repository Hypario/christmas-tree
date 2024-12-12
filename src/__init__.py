import platform
from src.MusicPlayer import MusicPlayer

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
