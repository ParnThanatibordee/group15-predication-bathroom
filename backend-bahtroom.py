from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.encoders import jsonable_encoder
import datetime

from pymongo import MongoClient

app = FastAPI()

client = MongoClient('mongodb://localhost', 27017)
db = client["Bathroom"]
estimate_collection = db['estimate']


@app.put("/bathroom/estimate")
def estimate_time():
    result = estimate_collection.find_one()
    estimate = result["sum_time"]/result["sum_used"]
    new_values = { "$set": {"estimate": estimate}}
    estimate_collection.update_one({}, new_values)
    return estimate