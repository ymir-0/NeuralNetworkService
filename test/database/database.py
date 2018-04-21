# coding=utf-8
# import
from unittest import TestCase
from neuralnetworkservice.database.database import Database
# database test utilities
class TestDatabase(TestCase):
    @classmethod
    def tearDownClass(cls):
        Database.closeConnection()
    pass
pass
