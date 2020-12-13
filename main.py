from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import os
import uvicorn

from utils.logic import Logic

class Messages(BaseModel):
    message : str
    from_context : str

app = FastAPI()
logic = Logic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/send_message")
def send_message(data:Messages):
    message = logic.get_response(data)
    print(message)
    return message

@app.get('/business')
def business():
    return {"I":"Dey"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")