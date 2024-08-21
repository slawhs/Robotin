from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
import os


class Server(FastAPI):

    def __init__(self):
        super().__init__()
        self.templates = Jinja2Templates(directory="templates")
        self.load_mounts()
        self.set_rutes()

    def load_mounts(self):
        self.mount("/static", StaticFiles(directory="static"), name="static")
        self.mount("/src/images", StaticFiles(directory="src/images"), name="images")

    def set_rutes(self):
        @self.get('/', response_class=HTMLResponse)
        def home(request: Request):
            return app.templates.TemplateResponse(
                "index.html", {
                    "request": request,
                    "show": self.images}
                )

        @self.post("/", response_class=HTMLResponse)
        async def delete(request: Request):
            data = self.body_to_dict(await request.body())
            name = data["name"].replace("+", " ")
            if os.path.exists(f"src/images/{name}"): os.remove(f"src/images/{name}")
            return self.templates.TemplateResponse(
                "index.html", {
                    "request": request,
                    "show": self.images
                })

        @self.post("/upload-files")
        async def create_upload_files(request: Request, files: List[UploadFile] = File(...)):
            for file in files:
                contents = await file.read()
                with open(f"src/images/{file.filename}", "wb") as f:
                    f.write(contents)

            return self.templates.TemplateResponse(
                "index.html", {
                    "request": request,
                    "show": self.images
                })

    @property
    def images(self):
        return list(filter(
            lambda x: x.endswith(".jpg") or x.endswith(".png"),
            [name for name in os.listdir("src/images")]
        ))

    def body_to_dict(self, body: bytes):
        data = {}
        for n in body.decode().split("&"):
            key, value = n.split("=")
            data[key] = value
        return data

app = Server()
