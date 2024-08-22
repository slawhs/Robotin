from PyQt6.QtCore import pyqtSignal, QObject
from ultralytics import YOLO
from threading import Thread
import torch
import cv2


MODEL = "yolov8n-face.pt"
DEVICE = "cpu"


class FaceDetection(QObject):

    sender_pose = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.set_model()

        self.state = 0

    def set_model(self):
        self.device = torch.device(DEVICE)
        self.model = YOLO("models/"+MODEL).to(self.device)

    def start_detection(self):
        self.state = 1
        connection_thread = Thread(target=self.detect, daemon=True)
        connection_thread.start()

    def stop_detection(self):
        self.state = 0

    def detect(self):
        if self.state:
            cap = cv2.VideoCapture(0)
            while self.state:
                ret, frame = cap.read()

                results = self.model(frame, verbose=False)

                if len(results[0].boxes) > 0:
                    if len(results[0].boxes) > 1:
                        max_bb = sorted(results[0].boxes, key=lambda x: - (x.xyxy[0][2] - x.xyxy[0][0]) * (x.xyxy[0][3] - x.xyxy[0][1]))[0]
                    else:
                        max_bb = results[0].boxes[0]
                else:
                    max_bb = None

                if max_bb is not None:
                    x1, y1, x2, y2 = max_bb.xyxy[0][0:4]
                    self.sender_pose.emit(
                        (640 - (x1 + x2) / 2) / 640,
                        (y1 + y2 / 2) / 480
                    )
                else:
                    self.sender_pose.emit(0.5, 0.5)

