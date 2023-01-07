from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from analysis.split_file import split_file
import analysis.main_for_solo as total_judge
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = './uploads'

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


@app.post("/uploadfile")
async def upload_file(upload_file: UploadFile = File(...), objective: str = 'solo'):
    """
    音声ファイルを受け取って，分析結果を返す
    """
    if upload_file:

        filename = upload_file.filename
        fileobj = upload_file.file

        # 一時ファイルを保存
        # https://qiita.com/XPT60/items/1ae2bb99e81bd8c8bc98
        upload_dir = open(os.path.join(UPLOAD_FOLDER, filename),'wb+')
        shutil.copyfileobj(fileobj, upload_dir)
        upload_dir.close()

        # すでに分割済みでなければ，ファイル分割
        if objective == 'vocals':
            n_stem = 2
        elif objective == 'drums' or objective == 'bass':
            n_stem = 5
        else:
            n_stem = 5
        
        dir_path = './outputs/' + str(n_stem) + '/' + filename[:-4]
        if os.path.isdir(dir_path) == False:
            split_file(n_stem, filename)
        
        # 目的により処理を変える
        if objective == 'solo':
            ans = total_judge.judge_code(n_stem, filename)
        elif objective == 'bass':
            ans = 'bass'
        elif objective == 'drums':
            ans = 'drum'
            file_path = './outputs/'+str(n_stem)+'/'+str(filename[:-4])+'/'+ objective +'.wav'
            return FileResponse(file_path)
        elif objective == 'other':
            ans = 'guitar'
        elif objective == 'piano':
            ans = 'piano'
        else:
            ans = 'vocals'

        return ans
    return {"Error": "アップロードファイルが見つかりません"}


@app.get("/detail/split_file")
async def get_split_file(objective: str = '', filename: str = ''):
    """
    分割されたオーディオファイルを返す
    """
    # 全stemで分割ファイルが存在するか確認
    for n_stem in [2, 4, 5]:
        print(filename)
        file_path = './outputs/'+str(n_stem)+'/'+str(filename[:-4])+'/'+ objective +'.wav'
        print(file_path)
        if os.path.isfile(file_path):
            print(file_path)
            return FileResponse(file_path)
    return 'None'


@app.get("/detail/chromagram")
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


@app.get("/detail/spectrum")
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
