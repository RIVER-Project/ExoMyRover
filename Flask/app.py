from flask import Flask, render_template, request

app = Flask(__name__)

def move_forward():
    # Code to move the robot forward
    return 'Moving forward'

def move_backward():
    # Code to move the robot backward
    return 'Moving backward'

def move_left():
    # Code to move the robot left
    return 'Moving left'

def move_right():
    # Code to move the robot right
    return 'Moving right'

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
    else:
        return 'Invalid direction'

if __name__ == '__main__':
    app.run(debug=True)
