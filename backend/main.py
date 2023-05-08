import uvicorn
from fastapi import FastAPI, HTTPException
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


class RegisterFormData(BaseModel):
    email: str
    password: str
    name: str
    gender: str
    course: str
    neighbourhood: str


@app.post('/login')
async def login(login_form_data: LoginFormData):
    verification = verifyUser(login_form_data.email, login_form_data.password)
    if not verification:
        raise HTTPException(400, "Incorrect credentials")

    return {
        "access_token": login_form_data.email,
    }


@app.post('/register')
async def login(register_form_data: RegisterFormData):

    register = registerUser(register_form_data.email, register_form_data.password, register_form_data.name,
                            register_form_data.gender, register_form_data.course, register_form_data.neighbourhood)
    if register == None:
        raise HTTPException(400, "Register failed. Email already in use")
    else:
        return {
            "access_token": register_form_data.email,
        }

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level='info')
