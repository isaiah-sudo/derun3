import math
import struct
import wave
import io
import os
import random

try:
    from ursina import Audio
except Exception:
    Audio = None

class SoundManager:
    """
    High-performance procedural synthesizer generating authentic synthwave SFX.
    Uses pure Python standard library wave synthesis cached to memory/disk.
    """
    def __init__(self):
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = True
        self.cache_dir = os.path.join(os.path.dirname(__file__), 'audio_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.generate_sfx_library()

    def _generate_wav(self, filename, samples, sample_rate=22050):
        filepath = os.path.join(self.cache_dir, filename)
        if not os.path.exists(filepath):
            try:
                with wave.open(filepath, 'w') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(sample_rate)
                    
                    data = bytearray()
                    for s in samples:
                        s = max(-1.0, min(1.0, s))
                        val = int(s * 32767.0)
                        data.extend(struct.pack('<h', val))
                    wav_file.writeframes(data)
            except Exception:
                return None
        return filepath

    def generate_sfx_library(self):
        sr = 22050

        # 1. Laser Fire SFX (downward pitch sweep)
        dur = 0.12
        num_s = int(sr * dur)
        laser_samples = []
        for i in range(num_s):
            t = i / float(sr)
            freq = 900.0 * (1.0 - (t / dur) ** 0.8) + 120.0
            phase = 2.0 * math.pi * freq * t
            val = 0.45 * (1.0 if math.sin(phase) > 0 else -1.0) * (1.0 - t / dur)
            laser_samples.append(val)
        self._generate_wav('laser.wav', laser_samples, sr)

        # 2. Shard Pickup SFX (High bell ping chime)
        dur = 0.14
        num_s = int(sr * dur)
        pickup_samples = []
        for i in range(num_s):
            t = i / float(sr)
            freq = 1100.0 + (i / num_s) * 600.0
            val = 0.45 * math.sin(2.0 * math.pi * freq * t) * math.exp(-t * 22.0)
            pickup_samples.append(val)
        self._generate_wav('pickup.wav', pickup_samples, sr)

        # 3. Jump Whoosh / Ramp Launch SFX
        dur = 0.22
        num_s = int(sr * dur)
        jump_samples = []
        for i in range(num_s):
            t = i / float(sr)
            freq = 220.0 + (t / dur) * 580.0
            val = 0.4 * math.sin(2.0 * math.pi * freq * t) * (1.0 - t / dur)
            jump_samples.append(val)
        self._generate_wav('jump.wav', jump_samples, sr)

        # 4. Explosion / Smash SFX
        dur = 0.25
        num_s = int(sr * dur)
        boom_samples = []
        for i in range(num_s):
            t = i / float(sr)
            noise = (random.random() * 2.0 - 1.0)
            env = math.exp(-t * 14.0)
            boom_samples.append(0.5 * noise * env)
        self._generate_wav('explosion.wav', boom_samples, sr)

        # 5. Speed Pad Boost SFX
        dur = 0.35
        num_s = int(sr * dur)
        boost_samples = []
        for i in range(num_s):
            t = i / float(sr)
            freq = 300.0 + (t / dur) * 750.0
            val = 0.4 * (1.0 if math.sin(2.0 * math.pi * freq * t) > 0 else -1.0) * math.exp(-t * 6.0)
            boost_samples.append(val)
        self._generate_wav('boost.wav', boost_samples, sr)

        # 6. EMP Shockwave SFX
        dur = 0.45
        num_s = int(sr * dur)
        emp_samples = []
        for i in range(num_s):
            t = i / float(sr)
            freq = 80.0 + math.sin(t * 40.0) * 40.0
            val = 0.6 * math.sin(2.0 * math.pi * freq * t) * (1.0 - t / dur)
            emp_samples.append(val)
        self._generate_wav('emp.wav', emp_samples, sr)

    def play(self, name, pitch=1.0, volume=0.6):
        if not self.sfx_enabled:
            return
        filepath = os.path.join(self.cache_dir, f'{name}.wav')
        if os.path.exists(filepath):
            try:
                from panda3d.core import Filename
                from direct.showbase.ShowBaseGlobal import base
                p3d_path = Filename.fromOsSpecific(filepath)
                snd = base.loader.loadSfx(p3d_path)
                if snd:
                    snd.setPlayRate(pitch)
                    snd.setVolume(volume)
                    snd.play()
            except Exception:
                pass

    def start_music(self):
        pass

    def stop_music(self):
        pass
