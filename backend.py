from flask import Flask, request, jsonify, render_template, Response
from RoverOOP import Rover, Joint
import cv2
from picamera2 import Picamera2
from adafruit_servokit import ServoKit
from gpiozero import ADC

# Initialize Flask app
app = Flask(__name__)

# Initialize the camera
try:
    camera = Picamera2()
    camera.preview_configuration.main.format = "RGB888"
    camera.start()
except Exception as e:
    print("Error initializing camera:", e)

# Initialize ServoKit
kit = ServoKit(channels=16)
servo180_1 = 535
servo180_2 = 2590
for i in range(6, 12):
    kit.servo[i].set_pulse_width_range(servo180_1, servo180_2)

# Initialize ADC for battery voltage reading
battery_adc = ADC(0)  # Assuming pin 0 is used for battery voltage reading

# Define global parameters for rover control
max_speed = 1
neutral_angle = 90
backward_direction = -1

# Define Joint objects
FLJ = Joint(0, 6)
FRJ = Joint(1, 7)
MLJ = Joint(2, 8)
MRJ = Joint(3, 9)
RLJ = Joint(4, 10)
RRJ = Joint(5, 11)

# Create the Rover object
rover = Rover(FLJ, FRJ, MLJ, MRJ, RLJ, RRJ)

# Define endpoint for receiving move commands
@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    direction = data.get('direction')

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
        return jsonify({'status': 'error', 'message': 'Invalid direction'}), 400

def move_forward():
    rover.Move_forward(neutral_angle)
    return jsonify({'status': 'success', 'action': 'move_forward'})

def move_backward():
    rover.Move_backward(neutral_angle)
    return jsonify({'status': 'success', 'action': 'move_backward'})

def move_left():
    rover.Move_forward(45)  # Assuming 45 degrees is the left movement angle
    return jsonify({'status': 'success', 'action': 'move_left'})

def move_right():
    rover.Move_forward(135)  # Assuming 135 degrees is the right movement angle
    return jsonify({'status': 'success', 'action': 'move_right'})

def stop_rover():
    rover.Stop_rover()
    return jsonify({'status': 'success', 'action': 'stop_rover'})

# Route for rendering index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route for video feed
def generate_frames():
    while True:
        try:
            frame = camera.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            print("Error capturing frame:", e)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def calculate_battery_percentage(voltage):

    max_voltage = 5.0  
    min_voltage = 0.0  

    voltage = max(min(voltage, max_voltage), min_voltage)

    battery_percentage = (voltage - min_voltage) / (max_voltage - min_voltage) * 100

    return battery_percentage


# Route for reading battery level
@app.route('/battery_level')
def battery_level():
    voltage = battery_adc.value * 3.3  # Assuming 3.3V reference voltage
    battery_percentage = calculate_battery_percentage(voltage) 
    return jsonify({'battery_level': battery_percentage})


if __name__ == '__main__':
    # Start Flask app
    app.run('0.0.0.0', 5000, debug=False, use_reloader=False)
