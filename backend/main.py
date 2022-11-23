from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analysis.transform import transformation
from pathlib import Path
# from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles

app = FastAPI()

class MyStatics(StaticFiles):

    def is_not_modified(
            self, response_headers, request_headers
    ) -> bool:
        # your own cache rules goes here...
        return False

app.mount("/img", MyStatics(directory="./analysis/img"), name="static")

origins = [
    "*"
    # "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# オーディオファイルを受け取って処理はするが，描画処理はバックグラウンドで
@app.post("/uploadfile/")
async def upload_file(upload_file: UploadFile = File(...)):
    if upload_file:
        filename = upload_file.filename
        fileobj = upload_file.file
        note_prob = transformation(fileobj)
        return note_prob
    return {"Error": "アップロードファイルが見つかりません"}
