from flask import Flask, Response, render_template, stream_with_context, request
import cv2

from RoverOOP import Rover, Joint

video = cv2.VideoCapture(0)  # Initialize camera

app = Flask(__name__)

def video_stream():
    while True:
        ret, frame = video.read()  # Read frame from camera
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
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
