import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AuthSystem import *
from DatabaseInterface import *
from typing import List

app = FastAPI()
db = DatabaseInterface()

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


class RideFormData(BaseModel):
    orig: str
    dest: str
    time: str
    days: List[int]
    seats_offered: int


@app.post('/login')
async def login(login_form_data: LoginFormData):
    user = authenticateUser(
        login_form_data.email, login_form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post('/register')
async def login(register_form_data: RegisterFormData):

    register = registerUser(register_form_data.email, register_form_data.password, register_form_data.name,
                            register_form_data.gender, register_form_data.course, register_form_data.neighbourhood)
    if register == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Register failed. Email already in use")
    else:
        return {
            "email": register_form_data.email,
        }
    
@app.get('/get_rides')
async def login():
    rides=db.get_all_rides()
    return rides

@app.post('/add_ride')
async def login(rfd: RideFormData):
    rides=db.add_ride(0,rfd.orig,rfd.dest,rfd.time,rfd.days,rfd.seats_offered);
    return rides

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level='info')
