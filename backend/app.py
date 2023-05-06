from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3000/login",
    "http://localhost:3000/register",
    " http://192.168.1.121:3000/"
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoginResponse(BaseModel):
    authorize: bool

@app.get('/')
async def root():
    return {"message": "Hello, World!"}

@app.get('/login', status_code=200)
async def login():
    return {
        "valid": True, 
        }
