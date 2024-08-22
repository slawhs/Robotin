from PyQt6.QtCore import pyqtSignal, QObject
import speech_recognition as sr
from threading import Thread
import pyttsx3


class SpeechToText(QObject):

    listening_signal = pyqtSignal()
    text_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.set_recognizer()

    def set_recognizer(self):
        self.recognizer = sr.Recognizer()
        self.source = sr.Microphone()

    def ajust_noise(self):
        self.recognizer.adjust_for_ambient_noise(self.source)

    def voice_reckoning_thread(self):
        connection_thread = Thread(target=self.voice_reckoning, daemon=True)
        connection_thread.start()

    def voice_reckoning(self):
        self.listening_signal.emit()
        with self.source as source:
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language="es-ES")
            except sr.UnknownValueError:
                text = "No se pudo entender el audio"
            except sr.RequestError as e:
                text = f"Error al conectar con el servicio de reconocimiento de voz; {e}"

            self.text_signal.emit(text)
