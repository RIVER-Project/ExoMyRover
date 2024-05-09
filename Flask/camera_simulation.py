from flask import Flask, Response, render_template
import cv2

from RoverOOP import Rover, Joint

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Initialize camera


def gen_frames():
    while True:
        success, frame = camera.read()  # Read frame from camera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    FLJ = Joint(0, 6)  # Front Left Joint
    FRJ = Joint(1, 7)  # Front Right Joint
    MLJ = Joint(2, 8)  # Middle Left Joint
    MRJ = Joint(3, 9)  # Middle Right Joint
    RLJ = Joint(4, 10)  # Rear Left Joint
    RRJ = Joint(5, 11)  # Rear Right Joint

    # Create the Rover object, having as arguments the 6 Joint objects
    Rover_obj = Rover(FLJ, FRJ, MLJ, MRJ, RLJ, RRJ)
    app.run('0.0.0.0', port=5069, debug=True)
