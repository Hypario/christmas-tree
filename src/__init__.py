import platform

def get_driver():
    driver = None
    try:
        from src.VLCDriver import VLCDriver

        driver = VLCDriver(quiet=True)
    except (ModuleNotFoundError, FileNotFoundError):
        if platform.system() == "Windows":
            # use the MP3Player class
            from src.WinmmDriver import WinmmDriver

            driver = WinmmDriver(quiet=True)
        else:
            print("VLC is not installed, please install the module or the software, or use Windows")
            exit(-1)
    return driver
