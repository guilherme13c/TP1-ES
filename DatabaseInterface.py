import sqlite3
from DataStructures import all

class DatabaseInterface:
    __instance = None
    
    def __commit(self):
        self.conn.commit()
    
    def __init__(self):
        
        # check for instances
        if DatabaseInterface.__instance != None:
            return DatabaseInterface.__instance
        
        # create connection and cursor
        self.conn = sqlite3.connect('faculride.db')
        self.c = self.conn.cursor()

        # create users table
        self.c.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id TEXT PRIMARY KEY,
                      login TEXT,
                      password TEXT,
                      name TEXT,
                      gender TEXT,
                      course TEXT)''')

        # create companions table
        self.c.execute('''CREATE TABLE IF NOT EXISTS companions
                     (user_1 TEXT,
                      user_2 TEXT,
                      counter INTEGER)''')

        # create rides table
        self.c.execute('''CREATE TABLE IF NOT EXISTS rides
                     (ride_id TEXT PRIMARY KEY,
                      driver TEXT,
                      schedule TEXT,
                      anouncements TEXT,
                      chat_channel TEXT,
                      seats_offered INTEGER)''')

        # create user_rides table
        self.c.execute('''CREATE TABLE IF NOT EXISTS user_rides
                     (user TEXT,
                      ride TEXT)''')

        # create tags table
        self.c.execute('''CREATE TABLE IF NOT EXISTS tags
                     (tag_id TEXT PRIMARY KEY,
                      description TEXT)''')

        # create ride_tags table
        self.c.execute('''CREATE TABLE IF NOT EXISTS ride_tags
                     (ride TEXT,
                      tag TEXT)''')
        
        # set instance
        __instance = self
        
        self.__commit()
    
    #### Adding data to database ####
    
    def add_user(self, user):
        new_user = (user.user_id, user.login, user.password, user.name, user.gender, user.course)
        self.c.execute("INSERT INTO users (user_id, login, password, name, gender, course) VALUES (?, ?, ?)", new_user)
        self.__commit()
    
    def add_ride(self, ride):
        new_ride = (ride.ride_id, ride.driver, ride.schedule, ride.anouncements, ride.chat_channel, ride.seats_offered)
        self.c.execute("INSERT INTO rides (ride_id, driver, schedule, anouncements, chat_channel, seats_offered) VALUES (?, ?, ?)", new_ride)
        self.__commit()
        
    def add_tag(self, tag):
        new_tag = (user.tag_id, user.description)
        self.c.execute("INSERT INTO tags (tag_id, description) VALUES (?, ?, ?)", new_tag)
        self.__commit()
        
    def __count_new_companions__(self, new_user, ride):
        
        # add each user already in ride to companions
        c.execute("SELECT user FROM user_rides WHERE ride=?", (ride.ride_id))
        companions = c.fetchall()
        for old_user in companions:
            
            # first entry must be the lowest
            if new_user[0] < old_user[0]:
                id_1, id_2 = new_user[0], old_user[0]
            else:
                id_1, id_2 = old_user[0],  new_user[0]
            
            # check if entry exist
            c.execute("SELECT counter FROM companions WHERE user_1=? AND user_2=?", (id_1, id_2))
            entry = c.fetchone()

            # if entry do not exist, create one
            if entry is not None:
                self.c.execute("INSERT INTO companions (user_1, user_2, counter) VALUES (?, ?, ?)", (id_1, id_2, 1))
            # if entry exist, add 1 to counter
            else:
                self.c.execute("UPDATE companions SET counter = ? WHERE user_1=? AND user_2=?", (entry[0]+1, user_1, user_2))
    
    def add_user_to_ride(self, user, ride):
        self.__count_new_passager(user, ride)
        new_passager = (user.user_id, ride.ride_id)
        self.c.execute("INSERT INTO users (tag_id, description) VALUES (?, ?, ?)", new_passager)
        self.__commit()
    
    def add_tag_to_ride(self, tag, ride):
        new_tagged = (ride.ride_id, tag.tag_id)
        c.execute("INSERT INTO ride_tags (ride, tag) VALUES (?, ?)", new_tagged)
        self.__commit()
    
    
    #### Get data from database ####
    
    
    def get_users(self):
        self.c.execute("SELECT user_id, login, password, name, gender, course FROM users")
        query = self.c.fetchall()
        return [User(*q) for q in query]
    
    def get_user(self, user):
        self.c.execute("SELECT user_id, login, password, name, gender, course FROM users WHERE user_id=?", user.user_id)
        query = self.c.fetchall()
        return User(*query)
    
    def get_companions(self, user):
        self.c.execute("SELECT user_2 FROM companions WHERE user_1=?", user.user_id)
        q1 = self.c.fetchall()
        l1 = [User(*q) for q in q1]
        self.c.execute("SELECT user_1 FROM companions WHERE user_2=?", user.user_id)
        q2 = self.c.fetchall()
        l2 = [User(*q) for q in q2]
        return l1+l2
    
    def get_rides(self, tags, ALL=True):
        query = """
            SELECT rides.ride_id, driver, schedule, anouncements, chat_channel, seats_offered, GROUP_CONCAT(tags.tag_id) AS tags
            FROM rides
            LEFT JOIN ride_tags ON rides.ride_id = ride_tags.ride
            LEFT JOIN tags ON ride_tags.tag = tags.tag_id
            WHERE tags.tag_id IN ({})
            GROUP BY rides.ride_id
            HAVING COUNT(*) >= {}
            ORDER BY COUNT(*) DESC;
        """.format(",".join(["?"]*len(tags)), len(tags) if ALL else 1)
        self.c.execute(query, tags*2 if ALL else tags)
        query = self.c.fetchall()
        return [Ride(*q[:6], q[6].split(',')) for q in query]
    
    def get_ride(self, ride):
        self.c.execute("SELECT ride_id, driver, schedule, anouncements, chat_channel, seats_offered FROM rides WHERE ride_id = ?", ride.ride_id,)
        query = self.c.fetchall()
        return User(*query)
    
    def get_rides_from_user(self, user):
        query = """
            SELECT rides.ride_id, driver, schedule, anouncements, chat_channel, seats_offered
            FROM rides
            LEFT JOIN user_rides ON rides.ride_id = user_rides.ride
            WHERE user_rides.user=?
        """
        self.c.execute(query, user.user_id)
        query = self.c.fetchall()
        return [Ride(*q) for q in query]
    
    
    def get_users_in_ride(self, ride):
        query = """
            SELECT rides.ride_id, driver, schedule, anouncements, chat_channel, seats_offered, GROUP_CONCAT(tags.tag_id) AS tags
            FROM users
            LEFT JOIN user_rides ON user.user_id = user_rides.user            LEFT JOIN tags ON ride_tags.tag = tags.tag_id
            WHERE user_rides.ride=?
        """
        self.c.execute(query, tags*2 if ALL else tags)
        query = self.c.fetchall()
        return [User(*q) for q in query]
    
    
    def get_tags(self):
        self.c.execute("SELECT tag_id, description FROM tags")
        query = self.c.fetchall()
        return [User(*q) for q in query]
        
        
    #### Alter data from database ####
    
    
    def update_user_data(self, user):
        new_data = (user.login, user.password, user.name, user.gender, user.course, user.user_id)
        self.c.execute("UPDATE companions SET login=?, password=?, name=?, gender=?, course=?  WHERE user_id=?", new_data)
        self.__commit()
    
    def update_ride_data(self, ride):
        new_data = (ride.driver, ride.schedule, ride.anouncements, ride.chat_channel, ride.seats_offered, ride.ride_id)
        self.c.execute("UPDATE companions SET driver=?, schedule=?, anouncements=?, chat_channel=?, seats_offered=?  WHERE ride_id=?", new_data)
        self.__commit()
    
    def update_tag_data(self, tag):
        new_data = (tag.description, tag.tag_id)
        self.c.execute("UPDATE companions SET description=?  WHERE tag_id=?", new_data)
        self.__commit()
        
        
    #### Delete data from database ####
    
    
    def __delete_from_companions(self, user_id):
        self.c.execute("DELETE FROM companions WHERE user_1=?", (user_id,))
        self.c.execute("DELETE FROM companions WHERE user_2=?", (user_id,))
    
    def delete_user(self, user_id):
        self.c.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.__commit()
    
    def delete_ride(self, ride_id):
        self.c.execute("DELETE FROM rides WHERE ride_id=?", (ride_id,))
        self.__commit()
    
    def delete_tag(self, tag_id):
        self.c.execute("DELETE FROM tags WHERE tag_id=?", (tag_id,))
        self.__commit()
    
    def remove_user_from_ride(self, user_id, ride_id):
        self.c.execute("DELETE FROM user_rides WHERE user=? AND ride=?", (user_id, ride_id))
        self.__commit()
    
    def remove_tag_from_ride(self, tag_id, ride_id):
        self.c.execute("DELETE FROM ride_tags WHERE tag=? AND ride=?", (tag_id, ride_id))
        self.__commit()
        
    def __del__(self):
        # commit changes and close connection
        self.__commit()
        self.conn.close()