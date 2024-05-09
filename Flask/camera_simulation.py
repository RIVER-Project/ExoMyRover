import cv2
from picamera2 import Picamera2
from flask import Flask, Response
import time

app = Flask(__name__)

# Initialize the camera
try:
    camera = Picamera2()
    camera.main.format= "RGB888"
    camera.start()
except Exception as e:
    print("Error initializing camera:", e)
# Generator function for streaming frames
def generate_frames():
    while True:
        try:
            frame = camera.capture_array()
            print(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Error capturing frame:", e)

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    time.sleep(5)
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

