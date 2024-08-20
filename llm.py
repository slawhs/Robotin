from PyQt6.QtCore import pyqtSignal, QObject
from threading import Thread
import ollama

class Llama(QObject):

    response_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def llama_thread(self, message):
        connection_thread = Thread(target=self.llama, args=(message,), daemon=True)
        connection_thread.start()

    def llama(self, message):
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": message,
                },
            ],
        )
        self.response_signal.emit(response["message"]["content"])