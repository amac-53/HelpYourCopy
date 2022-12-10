from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from starlette.staticfiles import StaticFiles
from analysis.split_file import split_file
from analysis.main import judge_code
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = './uploads'
# class MyStatics(StaticFiles):

#     def is_not_modified(
#             self, response_headers, request_headers
#     ) -> bool:
#         # your own cache rules goes here...
#         return False

# app.mount("/img", MyStatics(directory="./analysis/img"), name="static")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/uploadfile/")
async def upload_file(upload_file: UploadFile = File(...)):
    """
    音声ファイルを受け取って，分析結果を返す
    """
    if upload_file:
        filename = upload_file.filename
        fileobj = upload_file.file
        
        # 一旦一時ファイルを保存
        # https://qiita.com/XPT60/items/1ae2bb99e81bd8c8bc98
        upload_dir = open(os.path.join(UPLOAD_FOLDER, filename),'wb+')
        shutil.copyfileobj(fileobj, upload_dir)
        upload_dir.close()

        # ファイルをstemに分割
        n_stem = 5
        split_file(n_stem, filename)


        # コード解析
        ans = judge_code(n_stem, filename)
        
        return ans
    return {"Error": "アップロードファイルが見つかりません"}


@app.get("/detail/chromagram/")
async def get_chromagram(instrument: str = ''):
    """
    指定した楽器のchromagramを返す
    """
    # 音がなっていないと判定されれば，存在しないことをreturn
    file_path = './analysis/img/chromagram_'+str(instrument)+'.png'
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return 'None'


@app.get("/detail/spectrum/")
async def get_spectrum(instrument: str = ''):
    """
    指定した楽器のspectrumを返す
    """
    # 音がなっていないと判定されれば，存在しないことをreturn
    file_path = './analysis/img/spectrum_'+str(instrument)+'.png'
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return 'None'
