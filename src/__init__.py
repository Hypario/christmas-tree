import platform

def get_driver(debug=False):
    driver = None
    try:
        from src.VLCDriver import VLCDriver

        driver = VLCDriver(quiet=not debug)
    except (ModuleNotFoundError, FileNotFoundError):
        if platform.system() == "Windows":
            # use the Winmm driver
            from src.WinmmDriver import WinmmDriver

            driver = WinmmDriver(quiet=not debug)
        else:
            print("VLC is not installed, please install the module or the software, or use Windows")
            exit(-1)
    return driver
