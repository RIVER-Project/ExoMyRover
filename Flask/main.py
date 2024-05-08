from flask import Flask, Response, render_template
import cv2

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
    app.run('0.0.0.0',port=5001 ,debug=True)
