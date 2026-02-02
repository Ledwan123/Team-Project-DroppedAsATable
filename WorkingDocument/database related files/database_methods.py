import sqlite3

class DatabaseMethods:
    def __init__(self):
        self.connection=sqlite3.connect("task6.db")

    #will be called at the start, connects to/makes the database and its tables
    def setup(self):
        cursor=self.connection.cursor()
        
        #table to store users, if anyone knows anything about password security stuff we could do that instead of storing plaintext
        cursor.execute("CREATE TABLE IF NOT EXISTS nodes(nodeID INTEGER PRIMARY KEY, coordinatesX REAL, coordinatesY REAL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY, userName TEXT, email TEXT, password TEXT,userType TEXT CHECK(userType in ('T','A','M')), points INTEGER, lengthWeight REAL, lightingWeight REAL, crimeWeight REAL, trafficWeight REAL, greeneryWeight REAL, gradientWeight)") # usertype enum is short for travellers, admins, maintainers as said in the spec
        cursor.execute("CREATE TABLE IF NOT EXISTS missions(missionID INTEGER PRIMARY KEY, question TEXT, startNode INTEGER, endNode INTEGER, FOREIGN KEY(startNode) REFERENCES nodes(nodeID), FOREIGN KEY(endNode) REFERENCES nodes(nodeID))") #will change missions depending on how we deal with representing/storing routes
        cursor.execute("CREATE TABLE IF NOT EXISTS changes(changeID INTEGER PRIMARY KEY, userID INTEGER, missionID INTEGER, time TEXT, FOREIGN KEY(userID) REFERENCES users(userID), FOREIGN KEY(missionID) REFERENCES missions(missionID))")
        cursor.execute("CREATE TABLE IF NOT EXISTS locations(locationID INTEGER PRIMARY KEY, name TEXT, nodeID INTEGER, locationType TEXT, FOREIGN KEY(nodeID) REFERENCES nodes(nodeID))") #type will be used if we want to display locations with icons on the map e.g station type with a small train image etc...
        cursor.execute("CREATE TABLE IF NOT EXISTS edges(edgeID INTEGER PRIMARY KEY, startNode INTEGER, endNode INTEGER, length REAL, lighting REAL, crime REAL, traffic REAL, greenery REAL, gradient REAL, FOREIGN KEY(startNode) REFERENCES nodes(nodeID), FOREIGN KEY(endNode) REFERENCES nodes(nodeID))")#other indicators will be added here depending on what we decide on

        return()
    
    #methods used by route finding##
    def getUserWeights(self, userID):
        cursor=self.connection.cursor()
        cursor.execute("SELECT lengthWeight, lightingWeight, crimeWeight, trafficWeight, greeneryWeight, gradientWeight FROM users WHERE userID = ?", (userID))
        return(cursor.fetchall())

    def setUserWeights(self,userID, weights):
        cursor=self.connection.cursor()
        cursor.execute("UPDATE users SET lengthWeight=?, lightingWeight=?,crimeWeight=?, trafficWeight=?, greeneryWeight=?, gradientWeight=? WHERE userID = ?",(weights[0],weights[1],weights[2],weights[3],weights[4],weights[5],userID))

    def getSurroundingNodes(self,node):    #returns neighboring nodes and their indicators
        cursor=self.connection.cursor()
        cursor.execute("SELECT startNode, length,lighting,crime,traffic,greenery,gradient FROM edges WHERE endNode = ? UNION SELECT endNode, length,lighting,crime,traffic,greenery,gradient FROM edges WHERE startNode = ?",(node,node))
        return(cursor.fetchall())
    ################################

    #methods used by the map########
    def addNode(self,coordinatesX,coordinatesY):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO nodes (nodeID, coordinatesX,coordinatesY) VALUES (?,?,?)",(None, coordinatesX,coordinatesY))

    def addEdge(self,startNode,endNode,length,lighting,crime,traffic,greenery,gradient):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO edges(edgeID,startNode,endNode,length,lighting,crime,traffic,greenery,gradient) VALUES(?,?,?,?,?)",(None,startNode,endNode,length,lighting))

    def addLocation(self,name,nodeID,locationType):
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO locations (locationID,name,nodeID,locationType) VALUES(?,?,?,?)",(None,name,nodeID,locationType))

    def deleteNode(self, nodeID):  #deletes a node from the table using its nodeID, also removes any related edges and locations
        cursor=self.connection.cursor()
        cursor.execute("DELETE FROM locations WHERE nodeID =?",(nodeID))
        cursor.execute("DELETE FROM edges WHERE startNode =?",(nodeID))
        cursor.execute("DELETE FROM edges WHERE endNode =?",(nodeID))
        cursor.execute("DELETE FROM nodes WHERE nodeID =?",(nodeID))
  
    def getMapData(self): #returns a tuple containing (node/location data (if a node isnt a location, location data columns are null) and edge data
        cursor.execute("SELECT nodes.nodeID, nodes.coordinatesX, nodes.coordinatesY, locations.name, locations.locationType FROM nodes LEFT OUTER JOIN locations ON nodes.nodeID=locations.nodeID")
        nodesData=(cursor.fetchall())
        cursor.execute("SELECT * FROM edges")
        edgeData=(cursor.fetchall())
        return(nodesData,edgeData)

    def getLocationList(self): #In case we want to have a menu to select start/end locations
        cursor=self.connection.cursor()
        cursor.execute("SELECT nodeID, name FROM locations")
        return(cursor.fetchall())
    ################################

    #mission methods################
    def addMission(self,question,startNode,endNode):  #for use by an admin to add to the missions table
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO missions (missionID,question,startNode,endNode) VALUES(?,?,?,?)",(None, question, startNode,endNode))

    def addChange(self,userID,missionID,time): #whenever a change is made to a mission, use this to record it in the log
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO changes (changeID, userID, missionID, time) VALUES(?,?,?,?)",(None,userID,missionID,time))

    def addPoints(self, userID): #when a user completes a mission, use this to add a point to their score
        cursor=self.connection.cursor()
        cursor.execute("SELECT points FROM users WHERE userID = ?", (userID))
        cursor.execute("UPDATE users SET points = ? WHERE userID=?",(cursor.fetchall()+1,userID))
    ################################

    #login methods##################
    def addUser(self,username, email, password,usertype): #used when a user chooses to sign up and make an account
        cursor=self.connection.cursor()
        cursor.execute("INSERT INTO users (userID,userName,email,password,userType,points,lengthWeight,lightingWeight,crimeWeight, trafficWeight, greeneryWeight, gradientWeight) VALUES (?,?,?,?,?,?,?,?)",(None, username, email, password, usertype,0,1,1,1,1,1,1))

    def getLoginDetails(self, username, email):  #given the username and email, returns passwords
        cursor=self.connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ? AND email = ?",(username, email))

    #################################
