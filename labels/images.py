from PyQt6.QtGui import QPainter, QBrush, QColor, QMouseEvent, QPixmap
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtWidgets import QLabel
import json

class Images(QLabel):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #000000; border-radius: 30px;")

        self.load_pixmaps()

        self.current_image = 0
        self.image_timer = QTimer(self)
        self.image_timer.timeout.connect(self.change_image)
        self.image_timer.start(3000)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


    def load_pixmaps(self):
        self.time_data = json.load(open('src/times.json'))['times']
        self.pixmaps = []
        for brand in self.time_data:
            pixmap = QPixmap(f'src/images/{brand}.jpg')
            # pixmap = pixmap.scaled(1400, 1400, Qt.AspectRatioMode.KeepAspectRatio)
            self.pixmaps.append(pixmap)

    def change_image(self):
        # self.current_image += 1
        self.current_image = (self.current_image + 1) % len(self.pixmaps)
        self.setPixmap(self.pixmaps[self.current_image])
        self.setScaledContents(True)

