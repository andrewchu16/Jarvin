from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

conversation = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
def receive_transcript(item: dict):
    text = item.get("text")
    conversation.append(["User", text])
    
    response = "Jarvin says hi"
    conversation.append(["Jarvin", response])
    
    print(text)
    return { "text": response, 
            "promptUserAgain": False }
    

# check database status

# run tests

# read slack

# rebuild project

# manage pull requests