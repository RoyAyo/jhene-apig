from fastapi import FastAPI
from pydantic import BaseModel

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