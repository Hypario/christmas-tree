from src.MusicDrivers import DriverInterface

def get_vlc_driver(debug=False):
    from src.MusicDrivers.VLCDriver import VLCDriver

    return VLCDriver(quiet=not debug)

def get_winmm_driver(debug=False):
    from src.MusicDrivers.WinmmDriver import WinmmDriver
    return WinmmDriver(quiet=not debug)
