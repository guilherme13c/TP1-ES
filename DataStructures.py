class User:
    def __init__(self, user_id='', login='', password='', name='', gender='', course=''):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.name = name
        self.gender = gender
        self.course = course
        
class Ride:
    def __init__(self, ride_id='', driver='', schedule='', anouncements='', chat_channel='', seats_offered=0):
        self.ride_id = ride_id
        self.driver = driver
        self.schedule = schedule
        self.anouncements = anouncements
        self.chat_channel = chat_channel
        self.seats_offered = seats_offered
        
class Tag:
    def __init__(self, tag_id='', description=''):
        self.tag_id = tag_id
        self.description = description
