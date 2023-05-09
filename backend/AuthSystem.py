from DatabaseInterface import *
from DataStructures import User
from typing import Optional
from jwt import decode, exceptions, encode, ExpiredSignatureError, DecodeError
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials
from datetime import timedelta, datetime
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext


SECRET_KEY = "774c9e4e5419453a6ba6c3fcb43e128c5566a4c1a4c17bdff53390b7b1cbbb91"
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


def registerUser(email: str, password: str, name: str, gender: str, course: str, neighbourhood: str):
    if db.get_user(email):
        # email already registered
        return None
    db.add_user(email, pwd_context.hash(password),
                name, gender, course, neighbourhood)
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


async def get_current_user(token: str = Depends(oauth2_scheme)):
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

def verify_jwt(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except DecodeError:
        raise HTTPException(status_code=401, detail='Invalid token')
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired token')
    except Exception as e:
        raise HTTPException(status_code=401, detail='Could not validate credentials')
