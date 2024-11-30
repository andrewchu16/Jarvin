from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server import Server

app = FastAPI()
server = Server()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
def receive_transcript(item: dict):
    text = item["text"]
    
    response = server.process_text(text)
    
    return response