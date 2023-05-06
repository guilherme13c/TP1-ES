from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:3000",
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
async def root():
    return {"message": "Hello, World!"}

@app.post('/login')
async def login():
    
    # TODO: implement logic to verify if user exists
    
    return {
        "valid": True, 
        }
    
if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level='info')
