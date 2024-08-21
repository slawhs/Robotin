from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QBrush, QColor, QMouseEvent, QPixmap
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtCore import pyqtSignal


class TextBox(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("background-color: #9aabaa;  color: rgb(30,30,30); font-size: 30px; border: 5px solid rgb(0,0,0); border-radius: 20px;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
