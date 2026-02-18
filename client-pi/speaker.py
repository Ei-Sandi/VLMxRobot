import sounddevice as sd
import numpy as np
from piper.voice import PiperVoice
import wave
import io

class Speaker:
    def __init__(self, model_path="ufc_male.onnx", device=None):
        """Initializes the Speaker with a Piper voice model.
        
        Args:
            model_path (str): Path to the .onnx model.
            device (int or str, optional): Audio device index or substring name.
        """

        self.device = device
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
            
        try:
            with sd.OutputStream(samplerate=self.voice.config.sample_rate, 
                               channels=1, 
                               dtype='int16', 
                               device=self.device) as stream:
                 stream.write(audio_data)
        except Exception as e:
            print(f"Error playing audio: {e}")
            print("Try specifying the correct output device.")  
