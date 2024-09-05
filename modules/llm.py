from PyQt6.QtCore import pyqtSignal, QObject
from src.LLM.base_messages import messages, base_context
from threading import Thread

from llama_index.llms.ollama import Ollama
from llama_index.core import (VectorStoreIndex, SimpleDirectoryReader,
                              StorageContext, load_index_from_storage)
from llama_index.core.agent import ReActAgent
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_parse import LlamaParse
from src.LLM.function_tools import place_query

import os

from dotenv import load_dotenv
load_dotenv(dotenv_path="./src/LLM/.env")

PERSIST_DIR = "./src/LLM/storage/"

class Llama(QObject):

    response_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.set_messages()

        self.llm = Ollama(model='gemma2', request_timeout=60.0)
        self.embed_model = resolve_embed_model('local:jinaai/jina-embeddings-v2-base-es')
        self.parser = LlamaParse(result_type='markdown')
        self.file_extractor = {'.pdf': self.parser}
        self.data_list = ["practica", "data"]
        self.data_docs = {}
        self.data_indexes = {}

        self.store_data()
        self.create_engines()

        self.agent = ReActAgent.from_tools(self.query_engine_tools + [self.query_engine_sub_tool, self.place_tool],
                                    llm=self.llm,
                                    verbose=True,
                                    context=base_context,
                                    max_iterations=20,
                                    )
           
        # file = open("out.json", 'w')
        # print(self.agent.get_prompts(), file=file)
        # file.close()


    def store_data(self):
        for name in self.data_list:
            if not os.listdir(PERSIST_DIR + name):
                # print("No existe :(")
                self.data_docs[name] = SimpleDirectoryReader(
                    input_files=[os.path.join("src","LLM","data", f"{name}.pdf")],
                    file_extractor=self.file_extractor
                ).load_data()
                storage_context = StorageContext.from_defaults()
                self.data_indexes[name] = VectorStoreIndex.from_documents(
                    self.data_docs[name], embed_model=self.embed_model,
                    storage_context=storage_context
                )
                storage_context.persist(persist_dir=PERSIST_DIR+name)
            else:
                # print("Existe :)")
                storage_context = StorageContext.from_defaults(
                    persist_dir=PERSIST_DIR+name,
                )
                self.data_indexes[name] = load_index_from_storage(
                    storage_context,
                    embed_model=self.embed_model
                )
    
    def create_engines(self):
        practica_engine = self.data_indexes["practica"].as_query_engine(
            similarity_top_k=3, llm=self.llm)

        data_engine = self.data_indexes["data"].as_query_engine(similarity_top_k=3, llm=self.llm)

        self.query_engine_tools = [
            QueryEngineTool(
                query_engine=practica_engine,
                metadata=ToolMetadata(
                    name="practica_1_manual",
                    description="Entrega información sobre el manual de instrucciones y especificaciones de la práctica 1")
            ),
            QueryEngineTool(
                query_engine=data_engine,
                metadata=ToolMetadata(
                    name="eventos",
                    description="Entrega información sobre fechas y precios de distintos eventos y evaluaciones")
            )
        ]

        self.place_tool = FunctionTool.from_defaults(
            fn=place_query,
            name="place_query",
            description="Consulta las coordenadas (ubicación) de un lugar de la universidad."
        )

        query_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=self.query_engine_tools,
            llm=self.llm
        )

        self.query_engine_sub_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="sub_question_query_engine",
                description="Useful for when you want to answer more than ome question, or a compound question."
            )
        )


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
        response = self.agent.chat(message)
        self.response_signal.emit(str(response))
        self.add_message(str(response), role="assistant")

        return str(response)