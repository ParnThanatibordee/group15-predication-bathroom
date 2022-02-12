from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
import datetime

from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)
db = client["Bathroom"]
menu_collection = db['Record']

# แค่สมมติ
status1 = True
status2 = True
status3 = False


class Bathroom(BaseModel):
    number: str
    available: bool
    start_time: str  # iso datetime format: 2020-07-10 15:00:00.000
    end_time: str


@app.post("/bathroom/new-bathroom")
def add_bathroom(bathroom: Bathroom):
    b = jsonable_encoder(bathroom)
    print(b)
    menu_collection.insert_one(b)
