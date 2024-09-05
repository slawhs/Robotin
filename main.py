from PyQt6.QtWidgets import QApplication
from modules.main_window import MainWindow
import sys

LLM = True
FACE_DETECTION = False

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    if FACE_DETECTION:
        from modules.face_detection import FaceDetection

        facedetection = FaceDetection()

        window.signal_start_detection.connect(facedetection.start_detection)
        window.signal_stop_detection.connect(facedetection.stop_detection)
        facedetection.sender_pose.connect(window.face.face_detectio_target)

    if LLM:
        from modules.sst import SpeechToText
        from modules.llm import Llama

        stt_ = SpeechToText()
        llm_ = Llama()

        window.signal_start_listening.connect(stt_.voice_reckoning_thread)
        window.signal_ajust_noise.connect(stt_.ajust_noise)
        stt_.listening_signal.connect(window.listening)
        stt_.text_signal.connect(llm_.llama_thread)
        llm_.response_signal.connect(window.speech_detected)


    window.show()
    sys.exit(app.exec())
