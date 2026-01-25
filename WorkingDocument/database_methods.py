import sqlite3

class DatabaseMethods:
    def __init__(self):
        self.connection=sqlite3.connect("task6.db")

    #will be called at the start, connects to/makes the database and its tables
    def setup(self):
        cursor=self.connection.cursor()

        #table to store users, if anyone knows anything about password security stuff we could do that instead of storing plaintext
        #also, usertype enum is short for travellers, admins, maintainers as said in the spec
        cursor.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, userName TEXT, password TEXT,userType TEXT CHECK(userType in ('T','A','M')), points INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS missions(missionID INTEGER PRIMARY KEY, question TEXT, answer TEXT)") #will change missions depending on how we deal with representing/storing routes
        cursor.execute("CREATE TABLE IF NOT EXISTS changes(changeID INTEGER PRIMARY KEY, userID INTEGER, missionID INTEGER, time TEXT, FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(missionID) REFERENCES missions(missionID))")
        cursor.execute("CREATE TABLE IF NOT EXISTS nodes(nodeID INTEGER PRIMARY KEY, coordinatesX INTEGER, coordinatesY INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS locations(locationID INTEGER PRIMARY KEY, name TEXT, nodeID INTEGER, type TEXT, FOREIGN KEY(nodeID) REFERENCES nodes(nodeID))") #type will be used if we want to display locations with icons on the map e.g station type with a small train image etc...
        cursor.execute("CREATE TABLE IF NOT EXISTS edges(edgeID INTEGER PRIMARY KEY, startNode INTEGER, endNode INTEGER, length INTEGER, lighting INTEGER, FOREIGN KEY(startNode) REFERENCES nodes(nodeID), FOREIGN KEY(endNode) REFERENCES nodes(nodeID))")#other indicators will be added here depending on what we decide on

        return()

    def addUser(self,username,password,usertype):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO users (userID,userName,password,userType) VALUES (?,?,?,?)",(None, username, password, usertype))
