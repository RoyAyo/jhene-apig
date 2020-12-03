from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import os

from utils.logic import Logic

class Messages(BaseModel):
    message : str
    from_context : str
    answers : dict

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/send_message")
def send_message(data:Messages):
    return data

if __name__ == "__main__":
	logic = Logic()