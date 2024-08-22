from PyQt6.QtCore import pyqtSignal, QObject
from src.LLM.base_messages import messages
from threading import Thread
import ollama

class Llama(QObject):

    response_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.set_messages()

    def set_messages(self):
        with open("src/LLM/base.txt", "r") as f:
            self.messages = messages

    def add_message(self, message, role="user"):
        self.messages.append({"role": role, "content": message})

    def llama_thread(self, message):
        connection_thread = Thread(target=self.llama, args=(message,), daemon=True)
        connection_thread.start()

    def llama(self, message):
        self.add_message(message)
        response = ollama.chat(model="llama3", messages=self.messages)
        self.response_signal.emit(response["message"]["content"])
        self.add_message(response["message"]["content"], role="assistant")
