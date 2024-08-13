import sys
from time import sleep
from random import randint
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QBrush, QColor, QMouseEvent, QPixmap
from PyQt6.QtCore import Qt, QPoint, QTimer
from ultralytics import YOLO
import cv2 
import torch


class Face(QWidget):

    blink_step = 6
    speak_step = 6

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMouseTracking(True)

        self.scale = 10

        self.blink_count = 0
        self.speak_count = 0

        self.eye_size = 12
        self.mouth_size = 1

        self.speaking = 0

        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink)
        self.blink_timer.start(self.blink_step)

        self.speak_timer = QTimer(self)
        self.speak_timer.timeout.connect(self.speak)
        self.speak_timer.start(self.speak_step)

        # self.move_timer = QTimer(self)
        # self.move_timer.timeout.connect(self.move_face)
        # self.move_timer.start(self.step)

        # self.move_ = 0

    @property
    def c_x(self):
        return int(self.width()/2)

    @property
    def c_y(self):
        return int(self.height()/2)

    def resizeEvent(self, event):
        self.scale = min(event.size().height()*0.015, event.size().width()*0.015)
        self.centro_ojos = QPoint(self.c_x, self.c_y)
        self.centro_boca = QPoint(self.c_x, self.c_y + int(self.scale*8))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # -- Ojos --
        painter.setBrush(QBrush(QColor( 30,  30,  30)))
        painter.drawEllipse(self.centro_ojos + QPoint(-int(20 * self.scale), 0), int(5 * self.scale), int(self.eye_size * self.scale))
        painter.drawEllipse(self.centro_ojos + QPoint( int(20 * self.scale), 0), int(5 * self.scale), int(self.eye_size * self.scale))

        # -- Boca --
        painter.setBrush(QBrush(QColor( 30,  30,  30)))
        painter.drawEllipse(
            self.centro_boca,
            int(6 * self.scale),
            int(3 * self.scale))

        painter.setBrush(QBrush(QColor(194, 216, 214)))
        painter.drawEllipse(
            self.centro_boca,
            int(5 * self.scale),
            int(2 * self.scale * self.mouth_size))
        painter.drawRect(
            self.centro_boca.x() - int(6 * self.scale),
            self.centro_boca.y() - int(4 * self.scale),
            int(12 * self.scale),
            int( 4 * self.scale))

        painter.setBrush(QBrush(QColor( 30,  30,  30)))
        painter.drawEllipse(self.centro_boca + QPoint(
            -int(5.5 * self.scale), 0),
            int(0.55 * self.scale),
            int(0.55 * self.scale))
        painter.drawEllipse(self.centro_boca + QPoint(
            int(5.5 * self.scale), 0),
            int(0.55 * self.scale),
            int(0.55 * self.scale))


    def mouseMoveEvent(self, event: QMouseEvent):
        self.centro_ojos = QPoint(
            int(self.c_x + (event.pos().x() - self.c_x) * 0.5),
            int(self.c_y + (event.pos().y() - self.c_y) * 0.5)
        )
        self.centro_boca = QPoint(
            int(self.c_x + (event.pos().x() - self.c_x) * 0.45),
            int(self.c_y + (event.pos().y() - self.c_y) * 0.45) + int(8 * self.scale)
        )
        self.update()
    
    def faceDetectionMove(self, facepos):
        self.centro_ojos = QPoint(
            int(self.c_x + (facepos[0]*self.width() - self.c_x) * 0.5),
            int(self.c_y + (facepos[1]*self.height() - self.c_y) * 0.5)
        )
        self.centro_boca = QPoint(
            int(self.c_x + (facepos[0]*self.width() - self.c_x) * 0.45),
            int(self.c_y + (facepos[1]*self.height() - self.c_y) * 0.45) + int(8 * self.scale)
        )
        self.update()

    def blink(self):
        self.blink_count += self.blink_step
        if self.blink_count < 100:
            self.eye_size = 12 - self.blink_count/10
        elif self.blink_count < 200:
            self.eye_size = 2 + (self.blink_count - 100)/10
        elif self.blink_count > 4000:
            self.blink_count = 0
        self.update()

    def speak(self):
        if self.speaking:
            self.speak_count += self.speak_step
            if self.speak_count < 150:
                self.mouth_size = 1 - self.speak_count/150
            elif self.speak_count < 300:
                self.mouth_size = (self.speak_count - 150)/300
            else:
                self.speak_count = 0
        else:
            self.speak_count = 100
            self.mouth_size = 1

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.blink_count = 75

    # def move_face(self):

    #     if self.move_ == 0:
    #         if randint(0, 100) < 10:
    #             self.move_ = 1
    #             self.target = QPoint(randint(0, self.width()), randint(int(self.height()*0.4), self.height()))

    #     else:

    #         self.centro_ojos = QPoint(
    #             int(self.c_x + (event.pos().x() - self.c_x) * 0.5),
    #             int(self.c_y + (event.pos().y() - self.c_y) * 0.5)
    #         )
    #         self.centro_boca = QPoint(
    #             int(self.c_x + (event.pos().x() - self.c_x) * 0.45),
    #             int(self.c_y + (event.pos().y() - self.c_y) * 0.45) + int(8 * self.scale)
    #         )
    #         self.update()


