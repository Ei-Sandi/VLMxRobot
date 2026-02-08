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
        return self.camera.capture_array()
    
    def capture_and_encode(self):
        image = self.camera.capture_array()
        _, buffer = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality])
        return buffer
    
    def clean_up(self):
        self.camera.stop()
        self.camera.close()
