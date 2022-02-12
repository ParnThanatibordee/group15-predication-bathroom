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

menu_collection = db['Record']
estimate_collection = db['estimate']


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
    new_values = {"$set": {"estimate": estimate}}
    estimate_collection.update_one({}, new_values)
    return estimate


@app.post("/bathroom/update/")
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