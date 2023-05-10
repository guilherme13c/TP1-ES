import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from AuthSystem import *
from DatabaseInterface import *
from RideControl import *
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
    days: List[bool]
    seats_offered: int
    driver_id: str


class GetUserData(BaseModel):
    email: str


class EditUserData(BaseModel):
    email: str
    name: str
    gender: str
    course: str
    neighbourhood: str


class GetRide(BaseModel):
    ride_id: str


@app.post('/login')
async def login_api(login_form_data: LoginFormData):
    user = authenticateUser(
        login_form_data.email, login_form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password")

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email
    }


@app.post('/register')
async def register_api(register_form_data: RegisterFormData):

    register = registerUser(register_form_data.email, register_form_data.password, register_form_data.name,
                            register_form_data.gender, register_form_data.course, register_form_data.neighbourhood)
    if register == None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            "Register failed. Email already in use")
    else:
        access_token = create_access_token(
            data={"sub": register_form_data.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "email": register_form_data.email
        }


@app.get('/get_rides')
async def get_rides_api(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt(credentials)
        rides = db.get_all_rides()
        return {
            "rides": rides
        }
    except HTTPException as e:
        raise e


@app.post('/add_ride')
async def add_ride_api(ride_form_data: RideFormData, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt(credentials)
        db.add_ride(ride_form_data.driver_id, ride_form_data.orig, ride_form_data.dest,
                    ride_form_data.time, ride_form_data.days, ride_form_data.seats_offered)
        return {

        }

    except HTTPException as e:
        raise e


@app.post('/get_user')
async def get_user_api(json_email: GetUserData, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt(credentials)
        user = db.get_user(json_email.email)
        return {
            "email": user.email,
            "name": user.name,
            "gender": user.gender,
            "course": user.course,
            "neighbourhood": user.neighbourhood
        }
    except HTTPException as e:
        raise e


@app.post('/edit_user')
async def edit_user_api(edit_user_data: EditUserData, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt(credentials)
        user = db.update_user(edit_user_data.email, edit_user_data.name,
                              edit_user_data.gender, edit_user_data.course, edit_user_data.neighbourhood)
        return {
            "email": user.email,
            "name": user.name,
            "gender": user.gender,
            "course": user.course,
            "neighbourhood": user.neighbourhood
        }
    except HTTPException as e:
        raise e


@app.post('/get_my_rides')
async def get_my_rides_api(json_email: GetUserData, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt(credentials)
        user = User(json_email.email, 0, 0, 0, 0, 0)
        user_rides = get_user_rides(user)
        return {
            "userData": {
                "email": json_email.email
            },
            "userRides": user_rides
        }

    except HTTPException as e:
        raise e


@app.post('/get_ride')
async def get_ride_api(json_ride_id: GetRide, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = verify_jwt(credentials)
        ride = db.get_ride(json_ride_id.ride_id)
        return {
            "ride_id": json_ride_id.ride_id,
            "orig": ride.orig,
            "dest": ride.dest,
            "time": ride.time,
            "days": ride.days,
            "seats_oferred": ride.seats_offered,
            "driver_id": ride.driver_id
        }

    except HTTPException as e:
        raise e

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level='info')
