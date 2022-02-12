from fastapi import FastAPI, Query, HTTPException
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
estimate_collection = db['estimate']


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


@app.put("/bathroom/update/")
def update(bathroom: Bathroom):
    num = bathroom.number
    chk = bathroom.available
    if 1 <= num <= 3:
        res = menu_collection.find_one({"number": num}, {"_id": 0})
        query = {"number": num}
        if chk:
            if not res["available"]:
                new = {"$set": {"available": True,
                                "end_time": f'{datetime.datetime.now()}'}}
                menu_collection.update_one(query, new)

                start = datetime.datetime.strptime(res["start_time"], '%Y-%m-%d %H:%M:%S.%f')
                stop = datetime.datetime.strptime(res["start_time"], '%Y-%m-%d %H:%M:%S.%f')
                dur = stop - start

                res2 = estimate_collection.find_one()
                new_sum_time = {"$set": {"sum_time": res2["sum_time"] + dur.total_seconds()}}
                new_sum_used = {"$set": {"sum_use": res2["sum_used"] + 1}}
                estimate_collection.update_one({}, new_sum_time)
                estimate_collection.update_one({}, new_sum_used)
        else:
            if res["available"]:
                new = {"$set": {"available": False,
                                'start_time': f'{datetime.datetime.now()}',
                                'end_time': None}}
                menu_collection.update_one(query, new)
        return res
    else:
        raise HTTPException(404, "Update failed.")
