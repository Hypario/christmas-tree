# class is only imported if the OS is Windows

import ctypes
import os
import time
import uuid

from src.MusicDrivers.DriverInterface import DriverInterface


class WinmmDriver(DriverInterface):

    def __init__(self, quiet=False):
        super().__init__(quiet)

        # internal variables
        self.__winmm = ctypes.windll.winmm
        self.__alias = None
        self.__file_path = None
        self.__last_status = None
        self.__last_query_time = 0

    def set_media(self, file_path):
        self.__file_path = file_path

    def play(self):
        """Play an MP3 file using the Windows API."""

        self.__alias = f"mp3_{uuid.uuid4().hex[:8]}"

        self.__file_path = self.__file_path.replace("\\", "\\\\")
        if not os.path.isfile(self.__file_path):
            if not self.quiet: print(f"[WinmmDriver]: File {self.__file_path} not found")
            return

        # Open the MP3 file
        if self.__run_command(f'open "{self.__file_path}" type mpegvideo alias {self.__alias}') != 0: return

        # check if the file is ready
        status = self.__get_mci_status(self.__alias, 'ready')
        if status != "true":
            self.__run_command(f"close {self.__alias}")
            return

        # Play the MP3 file
        if self.__run_command(f"play {self.__alias}") != 0: return

        if not self.quiet: print(f"[WinmmDriver]: Playing {self.__file_path}")
        time.sleep(.5)  # wait a bit for the music to start playing
        return True

    def stop(self):
        """Stop the MP3 playback."""
        stop_result = self.__run_command(f"stop {self.__alias}")
        close_result = self.__run_command(f"close {self.__alias}")
        if stop_result == 0 and close_result == 0:
            if not self.quiet: print("[WinmmDriver]: Playback stopped")
            time.sleep(.5)  # wait a bit for the music to stop
            return True
        return False

    def is_playing(self) -> bool:
        mode = self.__get_status_with_caching(self.__alias, "mode")
        if mode != "playing": self.stop()
        return mode == "playing"

    def __run_command(self, command, status_buf=None, buf_size=0):
        if not self.quiet: print(f"[WinmmDriver]: Executing command '{command}'")
        result = self.__winmm.mciSendStringW(command, status_buf, buf_size, None)
        if result != 0: self.__get_mci_error(command, result)
        return result

    def __get_mci_status(self, alias, command):
        buffer_size = 128
        status_buffer = ctypes.create_unicode_buffer(buffer_size)
        command = f"status {alias} {command}"
        result = self.__run_command(command, status_buffer, buffer_size)
        if result != 0:
            self.__get_mci_error(command, result)
            return None
        return status_buffer.value

    def __get_mci_error(self, command, result):
        error_msg = ctypes.create_unicode_buffer(256)
        self.__winmm.mciGetErrorStringW(result, error_msg, 256)
        if not self.quiet: print(f"[WinmmDriver]: Error executing command '{command}': {error_msg.value}")

    def __get_status_with_caching(self, alias, command, cache_duration=1):
        current_time = time.time()
        if current_time - self.__last_query_time > cache_duration:
            self.__last_status = self.__get_mci_status(alias, command)
            self.__last_query_time = current_time
        return self.__last_status
