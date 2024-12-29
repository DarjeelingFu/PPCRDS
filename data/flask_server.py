from flask import Flask, request, Response
from flask_socketio import SocketIO
from flask_cors import *
from receive import create_inlets
import json
import numpy as np
import time
import cv2
import mediapipe as mp
import threading
from imutils.video import VideoStream
import imutils

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app, supports_credentials=True)

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
def index():
    return 'hello'

@socketio.on("connect")
def connect():
    print("Client connected")

    def send_data(request):
        inlet = create_inlets()
        while True:
            sample, _ = inlet.pull_sample()
            json_data = parse_data(sample)
            socketio.emit("data", json_data)
            print(f"Data sent at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            socketio.sleep(3)

    socketio.start_background_task(send_data, request)

@socketio.on("disconnect")
def disconnect():
    print("Client disconnected")

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

def parse_data(data):
    field_length = {
        "heartRate": 1,
        "respiration": 1,
        "leftEnergy": 1,
        "ECG": 6000,
        "RESP": 6000,
        "EDA": 6000,
        "PULSE": 6000,
        "mean": 1,
        "variance": 1,
        "value": 1,
        "corrdinates": 120,
        "cognitiveLoad": 1,
        "vigilance": 1,
        "emotion": 5,
        "emotionHistory": 150
    }

    json_data = {}
    offset = 0

    for field in field_length:
        length = field_length[field]

        if field == 'corrdinates':
            field_data = data[offset:offset + length]
            json_data[field] = np.array(field_data).reshape(-1, 2).tolist()

        elif field == 'emotion_history':
            field_data = data[offset:offset + length]
            json_data[field] = np.array(field_data).reshape(-1, 5).tolist()
        
        elif length == 1:
            json_data[field] = data[offset]
        
        else:
            json_data[field] = data[offset:offset + length]
        
        offset += length
        
    return json.dumps(json_data)

def detect():
    global vs, outputFrame, lock
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection, \
        mp_face_mesh.FaceMesh(min_detection_confidence=0.1, min_tracking_confidence=0.1) as face_mesh:
        
        landmark_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)  # 调整thickness和circle_radius

        # loop over frames from the video stream
        while True:
            # read the next frame from the video stream, resize it,
            # convert the frame to grayscale, and blur it
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 进行Face Detection
            results_detection = face_detection.process(rgb_frame)

            # 进行Face Mesh
            results_mesh = face_mesh.process(rgb_frame)

            # 如果检测到面部
            if results_detection and results_detection.detections:
                for detection in results_detection.detections:
                    mp_drawing.draw_detection(frame, detection)

            # 如果检测到面部并提取到了面部特征点
            if results_mesh and results_mesh.multi_face_landmarks:
                for face_landmarks in results_mesh.multi_face_landmarks:
                    mp_drawing.draw_landmarks(frame, face_landmarks, landmark_drawing_spec=landmark_drawing_spec)
            
            with lock:
                outputFrame = frame.copy()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        print('yielding frame')
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

if __name__ == '__main__':
    t = threading.Thread(target=detect)
    t.daemon = True
    t.start()
    socketio.run(app, host='0.0.0.0', port=8000)
    vs.stop()