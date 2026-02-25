import sounddevice as sd
import sys
import os

# Add parent directory to path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speaker import Speaker

def test_speaker():
    print("Listing audio devices:")
    try:
        print(sd.query_devices())
    except Exception as e:
        print(f"Error querying devices: {e}")

    print("\nInitializing Speaker...")
    try:
        # Construct path to model relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        model_path = os.path.join(project_root, "ufc_male.onnx")
        
        speaker = Speaker(model_path=model_path)
        print("Speaker initialized.")
        
        text = "This is a test of the speaker system."
        print(f"Speaking: '{text}'")
        speaker.speak(text)
        print("Done speaking.")
        
    except Exception as e:
        print(f"Error during speaker test: {e}")

if __name__ == "__main__":
    test_speaker()
