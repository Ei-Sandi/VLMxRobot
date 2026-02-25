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
        
        if device is None or isinstance(device, str):
            device = self._find_device_index(device)

        self.device = device
        print(f"Using audio device index: {self.device}")
        
        print(f"Loading voice model from: {model_path}...")
        self.voice = PiperVoice.load(model_path)
        print("Voice model loaded successfully.")

        try:
            from gpiozero import OutputDevice
            self.amp = OutputDevice(20) 
            self.amp.on()
            print("SunFounder amplifier enabled (GPIO 20 is HIGH).")
        except Exception as e:
            print(f"Note: Could not toggle GPIO 20 amp pin: {e}")

    def _find_device_index(self, name_hint):
        """Finds the audio device index by name."""
        try:
            devices = sd.query_devices()
            search_order = [name_hint] if name_hint else []
            search_order.extend(['hifiberry', 'dac', 'robothat', 'speaker', 'usb', 'vc4', 'hdmi']) 
            
            for keyword in search_order:
                for i, dev in enumerate(devices):
                    dev_name = dev.get('name', '')
                    if 'headphones' in dev_name.lower() and keyword not in ['headphones', 'bcm2835']:
                        continue
                        
                    if keyword.lower() in dev_name.lower() and dev.get('max_output_channels', 0) > 0:
                        print(f"Auto-detected audio device: '{dev_name}' (ID: {i})")
                        return i
                
            print("No matching audio device found. Using system default.")
            return None
        except Exception as e:
            print(f"Error finding device: {e}")
            return None
    
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
            channels = wav_file.getnchannels() 
            raw_frames = wav_file.readframes(wav_file.getnframes())
            
        audio_data = np.frombuffer(raw_frames, dtype=np.int16)
        audio_data = audio_data.reshape(-1, channels) 
            
        try:
            with sd.OutputStream(
                samplerate=self.voice.config.sample_rate, 
                device=self.device, 
                channels=channels, 
                dtype='int16'
            ) as stream:
                stream.write(audio_data)
        except Exception as e:
            print(f"Error playing audio: {e}")
            print("Try specifying the correct output device or check if volume is muted (alsamixer).")