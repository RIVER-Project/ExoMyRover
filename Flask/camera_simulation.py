from picamera2 import Picamera2
from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize the camera
camera = Picamera2()
camera.resolution = (640, 480)
camera.start()

# Generator function for streaming frames
def generate_frames():
    while True:
        frame = camera.capture_array(format='jpeg', use_video_port=True)
        print(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

