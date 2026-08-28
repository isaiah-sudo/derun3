"""
Silent sound manager - all audio removed.
"""
class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.music_enabled = False
        self.sfx_enabled = False

    def play(self, name, pitch=1.0, volume=0.7):
        pass

    def start_music(self):
        pass

    def stop_music(self):
        pass
