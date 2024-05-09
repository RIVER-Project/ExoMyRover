from flask import Flask, Response, render_template, stream_with_context, request
import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1920, 1080)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()
app = Flask(__name__)


def video_stream():
    while True:
        buffer = picam2.capture_array()
        frame = buffer.tobytes()
        yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5069, debug=False)
