from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analysis.transform import transformation
from pathlib import Path
# from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
import requests, json

app = FastAPI()

@app.get('/')
async def tmp():
    url = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    API_KEY = '296aec41c1f8b322'
    lat = '34.910047'
    lng = '135.7805467'
    range = '1'
    r = requests.get(url + '?key=' + API_KEY + '&lat=' + lat + '&lng=' + lng + '&range=' + range)
    return  {'res': r.text}