import sqlite3

class DatabaseMethods:
    def __init__(self):
        self.connection=sqlite3.connect("task6.db")

    #will be called at the start, connects to/makes the database and its tables
    def setup(self):
        cursor=self.connection.cursor()

        #table to store users, if anyone knows anything about password security stuff we could do that instead of storing plaintext
        cursor.execute("CREATE TABLE IF NOT EXISTS nodes(nodeID INTEGER PRIMARY KEY, coordinatesX REAL, coordinatesY REAL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, userName TEXT, email TEXT, password TEXT,userType TEXT CHECK(userType in ('T','A','M')), points INTEGER)") # usertype enum is short for travellers, admins, maintainers as said in the spec
        cursor.execute("CREATE TABLE IF NOT EXISTS missions(missionID INTEGER PRIMARY KEY, question TEXT, startNode INTEGER, endNode INTEGER, FOREIGN KEY(startNode) REFERENCES nodes(nodeID), FOREIGN KEY(endNode) REFERENCES nodes(nodeID))") #will change missions depending on how we deal with representing/storing routes
        cursor.execute("CREATE TABLE IF NOT EXISTS changes(changeID INTEGER PRIMARY KEY, userID INTEGER, missionID INTEGER, time TEXT, FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(missionID) REFERENCES missions(missionID))")
        cursor.execute("CREATE TABLE IF NOT EXISTS locations(locationID INTEGER PRIMARY KEY, name TEXT, nodeID INTEGER, locationType TEXT, FOREIGN KEY(nodeID) REFERENCES nodes(nodeID))") #type will be used if we want to display locations with icons on the map e.g station type with a small train image etc...
        cursor.execute("CREATE TABLE IF NOT EXISTS edges(edgeID INTEGER PRIMARY KEY, startNode INTEGER, endNode INTEGER, length INTEGER, lighting INTEGER, FOREIGN KEY(startNode) REFERENCES nodes(nodeID), FOREIGN KEY(endNode) REFERENCES nodes(nodeID))")#other indicators will be added here depending on what we decide on

        return()

    #adder methods##################
    def addNode(self,coordinatesX,coordinatesY):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO nodes (nodeID, coordinatesX,coordinatesY) VALUES (?,?,?)",(None, coordinatesX,coordinatesY))

    def addUser(self,username, email, password,usertype):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO users (userID,userName,email,password,userType,points) VALUES (?,?,?,?,?,?)",(None, username, email,password, usertype,0))

    def addChange(self,userID,missionID,time):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO changes (changeID, userID, missionID, time) VALUES(?,?,?,?)",(None,userID,missionID,time))

    def addLocation(self,name,nodeID,locationType):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO locations (locationID,name,nodeID,locationType) VALUES(?,?,?,?)",(None,name,nodeID,locationType))

    def addEdge(self,startNode,endNode,length,lighting):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO edges(edgeID,startNode,endNode,length,lighting) VALUES(?,?,?,?,?)",(None,startNode,endNode,length,lighting))
    ################################
    
    #methods used by route finding##
    def getSurroundingNodes(self,node):    #returns neighboring nodes and their indicators (indicators will be updated once we decide on which we are using)
        cursor=self.connection.cursor()
        cursor.execute("SELECT startNode, length,lighting FROM edges WHERE endNode = ? UNION SELECT endNode, length,lighting FROM edges WHERE startNode = ?",(node,node))
        return(cursor.fetchall())
    ################################

    #methods used by the map########
    #add node and edge
    #remove node and edge
    def getMapData(self):
        cursor=self.connection.cursor()
        cursor.execute("SELECT * FROM nodes")
        nodesData=(cursor.fetchall())
        cursor.execute("SELECT * FROM edges")
        edgeData=(cursor.fetchall())
        return(nodesData,edgeData)

    def getLocationList(self):
        cursor=self.connection.cursor()
        cursor.execute("SELECT nodeID, name FROM locations")
        return(cursor.fetchall())

    def getNodeFromLocation(self):
        cursor=self.connection.cursor()
        cursor.execute("SELECT * FROM nodes WHERE")
    ################################

    #admin methods##################
    def addMission(self,question,startNode,endNode):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO missions (missionID,question,startNode,endNode) VALUES(?,?,?,?)",(None, question, startNode,endNode))
    ################################

    #login methods##########
    def getLoginDetails(self,)