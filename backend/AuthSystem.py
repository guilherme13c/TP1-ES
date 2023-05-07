from passlib.context import CryptContext
from DatabaseInterface import *
from DataStructures import User

db = DatabaseInterface()


def verifyUser(email: str, password: str):

    user = db.get_user(email)
    if user:
        if user.password == password:
            return user
        return False
    else:
        return None


def registerUser(email: str, password: str, name: str, gender: str, course: str, neighborhood: str):
    if db.get_user(email):
        # email already registered
        return
    db.add_user(email, password, name, gender, course, neighborhood)
