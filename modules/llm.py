from PyQt6.QtCore import pyqtSignal, QObject
from src.LLM.base_messages import messages
from threading import Thread

from llama_index.llms.ollama import Ollama
from llama_index.core import (VectorStoreIndex, SimpleDirectoryReader,
                              StorageContext, load_index_from_storage)
from llama_index.core.agent import ReActAgent
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_parse import LlamaParse
from prompts import context
from function_tools import place_query
import os

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
        return response["message"]["content"]
