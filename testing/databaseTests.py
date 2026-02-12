import unittest
import os
from database_methods import *

class TestDatabaseMethods(unittest.TestCase):
    # USER TESTS
    def testAddUser(self):
        db = DatabaseMethods()
        userType = db.getUserType(1)
        self.assertEqual(userType[0][0], "T") # note that single values are returned as tuples
        db.closeConnection()

    def testUserWeights(self):
        db = DatabaseMethods()
        weights = db.getUserWeights(1)
        self.assertEqual(weights, [(0.6, 0.1, 0.1, 0.1, 0.1)])
        db.setUserWeights(1, [0,0.2,0.3,0.4,0.8])
        weights = db.getUserWeights(1)
        self.assertEqual(weights, [(0,0.2,0.3,0.4,0.8)])
        db.closeConnection()
        resetDatabase()

    # MAP TESTS
    def testGetNodes(self):
        db = DatabaseMethods()
        nodes = db.getAllNodes()
        self.assertEqual(nodes, [(1, 0.1, 0.1, 0.1, 0.1), (2, 0.2, 0.2, 0.2, 0.2), (3, 0.3, 0.3, 0.3, 0.3), (4, 0.4, 0.4, 0.4, 0.4)])
        self.assertTrue(db.nodeExists(1))
        self.assertFalse(db.nodeExists(17))
        db.closeConnection()
        

    def testUpdateNode(self):
        db = DatabaseMethods()
        db.updateNode(1, 2, 2, 5, 5, 5, 5)
        nodes = db.getAllNodes()
        self.assertEqual(nodes[0], (1, 5, 5, 5, 5))
        db.closeConnection()
        resetDatabase()

    def testGetAllEdges(self):
        db = DatabaseMethods()
        edges = db.getAllEdges()
        self.assertEqual([(1, 1, 2, 20), (2, 1, 3, 40), (3, 2, 3, 50)], edges)
        db.closeConnection()

    def testUpdateEdgeLength(self):
        db = DatabaseMethods()
        db.editLength(1, 30)
        edges = db.getAllEdges()
        self.assertEqual([(1, 1, 2, 30), (2, 1, 3, 40), (3, 2, 3, 50)], edges)
        db.closeConnection()
        resetDatabase()

    def testGetSurroundingLength(self):
        db = DatabaseMethods()
        oneEdges = db.getSurroundingLength(1)
        self.assertEqual(oneEdges, [(2, 20), (3, 40)])
        db.closeConnection()

    def testDeleteNode(self):
        db = DatabaseMethods()
        db.deleteNode(1)
        self.assertFalse(db.nodeExists(1))
        edges = db.getAllEdges()
        self.assertEqual([(3, 2, 3, 50)], edges)
        self.assertEqual([(2, "St. David's")], db.getLocationList())
        db.closeConnection()
        resetDatabase()

    def testGetLocations(self):
        db = DatabaseMethods()
        locs = db.getLocationList()
        self.assertEqual(locs, [(1, "University of Exeter"), (2, "St. David's")])
        db.closeConnection()

    # MISSION TESTS
        
    
def resetDatabase():
    try:
        os.remove("testing.db")
    except:
        print("something went wrong, hope that the overwrite works")
    db = DatabaseMethods()
    #nodes
    db.addNode(1, 1, 0.1, 0.1, 0.1, 0.1, 0.1)
    db.addNode(2, 2, 0.2, 0.2, 0.2, 0.2, 0.2)
    db.addNode(3, 3, 0.3, 0.3, 0.3, 0.3, 0.3)
    db.addNode(4, 4, 0.4, 0.4, 0.4, 0.4, 0.4)
    #edges
    db.addEdge(1, 1, 2, 20)
    db.addEdge(2, 1, 3, 40)
    db.addEdge(3, 2, 3, 50)
    #user
    db.addUser("test", "test@email.com", "password", "T")
    #location
    db.addLocation("University of Exeter", 1, "University")
    db.addLocation("St. David's", 2, "Station")
    db.closeConnection()
    

if __name__ == '__main__':
    resetDatabase()
    unittest.main(exit=False)
    os.remove("testing.db")
