class User:
    def __init__(self, email, password, name, gender, course, neighborhood):
        self.email = email # email
        self.password = password
        self.name = name
        self.gender = gender
        self.course = course
        self.neighborhood = neighborhood

class Companions:
    def __init__(self, name, gender, course, neighborhood, counter):
        self.name = name
        self.gender = gender
        self.course = course
        self.neighborhood = neighborhood
        self.counter = counter
        
class Ride:
    def __init__(self, ride_id, driver_id, orig, dest, time, days, seats_offered, anouncements='', chat_channel='', tags=[]):
        self.ride_id = ride_id
        self.driver_id = driver_id # id / email
        self.orig = orig # bairro
        self.dest = dest # campus
        self.time = time # hours
        self.days = days # list[bool] len = 5
        self.seats_offered = seats_offered
        self.anouncements = anouncements
        self.chat_channel = chat_channel # grupo do whatsapp
        self.tags=tags
        
class Tag:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

class Request:
    def __init__(self, request_id, ride_id, driver_id, rider_id, message=''):
        self. request_id = request_id
        self.ride_id = ride_id
        self.driver_id = ride_id
        self.rider_id = rider_id
        self.message = message