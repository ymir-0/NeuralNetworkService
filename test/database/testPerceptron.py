#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from random import randint, choice
from string import ascii_letters
from neuralnetworkcommon.perceptron import Perceptron
from neuralnetworkservice.database.perceptron import PerceptronDB
# test perceptron
class testPerceptronDB(TestCase):
    @staticmethod
    def randomPerceptron():
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        perceptron = Perceptron(dimensions,comments)
        return perceptron
    # test CRUD OK
    def testCrudOK(self):
        # initialize random perceptron
        initialPerceptron = testPerceptronDB.randomPerceptron()
        # precheck
        self.assertFalse(hasattr(initialPerceptron,"id"),"ERROR : perceptron has id")
        # call DB insert
        PerceptronDB.insert(initialPerceptron)
        # check DB insert
        self.assertTrue(hasattr(initialPerceptron,"id"),"ERROR : perceptron has no id")
        # call DB select by id
        fetchedInsertedPerceptron = PerceptronDB.selectById(initialPerceptron.id)
        # check DB select by id
        self.assertEqual(initialPerceptron,fetchedInsertedPerceptron,"ERROR : inserted perceptron does not match")
        # call DB update
        newPerceptron = testPerceptronDB.randomPerceptron()
        newPerceptron.id = initialPerceptron.id
        PerceptronDB.update(newPerceptron)
        # check DB update
        fetchedUpdatedPerceptron = PerceptronDB.selectById(initialPerceptron.id)
        self.assertNotEqual(fetchedUpdatedPerceptron,fetchedInsertedPerceptron,"ERROR : perceptron not updated")
        self.assertEqual(fetchedUpdatedPerceptron,newPerceptron,"ERROR : updated perceptron does not match")
        # call DB delete
        PerceptronDB.deleteById(initialPerceptron.id)
        # check DB delete
        deletedPerceptron = PerceptronDB.selectById(initialPerceptron.id)
        self.assertIsNone(deletedPerceptron,"ERROR : perceptron not deleted")
        pass
    # test CRUD OK
    def testSelectDeleteAll(self):
        # initialize random perceptrons
        initialIds=set()
        perceptronNumber = randint(5, 10)
        for _ in range(perceptronNumber):
            perceptron = testPerceptronDB.randomPerceptron()
            PerceptronDB.insert(perceptron)
            initialIds.add(perceptron.id)
            pass
        # select IDs
        fetchedIds = PerceptronDB.selectAllIds()
        # check IDs
        self.assertTrue(initialIds.issubset(fetchedIds),"ERROR : IDs selection does not match")
        # delete all
        PerceptronDB.deleteAll()
        # check IDs
        deletedIds = PerceptronDB.selectAllIds()
        self.assertEqual(len(deletedIds),0,"ERROR : complete deletion failed")
        pass
    pass
pass
