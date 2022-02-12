from ast import Return
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
import json
import datetime

from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)
db = client["Bathroom"]
estimate_collection = db['estimate']

menu_collection = db['Record']


class Bathroom(BaseModel):
    number: int
    available: int


@app.post("/bathroom/new-entry")
def add_bathroom(bathroom: Bathroom):
    bathroom_dict = {'number': bathroom.number, 'available': bathroom.available,
                     'start_time': f'{datetime.datetime.now()}', 'end_time': None}
    menu_collection.insert_one(bathroom_dict)


@app.get("/bathroom/get-record")
def get_bathroom():
    estimate_t = estimate_time()
    room = menu_collection.find({})
    result = []
    print(room)
    for r in room:
        result.append({'number': r['number'], 'available': r['available'], 'start_time': r['start_time']})
        print(r)
    return {"estimatedTime": estimate_t,
            "room": result
             }


@app.put("/bathroom/estimate")
def estimate_time():
    result = estimate_collection.find_one()
    estimate = result["sum_time"]/result["sum_used"]
    new_values = { "$set": {"estimate": estimate}}
    estimate_collection.update_one({}, new_values)
    return estimate