class TextBox(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: #9aabaa;  color: rgb(30,30,30); font-size: 30px; border: 5px solid rgb(0,0,0); border-radius: 20px;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robotin")
        self.setStyleSheet("background-color: rgb(194,216,214);")
        # self.resize(200, 400)
        self.showFullScreen()

        self.layout = QVBoxLayout()
        self.face = Face()
        self.face_detection = FaceDetection(self.face)
        self.layout.addWidget(self.face, 3)

        self.layout.addWidget(TextBox("sas", self), 1)
        pixmap = QPixmap('wasil.jpg')
        pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        self.layout.addWidget(image_label, 27)
        # self.layout.setContentsMargins(1, 1, 1, 0)
        self.layout.itemAt(1).widget().hide()
        self.layout.itemAt(2).widget().hide()

        widget = QWidget()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        if event.key() == Qt.Key.Key_1:
            self.layout.itemAt(1).widget().hide()
            self.layout.itemAt(2).widget().hide()
        if event.key() == Qt.Key.Key_2:
            self.layout.itemAt(1).widget().show()
            self.layout.itemAt(2).widget().hide()
        if event.key() == Qt.Key.Key_3:
            self.layout.itemAt(1).widget().hide()
            self.layout.itemAt(2).widget().show()
        if event.key() == Qt.Key.Key_Space:
            self.layout.itemAt(0).widget().speaking = not self.layout.itemAt(0).widget().speaking
        
        if self.face_detection.state == "Off":
            if event.key() == Qt.Key.Key_D: # Cambiamos a deteccion si apretamos D y no estamos en deteccion
                self.face.setMouseTracking(False)
                self.face_detection.detect()
        
            if event.key() == Qt.Key.Key_S: # Cambiamos a mouse follow si apretamos S y no estamos en deteccion
                self.face.setMouseTracking(True)

        # Para apagar la deteccion debemos presionar Q imentras estamos en deteccion
            


class FaceDetection:
    def __init__(self, robotin):
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.robotin = robotin
        self.device = torch.device("cpu")
        model = YOLO("best2.pt")
        self.model = model.to(self.device)
        self.facepos = None
        self.state = "Off"

    def detect(self):
        self.state = "On"
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()

            # Realizamos la deteccion
            results = self.model(frame)

            # Encontramos el bounding box mas grande
            max_area = 0
            max_bb = None
            for result in results[0].boxes:  # Accede a los resultados de las cajas
                x1, y1, x2, y2 = result.xyxy[0].cpu().numpy().astype(int)
                area = (x2 - x1) * (y2 - y1)
                if area > max_area:
                    max_area = area
                    max_bb = result

            if max_bb is not None:
                x1, y1, x2, y2 = max_bb.xyxy[0].cpu().numpy().astype(int)
                # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # label = f'{self.model.names[int(max_bb.cls[0].cpu().numpy())]} {max_bb.conf[0].cpu().numpy():.2f}'
                # cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # print(f'Centro: {(x1 + x2) / 2}, {(y1 + y2) / 2}')
                self.robotin.faceDetectionMove((
                    (640 - ((x1 + x2) / 2)) / 640,
                    ((y1 + y2) / 2) /480
                    ))

            # cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                cap.release()
                self.state = "Off"
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
