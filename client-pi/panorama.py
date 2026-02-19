import time
import cv2
import numpy as np

class PanoramaScanner:
    def __init__(self, car, camera):
        self.car = car
        self.camera = camera
        
        self.tilt_angles = [0, -29] 
        self.pan_angles = [-42, 0, 42]
        self.quality = 70

    def capture_grid(self):
        """
        Internal method to capture the 2x3 grid.
        Returns a list of numpy arrays.
        """
        images = []
        
        for tilt in self.tilt_angles:
            self.car.set_cam_tilt_angle(tilt)
            time.sleep(1) 
            
            for pan in self.pan_angles:
                self.car.set_cam_pan_angle(pan)
                time.sleep(1) 
                
                frame = self.camera.capture_array()
                
                if frame is not None:
                    images.append(frame)
                    print(f"Captured frame at Tilt: {tilt}, Pan: {pan}")
                else:
                    print(f"Failed to capture frame at Tilt: {tilt}, Pan: {pan}")
        
        self.car.set_cam_tilt_angle(0)
        self.car.set_cam_pan_angle(0)
        return images

    def scan(self):
        """
        Captures the grid and returns the encoded multipart message list.
        Returns: list of bytes [b'PANORAMA', img1_bytes, img2_bytes, ...]
        """
        grid_images = self.capture_grid()
        
        if grid_images:
            encoded_grid = [b'PANORAMA']
            
            for img in grid_images:
                _, buf = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), self.quality])
                encoded_grid.append(buf)
            
            return encoded_grid
        return None

