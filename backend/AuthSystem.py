from DatabaseInterface import *
from DataStructures import User
from typing import Optional
from jwt import decode, exceptions, encode
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext


SECRET_KEY = "unsafe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

db = DatabaseInterface()


def authenticateUser(email: str, password: str):

    user = db.get_user(email)
    if user:
        if pwd_context.verify(password, user.password):
            return user
        return False
    else:
        return None


def registerUser(email: str, password: str, name: str, gender: str, course: str, neighborhood: str):
    if db.get_user(email):
        # email already registered
        return None
    db.add_user(email, pwd_context.hash(password),
                name, gender, course, neighborhood)
    return True


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid authentication credentials")
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials")
    user = db.get_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {"email": user.email}
