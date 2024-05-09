import picamera2  # camera module for RPi camera
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder, H264Encoder
import io

from flask import Flask, Response, request, render_template
from flask_restful import Resource, Api, reqparse, abort
from threading import Condition

app = Flask(__name__)
api = Api(app)


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


# defines the function that generates our frames
def genFrames():
    with picamera2.Picamera2() as camera:
        camera.configure(camera.create_video_configuration(main={"size": (640, 480)}))
        encoder = JpegEncoder()
        output3 = StreamingOutput()

        camera.start_encoder(encoder)
        camera.start()
        while True:
            with output3.condition:
                output3.condition.wait()
            frame = output3.frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# defines the route that will access the video feed and call the feed function
class video_feed(Resource):
    def get(self):
        return Response(genFrames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('camera.html')

api.add_resource(video_feed, '/cam')




if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
