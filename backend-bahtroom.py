from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
import json
import datetime
import requests

from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)
db = client["Bathroom"]
menu_collection = db['Record']


class Bathroom(BaseModel):
    number: int
    available: int


@app.post("/bathroom/new-entry")
def add_bathroom(bathroom: Bathroom):
    bathroom_dict = {'number': bathroom.number, 'available': bathroom.available,
                     'start_time': f'{datetime.datetime.now()}', 'end_time': None}
    b = json.dumps(bathroom_dict)
    print(b)
    menu_collection.insert_one(b)


@app.get("/bathroom/get-record")
def get_bathroom():
    estimate_t = estimate_time()
    room = menu_collection.find({}, {"_id": 0, "number": 1, "available": 1, "start_time": 1, "end_time": 0})
    return {"estimatedTime": estimate_t,
            "room": room
            }


def estimate_time():
    return 0
