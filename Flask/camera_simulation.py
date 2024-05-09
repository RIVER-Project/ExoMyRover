from picamera2 import Picamera2
import io
from flask import Flask, Response, render_template

app = Flask(__name__)


# Create a streaming output object
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = picamera2.Picamera2Lock()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


# Camera initialization
camera = Picamera2()
camera.resolution = (640, 480)
output = StreamingOutput()
camera.start_recording(output, format='mjpeg')


@app.route('/')
def index():
    return render_template('camera.html')


# Generator function for streaming frames
def generate():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
