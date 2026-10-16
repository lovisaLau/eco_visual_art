import numpy as np
import sounddevice as sd

class AudioManager:
    def __init__(self, rate=44100):
        self.rate = rate
        self.raw_volume = 0.0
        self.smoothed_volume = 0.0
        self.stream = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        
        rms = np.sqrt(np.mean(indata**2))
        threshold = 0.015
        if rms < threshold:
            scaled_rms = 0.0
        else:
            scaled_rms = (rms - threshold) * 140.0

        self.raw_volume = float(scaled_rms)

    def start(self):
        try:
            self.stream = sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=self.rate,
                blocksize=1024,
                latency='low',
            )
            self.stream.start()
        except Exception as e:
            print(f"Error al abrir el micrófono: {e}")

    def update(self):
        # Suavizado exponencial del volumen
        self.smoothed_volume += (self.raw_volume - self.smoothed_volume) * 0.08
        return self.smoothed_volume

    def stop(self):
        try:
            if self.stream:
                self.stream.stop()
                self.stream.close()
        except:
            pass