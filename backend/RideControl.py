import DatabaseInterface
from DataStructures import *
from typing import List

db = DatabaseInterface()

def add_ride(driver: User, orig: str, dest: str, time: str, days=[0,0,0,0,0], seats_offered=0, anouncements='', chat_channel='', tags=[]):
    db.add_ride(driver.email, orig, dest, time, days, seats_offered, anouncements, chat_channel, tags)

def get_all_rides():
    return db.get_all_rides()

def get_user_rides(user: User):
    return db.get_rides_from_user(user.email)

def add_rider_to_ride(ride: Ride, email: str):
    if len(db.get_user_in_ride(ride.ride_id)) < ride.seats_offered:
        db.add_user_to_ride(ride.ride_id, email)

def remove_rider_from_ride(ride: Ride, email: str):
    db.remove_user_from_ride(ride.ride_id, email)

def add_ride_tags(ride: Ride, tags: List[Tag]):
    for t in tags:
        if t not in ride.tags:
            db.add_tag_to_ride(ride.ride_id, t.tag_id)
            ride.tags.append(t)
    return ride

def remove_ride_tags(ride: Ride, tags: List[Tag]):
    for t in tags:
        if t in ride.tags:
            db.remove_tag_from_ride(ride.ride_id, t.tag_id)
            ride.tags.remove(t)
    return ride