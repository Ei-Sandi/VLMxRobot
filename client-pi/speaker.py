import sounddevice as sd
import numpy as np
from piper.voice import PiperVoice
import wave
import io

class Speaker:
    def __init__(self, model_path="ufc_male.onnx"):
        """Initializes the Speaker with a Piper voice model."""
        print(f"Loading voice model from: {model_path}...")
        self.voice = PiperVoice.load(model_path)
        print("Voice model loaded successfully.")
    
    def speak(self, text):
        """Synthesizes speech in memory and plays it immediately."""
        if not text:
            return
        
        print(f"Robot says: {text}")
        
        audio_buffer = io.BytesIO()
        
        with wave.open(audio_buffer, 'wb') as wav_file:
            self.voice.synthesize_wav(text, wav_file)
        
        audio_buffer.seek(0)
        
        with wave.open(audio_buffer, 'rb') as wav_file:
            raw_frames = wav_file.readframes(wav_file.getnframes())
            audio_data = np.frombuffer(raw_frames, dtype=np.int16)
            
        sd.play(audio_data, samplerate=self.voice.config.sample_rate)
        sd.wait()  
