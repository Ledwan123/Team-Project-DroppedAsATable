import unittest
from database_methods import *

class TestDatabaseMethods(unittest.TestCase):
    def testAddUser(self):
        db = DatabaseMethods()
        db.addUser()
        db.closeConnection()
    def testUserWeights(self):
        DatabaseMethods.setUserWeights()