#!/usr/bin/env python3
# coding=utf-8
# import
from random import choice
from neuralnetworkcommon.trainingSet import TrainingSet
from neuralnetworkservice.database.trainingSet import TrainingSetDB
from unittest import TestCase
from test import commonUtilities
from string import ascii_letters
# utilities
def randomTrainingSet():
    trainingElements, comments = commonUtilities.genereteTrainingSetParameters()
    trainingSet = TrainingSet.constructFromAttributes(None, trainingElements, comments)
    return trainingSet
# test training set
class testTrainingSetDB(TestCase):
    # test CRUD OK
    def testCrudOK(self):
        # initialize random trainingSet
        initialTrainingSet = randomTrainingSet()
        # precheck
        self.assertIsNone(initialTrainingSet.id,"ERROR : trainingSet has id")
        # call DB insert
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        TrainingSetDB.insert(initialTrainingSet)
        # check DB insert
        self.assertIsNotNone(initialTrainingSet.id,"ERROR : trainingSet has no id")
        # call DB select by id
        fetchedInsertedTrainingSet = TrainingSetDB.selectById(initialTrainingSet.id)
        # check DB select by id
        self.assertEqual(initialTrainingSet,fetchedInsertedTrainingSet,"ERROR : inserted trainingSet does not match")
        # call DB update
        newTrainingSet = randomTrainingSet()
        newTrainingSet.id = initialTrainingSet.id
        TrainingSetDB.update(newTrainingSet)
        # check DB update
        fetchedUpdatedTrainingSet = TrainingSetDB.selectById(initialTrainingSet.id)
        self.assertNotEqual(fetchedUpdatedTrainingSet,fetchedInsertedTrainingSet,"ERROR : trainingSet not updated")
        self.assertEqual(fetchedUpdatedTrainingSet,newTrainingSet,"ERROR : updated trainingSet does not match")
        # call DB delete
        TrainingSetDB.deleteById(initialTrainingSet.id)
        # check DB delete
        deletedTrainingSet = TrainingSetDB.selectById(initialTrainingSet.id)
        self.assertIsNone(deletedTrainingSet,"ERROR : trainingSet not deleted")
        pass
    pass
pass

