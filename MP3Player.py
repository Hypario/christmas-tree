# class is only imported if the OS is Windows

import ctypes
import os
import threading
import time

class MP3Player:
    def __init__(self, quiet=False):
        self.winmm = ctypes.windll.winmm
        self.playing = False
        self.thread = None
        self.quiet = quiet
        self.file_path = None

    def play(self):
        """Play an MP3 file using the Windows API."""
        if not os.path.isfile(self.file_path):
            if not self.quiet: print(f"File not found: {self.file_path}")
            return

        # Open the MP3 file
        command = f'open "{self.file_path}" type mpegvideo alias mp3'
        self.winmm.mciSendStringW(command, None, 0, None)

        # Play the MP3 file
        self.winmm.mciSendStringW("play mp3", None, 0, None)
        self.playing = True
        if not self.quiet: print(f"Playing: {self.file_path}")

        # Monitor the playback status in a thread
        def monitor_playback():
            while self.playing:
                status_buf = ctypes.create_unicode_buffer(128)
                self.winmm.mciSendStringW("status mp3 mode", status_buf, 128, None)
                if status_buf.value == "stopped":
                    self.playing = False
                time.sleep(0.1)

            self.stop()

        self.thread = threading.Thread(target=monitor_playback)
        self.thread.start()

    def set_media(self, file_path):
        self.file_path = file_path

    def is_playing(self):
        return self.playing

    def stop(self):
        """Stop the MP3 playback."""
        if self.playing:
            self.winmm.mciSendStringW("stop mp3", None, 0, None)
            self.winmm.mciSendStringW("close mp3", None, 0, None)
            self.playing = False
            if self.thread:
                self.thread.join()
            if not self.quiet: print("Playback stopped")