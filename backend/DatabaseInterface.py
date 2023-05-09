import sqlite3
from DataStructures import *


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
        self.c.execute("""
                        CREATE TABLE IF NOT EXISTS users
                        (email TEXT PRIMARY KEY,
                        password TEXT,
                        name TEXT,
                        gender TEXT,
                        course TEXT,
                        neighbourhood TEXT)
                        """)

        # create companions table
        self.c.execute("""
                        CREATE TABLE IF NOT EXISTS companions
                        (user_1 TEXT,
                        user_2 TEXT,
                        counter INTEGER,
                        FOREIGN KEY (user_1) REFERENCES users(user_id) ON DELETE CASCADE,
                        FOREIGN KEY (user_2) REFERENCES users(user_id) ON DELETE CASCADE)
                        """)

        # create rides table
        self.c.execute("""
                        CREATE TABLE IF NOT EXISTS rides
                        (ride_id INTEGER PRIMARY KEY,
                        driver_id TEXT,
                        orig TEXT,
                        dest TEXT,
                        time TIME,
                        mon BIT,
                        thu BIT,
                        wed BIT,
                        tue BIT,
                        fri BIT,
                        seats_offered INTEGER,
                        anouncements TEXT,
                        chat_channel TEXT,
                        FOREIGN KEY (driver_id) REFERENCES users(email) ON DELETE CASCADE)
                        """)

        # create user_rides table
        self.c.execute("""
                        CREATE TABLE IF NOT EXISTS user_rides
                        (user_id TEXT,
                        ride_id TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(email) ON DELETE CASCADE,
                        FOREIGN KEY (ride_id) REFERENCES rides(ride_id) ON DELETE CASCADE)
                        """)

        # create tags table
        self.c.execute("""
                        CREATE TABLE IF NOT EXISTS tags
                        (tag_id TEXT PRIMARY KEY,
                        description TEXT)
                        """)

        # create ride_tags table
        self.c.execute("""
                        CREATE TABLE IF NOT EXISTS ride_tags
                        (ride_id TEXT,
                        tag_id TEXT,
                        FOREIGN KEY (ride_id) REFERENCES rides(ride_id) ON DELETE CASCADE,
                        FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE)
                        """)

        # creat requests table
        self.c.execute("""
                        CREATE TABLE IF NOT EXISTS requests
                        (request_id INTEGER PRIMARY KEY,
                        ride_id TEXT,
                        driver_id TEXT,
                        rider_id TEXT,
                        message TEXT,
                        FOREIGN KEY (ride_id) REFERENCES rides(ride_id) ON DELETE CASCADE,
                        FOREIGN KEY (driver_id) REFERENCES users(email) ON DELETE CASCADE,
                        FOREIGN KEY (rider_id) REFERENCES users(email) ON DELETE CASCADE)
                        """)

        # set instance
        __instance = self

        self.__commit()

    #################################
    #### Adding data to database ####
    #################################

    def add_user(self, email, password, name, gender, course, neighbourhood):
        new_entry = (email, password, name, gender, course, neighbourhood)
        self.c.execute(
            "INSERT INTO users (email, password, name, gender, course, neighbourhood) VALUES (?, ?, ?, ?, ?, ?)", new_entry)
        self.__commit()

    def update_user(self, email, name, gender, course, neighbourhood):
        new_entry = (name, gender, course, neighbourhood, email)
        self.c.execute(
            "UPDATE users SET name=?,gender=?,course=?,neighbourhood=? where email = ?", new_entry)
        self.__commit()
        return User(name, 0, name, gender, course, neighbourhood)

    def __count_new_companions(self, user_id, ride_id):

        # add each user already in ride to companions
        self.c.execute(
            "SELECT user_id FROM user_rides WHERE ride_id=?", (ride_id,))
        old_users_id = self.c.fetchall()
        for old_user in old_users_id:

            # check if entry exist
            self.c.execute("SELECT * FROM companions WHERE (user_1=? AND user_2=?) OR (user_1=? AND user_2=?)",
                           (user_id, old_user[0], old_user[0], user_id))
            entry = self.c.fetchone()

            # if entry do not exist, create one
            if entry is None:
                self.c.execute(
                    "INSERT INTO companions (user_1, user_2, counter) VALUES (?, ?, ?)", (user_id, old_user[0], 1))
            # if entry exist, add 1 to counter
            else:
                self.c.execute(
                    "UPDATE companions SET counter = ? WHERE user_1=? AND user_2=?", (entry[2]+1, entry[0], entry[1]))

    def add_user_to_ride(self, user_id, ride_id):
        self.__count_new_companions(user_id, ride_id)
        new_entry = (user_id, ride_id)
        self.c.execute(
            "INSERT INTO user_rides (user_id, ride_id) VALUES (?, ?)", new_entry)
        self.__commit()

    def add_tag(self, tag_id, description=''):
        new_entry = (tag_id, description)
        self.c.execute(
            "INSERT INTO tags (tag_id, description) VALUES (?, ?)", new_entry)
        self.__commit()

    def add_tag_to_ride(self, ride_id, tag_id):
        new_entry = (ride_id, tag_id)
        self.c.execute(
            "INSERT INTO ride_tags (ride_id, tag_id) VALUES (?, ?)", new_entry)
        self.__commit()

    def add_ride(self, driver_id, orig, dest, time, days, seats_offered, anouncements='', chat_channel='', tags=[]):
        new_entry = (driver_id, orig, dest, time,
                     days[0], days[1], days[2], days[3], days[4], seats_offered, anouncements, chat_channel)
        self.c.execute("""
                        INSERT INTO rides 
                        (driver_id, orig, dest, time, mon, thu, wed, tue, fri, seats_offered, anouncements, chat_channel)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, new_entry)
        ride_id=self.c.lastrowid;
        for t in tags:
            self.add_tag_to_ride(ride_id, t.tag_id)
        self.add_user_to_ride(driver_id, ride_id)
        self.__commit()

    def add_request(self, request_id, ride_id, driver_id, rider_id, message=''):
        new_entry = (ride_id, driver_id, rider_id, message)
        self.c.execute("""
                        INSERT INTO requests (ride_id, driver_id, rider_id, message)
                        VALUES (?, ?, ?, ?)
                        """, new_entry)
        self.__commit()

    ################################
    #### Get data from database ####
    ################################

    def get_user(self, email):
        self.c.execute("SELECT * FROM users WHERE email=?", (email,))
        query = self.c.fetchone()
        if query:
            return User(*query)
        return None

    def get_companions_from_user(self, email):
        self.c.execute("""
                        SELECT name, gender, course, neighbourhood, counter 
                        FROM users
                        LEFT JOIN companions ON email=user_1 
                        WHERE user_2=?
                        """, (email,))
        q1 = self.c.fetchall()
        l1 = [User(*q) for q in q1]
        self.c.execute("""
                        SELECT name, gender, course, neighbourhood, counter 
                        FROM users
                        LEFT JOIN companions ON email=user_2 
                        WHERE user_1=?
                        """, (email,))
        q2 = self.c.fetchall()
        l2 = [Companion(*q) for q in q2]
        return l1+l2

    def get_ride_tags(self, ride_id):
        self.c.execute("""
                        SELECT tags.tag_id, description 
                        FROM tags
                        LEFT JOIN ride_tags ON tags.tag_id=ride_tags.tag_id
                        WHERE ride_id=?
                        """, (ride_id,))
        return [Tag(*q) for q in self.c.fetchall()]

    def get_ride(self, ride_id):
        self.c.execute("SELECT * FROM rides WHERE ride_id = ?", (ride_id,))
        query = self.c.fetchone()
        if query:
            driver_id = query[1]
            orig = query[2]
            dest = query[3]
            time = query[4]
            days = query[5:10]
            seats_offered = query[10]
            anouncements = query[11]
            chat_channel = query[12]
            tags = self.get_ride_tags(ride_id)
            return Ride(ride_id, driver_id, orig, dest, time, days, seats_offered, anouncements, chat_channel, tags)
        return None

    def get_all_rides(self):
        self.c.execute("SELECT ride_id FROM rides")
        query = self.c.fetchall()
        return [self.get_ride(q[0]) for q in query]

    def get_rides_from_user(self, email):
        self.c.execute(
            "SELECT ride_id FROM user_rides WHERE user_id=?", (email,))
        query = self.c.fetchall()
        return [self.get_ride(q[0]) for q in query]

    def get_user_in_ride(self, ride_id):
        self.c.execute(
            "SELECT user_id FROM user_rides WHERE ride_id=?", (ride_id,))
        query = self.c.fetchall()
        return [self.get_user(q[0]) for q in query]

    def get_tags(self):
        self.c.execute("SELECT * FROM tags")
        query = self.c.fetchall()
        return [Tag(*q) for q in query]

    def get_user_requests(self, email):
        self.c.execute("SELECT * FROM requests WHERE driver_id=?", (email,))
        query = self.c.fetchall()
        return [Request(*q) for q in query]

    ##################################
    #### Alter data from database ####
    ##################################

    def update_user_data(self, user):
        new_data = (user.password, user.name, user.gender,
                    user.course, user.neighbourhood, user.email)
        self.c.execute(
            "UPDATE companions SET password=?, name=?, gender=?, course=?, neighbourhood=?  WHERE email=?", new_data)
        self.__commit()

    ###################################
    #### Delete data from database ####
    ###################################

    def delete_user(self, email):
        self.c.execute("DELETE FROM users WHERE email=?", (email,))
        self.__commit()

    def delete_ride(self, ride_id):
        self.c.execute("DELETE FROM rides WHERE ride_id=?", (ride_id,))
        self.__commit()

    def delete_tag(self, tag_id):
        self.c.execute("DELETE FROM tags WHERE tag_id=?", (tag_id,))
        self.__commit()

    def remove_request(self, request_id):
        self.c.execute(
            "DELETE FROM requests WHERE request_id=?", (request_id,))
        self.__commit()

    def remove_user_from_ride(self, user_id, ride_id):
        self.c.execute(
            "DELETE FROM user_rides WHERE user=? AND ride=?", (user_id, ride_id))
        self.__commit()

    def remove_tag_from_ride(self, tag_id, ride_id):
        self.c.execute(
            "DELETE FROM ride_tags WHERE tag=? AND ride=?", (tag_id, ride_id))
        self.__commit()

    def __del__(self):
        # commit changes and close connection
        self.__commit()
        self.c.close()
        self.conn.close()

    def get_all_users(self):
        self.c.execute("SELECT * FROM users")
        query = self.c.fetchall()
        return [u for u in query]


if __name__ == "__main__":
    db = DatabaseInterface()
    # db.c.execute("DELETE FROM users")
    users = db.get_all_users()
    for user in users:
        print(user)
