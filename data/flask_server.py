from flask import Flask, request, Response
from flask_socketio import SocketIO
from flask_cors import *
from receive import create_inlets_ECG, create_inlets_EEG
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
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')
CORS(app, supports_credentials=True)
disconnected = True

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

vs = VideoStream(src=0).start()
time.sleep(2.0)

emotion_queue = []

others_stream = {
    "heartRate": 1,
    "respiration": 1,
    "leftEnergy": 1,
    "ECG": 3000,
    "RESP": 3000,
    "EDA": 3000,
    "PULSE": 3000,
    "mean": 1,
    "variance": 1,
    "value": 1,
    "corrdinates": 120,
}

EEG_stream = {
    "emotion": 5,
    "topography": 100 * 300 * 3,
    "cognitiveLoad": 1,
    "vigilance": 1,
}

@app.route("/")
def index():
    return 'hello'


@socketio.on("connect")
def connect():
    global disconnected
    disconnected = False
    print("Client connected")


@socketio.on("disconnect")
def disconnect():
    global disconnected
    disconnected = True
    print("Client disconnected")
    

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")


def send_EEG_data():
    global disconnected
    inlet = create_inlets_EEG()
    while True:
        if not disconnected:
            sample, _ = inlet.pull_sample()
            print(f'EEG data len: {len(sample)}')
            json_data = parse_EEG_data(sample)
            socketio.emit("data", json_data)
            print(f"EEG data sent at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        socketio.sleep(3)


def send_other_data():
    global disconnected
    inlet = create_inlets_ECG()
    while True:
        if not disconnected:
            sample, _ = inlet.pull_sample()
            print(f'ECG data len: {len(sample)}')
            json_data = parse_other_data(sample)
            socketio.emit("data", json_data)
            print(f"Other data sent at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        socketio.sleep(3)


def send_all_data():
    global disconnected
    inlet1 = create_inlets_ECG()
    inlet2 = create_inlets_EEG()
    while True:
        if not disconnected:
            sample_ECG, _ = inlet1.pull_sample()
            sample_EEG, _ = inlet2.pull_sample()
            json_data_ECG = parse_other_data(sample_ECG)
            json_data_EEG = parse_EEG_data(sample_EEG)
            socketio.emit("data", json_data_ECG)
            socketio.emit("data", json_data_EEG)
            print(f"All data sent at: {time.strftime('%Y-%m-%d %H:%M:%S')}")


def parse_other_data(data):
    json_data = {}
    offset = 0

    for field in others_stream:
        length = others_stream[field]

        if field == 'corrdinates':
            field_data = data[offset:offset + length]
            json_data[field] = np.array(field_data).reshape(-1, 2).tolist()
        elif length == 1:
            json_data[field] = data[offset]
        else:
            json_data[field] = data[offset:offset + length]
        
        offset += length
        
    return json.dumps(json_data)


def parse_EEG_data(data):
    json_data = {}
    offset = 0

    for field in EEG_stream:
        length = EEG_stream[field]

        if field == 'emotion_history':
            field_data = data[offset:offset + length]
            json_data[field] = np.array(field_data).reshape(-1, 5).tolist()
        elif field == 'topography':
            field_data = data[offset:offset + length]
            json_data[field] = np.array(field_data).reshape(100, 300, 3).tolist()
        elif field == 'emotion':
            emotion = data[offset:offset + length]
            emotion_queue.append(emotion)
            if len(emotion_queue) > 30:
                emotion_queue.pop(0)
            json_data[field] = emotion
            json_data['emotionHistory'] = emotion_queue
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
            if frame is None:
                continue
            frame = imutils.resize(frame, width=400)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 进行Face Detection
            results_detection = face_detection.process(rgb_frame)

            # 进行Face Mesh
            results_mesh = face_mesh.process(rgb_frame)
            # 进行Face Mesh
            results_mesh = face_mesh.process(rgb_frame)

            # 如果检测到面部并提取到了面部特征点
            if results_mesh and results_mesh.multi_face_landmarks:
                for face_landmarks in results_mesh.multi_face_landmarks:
                    # 只绘制嘴部特征点
                    mouth_landmarks = [
                        61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 
                        291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 
                        95, 185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 
                        310, 311, 312, 13, 82, 81, 42, 183, 78
                    ]
                    for idx in mouth_landmarks:
                        x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                        y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                        cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            # 如果检测到面部
            # if results_detection and results_detection.detections:
            #     for detection in results_detection.detections:
            #         mp_drawing.draw_detection(frame, detection)

            # # 如果检测到面部并提取到了面部特征点
            # if results_mesh and results_mesh.multi_face_landmarks:
            #     for face_landmarks in results_mesh.multi_face_landmarks:
            #         mp_drawing.draw_landmarks(frame, face_landmarks, landmark_drawing_spec=landmark_drawing_spec)
            
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
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')


if __name__ == '__main__':
    t = threading.Thread(target=detect)
    t.daemon = True
    t.start()
    socketio.start_background_task(send_EEG_data)
    socketio.start_background_task(send_other_data)
    # socketio.start_background_task(send_all_data)
    socketio.run(app, host='0.0.0.0', port=8000)
    vs.stop()
