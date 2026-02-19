import cv2
from picamera2 import Picamera2

class Camera():
    def __init__(self, jpeg_quality=90):
        self.camera = Picamera2()
        self.jpeg_quality = jpeg_quality

    def set_config(self, width, height):
        config = self.camera.create_still_configuration(
            main={"size": (width, height)},
        )
        self.camera.configure(config)
    
    def start(self):
        self.camera.start()

    def capture_array(self):
        frame = self.camera.capture_array()
        corrected_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return corrected_frame
    
    def capture_and_encode(self):
        image = self.camera.capture_array()
        corrected_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', corrected_frame, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality])
        return buffer
    
    def clean_up(self):
        self.camera.stop()
        self.camera.close()
