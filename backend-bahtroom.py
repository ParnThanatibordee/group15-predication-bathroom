from fastapi import FastAPI, Query, HTTPException
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
    #start_time: str  # iso datetime format: 2020-07-10 15:00:00.000
    #end_time: str

# @app.put("/bathroom/update/{num}")
# def update(num: str):
#     lst=[]
#     for i in menu_collection.find({"number": num},{"end_time": None}):
#         lst.append(i)
#         break

#     if(len(lst) > 0):
#         pass
#     else:
#         raise HTTPException(404, f"This room is not used")

@app.put("/bathroom/update/")
def update(bathroom: Bathroom):
    query = {"number": bathroom.number, "start_time": bathroom.start_time}
    if(len(query) > 0):
        new = { "$set": {"end_time": "out"}}
        menu_collection.update_one(query, new)
        return "Update completed."
    else:
        raise HTTPException(404, f"This room is not used")

#uvicorn backend-bahtroom:app --reload
