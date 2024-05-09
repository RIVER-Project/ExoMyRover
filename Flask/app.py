from flask import Flask, Response, render_template, request
import cv2
from RoverOOP import Rover, Joint

app = Flask(__name__)

camera = cv2.VideoCapture(0)

FLJ = Joint(0, 6)  # Front Left Joint
FRJ = Joint(1, 7)  # Front Right Joint
MLJ = Joint(2, 8)  # Middle Left Joint
MRJ = Joint(3, 9)  # Middle Right Joint
RLJ = Joint(4, 10)  # Rear Left Joint
RRJ = Joint(5, 11)  # Rear Right Joint

# Create the Rover object, having as arguments the 6 Joint objects
Rover_obj = Rover(FLJ, FRJ, MLJ, MRJ, RLJ, RRJ)

def generate_frames():
    while True:
        success, frame = camera.read
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show $

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
def move_forward():
    # Code to move the robot forward
    Rover_obj.Move_forward(90)
    return 'Moved forward'


def move_backward():
    # Code to move the robot backward
    Rover_obj.Move_backward(90)
    return 'Moved backward'


def move_left():
    # Code to move the robot left
    return 'Moving left'


def move_right():
    # Code to move the robot right
    return 'Moving right'


def stop_rover():
    Rover_obj.Stop_rover()
    return 'Stopped rover'


@app.route('/')
def index():
    return render_template('index1.html')


# Move endpoint
@app.route('/move', methods=['POST'])
def move():
    direction = request.args.get('direction')
    if direction == 'forward':
        return move_forward()
    elif direction == 'backward':
        return move_backward()
    elif direction == 'left':
        return move_left()
    elif direction == 'right':
        return move_right()
    elif direction == 'stop':
        return stop_rover()
    else:
        return 'Invalid direction'


if __name__ == '__main__':
    Rover_obj.Move_forward(90)
    app.run('0.0.0.0', 5420, debug=True)
