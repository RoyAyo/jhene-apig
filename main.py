from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import os
import uvicorn

from utils.logic import Logic

class Messages(BaseModel):
    message : str
    from_context : str
    more_info : bool
    answers : dict
    location : str

app = FastAPI()
logic = Logic()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jhene.co","https://*.jhene.co","https://www.jhene.co"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return "Hello World2"

@app.post("/send_message")
def send_message(data:Messages):
    try:
        message = logic.get_response(data)
        return message
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail={"message":"Unable to process data","success":False})


@app.get('/business')
def business():
    return {"I":"Dey"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
