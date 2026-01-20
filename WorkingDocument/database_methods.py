import sqlite3

class DatabaseMethods:
    def __init__(self):
        self.connection=sqlite3.connect("task6.db")

    #will be called at the start, connects to/makes the database and its tables
    def setup(self):
        cursor=self.connection.cursor()

        #table to store users, if anyone knows anything about password security stuff we could do that instead of storing plaintext
        #also, usertype enum is short for travellers, admins, maintainers as said in the spec
        cursor.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, userName TEXT, password TEXT,userType TEXT CHECK(userType in ('T','A','M')))")

        #could create all the other tables (node, mission etc)in here too if we want them all in one .db

        return()

    def addUser(self,username,password,usertype):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO users (userID,userName,password,userType) VALUES (?,?,?,?)",(None, username, password, usertype))
        

a=DatabaseMethods()
a.setup()
a.addUser("john_database","password123","T")