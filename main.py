from PyQt6.QtWidgets import QApplication
from face import MainWindow
import sys

FACE_DETECTION = True
SPEECH_RECOGNITION = True

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    if FACE_DETECTION:
        from face_detection import FaceDetection

        facedetection = FaceDetection()

        window.signal_start_detection.connect(facedetection.start_detection)
        window.signal_stop_detection.connect(facedetection.stop_detection)
        facedetection.sender_pose.connect(window.face.face_detectio_target)

    if SPEECH_RECOGNITION:
        from sst import SpeechToText

        stt_ = SpeechToText()

        window.signal_start_listening.connect(stt_.voice_reckoning_thread)
        window.signal_ajust_noise.connect(stt_.ajust_noise)
        stt_.listening_signal.connect(window.listening)
        stt_.text_signal.connect(window.speech_detected)

    window.show()
    sys.exit(app.exec())
