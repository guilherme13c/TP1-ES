import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AuthSystem import *

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

class LoginFormData(BaseModel):
    email: str
    password: str

@app.post('/token')
async def login(login_form_data: LoginFormData):
    
    verification = verifyUser(login_form_data.email, login_form_data.password)
    if not verification:
        raise HTTPException(400, "Incorrect credentials")
        
    return {
        "access_token": login_form_data.username,
        "token_type": "bearer"
        }
    
if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level='info')
