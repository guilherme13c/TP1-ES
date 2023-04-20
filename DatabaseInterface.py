import sqlite3

class DatabaseInterface:
    __instance = None

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

        # create ride table
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
        instance = self

    def add_user(self, user):
        new_user = (user.user_id, user.login, user.password, user.name, user.gender, user.course)
        self.c.execute("INSERT INTO users (user_id, login, password, name, gender, course) VALUES (?, ?, ?)", new_user)

    def add_ride(self, ride):
        new_ride = (ride.ride_id, ride.driver, ride.schedule, ride.anouncements, ride.chat_channel, ride.seats_offered)
        self.c.execute("INSERT INTO rides (ride_id, driver, schedule, anouncements, chat_channel, seats_offered) VALUES (?, ?, ?)", new_ride)

    def add_tag(self, tag):
        new_tag = (user.tag_id, user.description)
        self.c.execute("INSERT INTO tags (tag_id, description) VALUES (?, ?, ?)", new_tag)

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

    def add_tag_to_ride(self, tag, ride):
        new_tagged = (ride.ride_id, tag.tag_id)
        c.execute("INSERT INTO ride_tags (ride, tag) VALUES (?, ?)", new_tagged)

    def update_user_data(self, user):
        new_data = (user.login, user.password, user.name, user.gender, user.course, user.user_id)
        self.c.execute("UPDATE companions SET login=?, password=?, name=?, gender=?, course=?  WHERE user_id=?", new_data)

    def update_ride_data(self, ride):
        new_data = (ride.driver, ride.schedule, ride.anouncements, ride.chat_channel, ride.seats_offered, ride.ride_id)
        self.c.execute("UPDATE companions SET driver=?, schedule=?, anouncements=?, chat_channel=?, seats_offered=?  WHERE ride_id=?", new_data)

    def update_tag_data(self, tag):
        new_data = (tag.description, tag.tag_id)
        self.c.execute("UPDATE companions SET description=?  WHERE tag_id=?", new_data)

    def delete_user(self):
        pass

    def delete_ride(self):
        pass

    def delete_tag(self):
        pass

    def remove_user_from_ride(self):
        pass

    def remove_tag_from_ride(self):
        pass

    def __del__(self):
        # commit changes and close connection
        self.conn.commit()
        self.conn.close()
