import unittest
import os
from database_methods import *

class TestDatabaseMethods(unittest.TestCase):
    def testAddUser(self):
        db = DatabaseMethods()
        userType = db.getUserType(1)
        self.assertEqual(userType[0][0], "T") # note that single values are returned as tuples
        db.closeConnection()

    def testUserWeights(self):
        db = DatabaseMethods()
        weights = db.getUserWeights(1)
        self.assertEqual(weights, [(1.0,1.0,1.0,1.0,1.0)])
        db.setUserWeights(1, [0,0.2,0.3,0.4,0.8])
        weights = db.getUserWeights(1)
        self.assertEqual(weights, [(0,0.2,0.3,0.4,0.8)])
        db.closeConnection()

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
    

if __name__ == '__main__':
    db = DatabaseMethods()
    db.addUser("test", "test@email.com", "password", "T")
    db.addNode(1, 1, 0.1, 0.1, 0.1, 0.1, 0.1)
    db.addNode(2, 2, 0.2, 0.2, 0.2, 0.2, 0.2)
    db.addNode(3, 3, 0.3, 0.3, 0.3, 0.3, 0.3)
    db.addNode(4, 4, 0.4, 0.4, 0.4, 0.4, 0.4)
    db.closeConnection()
    unittest.main(exit=False)
    os.remove("testing.db")
