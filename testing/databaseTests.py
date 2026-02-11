import unittest
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

if __name__ == '__main__':
    db = DatabaseMethods()
    db.addUser("test", "test@email.com", "password", "T")
    db.closeConnection()
    unittest.main()
