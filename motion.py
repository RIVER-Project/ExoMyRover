import cv2
import numpy as np

# With a single camera we have two options:
# 1. We use some ML model to determine the distance well
# 2. We calibrate the distance for multiple objects (less good and time consuming)
# Another way would be to get two cameras or add sensors to get the depth:)    
class Motion:
    def __init__(self, camera, known_width, focal_length, rover):
        self.camera = camera
        self.known_width = known_width
        self.focal_length = focal_length
        self.rover = rover

    def detect_black_object_and_get_width(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([180, 255, 50])
        mask = cv2.inRange(hsv, lower_black, upper_black)

        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            object_width_in_pixels = w
            return frame, object_width_in_pixels
        else:
            return frame, 0

    def calculate_distance(self, width_in_pixels):
        if width_in_pixels > 0:
            return (self.known_width * self.focal_length) / width_in_pixels
        return 0

    def check_if_object_too_close(self, frame_width, object_width_in_pixels):
        threshold = 0.8 * frame_width
        if object_width_in_pixels > threshold:
            return True
        return False


    def generate_frames(self):
        while True:
            frame = self.camera.capture_array()
            frame, width_in_pixels = self.detect_black_object_and_get_width(frame)
            distance = self.calculate_distance(width_in_pixels)

            frame_width = frame.shape[1]
            if self.check_if_object_too_close(frame_width, width_in_pixels):
                self.rover.Stop_rover()

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            print('width:', width_in_pixels)
            print('distance', distance)
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')