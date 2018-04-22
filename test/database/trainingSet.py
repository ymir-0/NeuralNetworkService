#!/usr/bin/env python3
# coding=utf-8
# import
from random import randint, choice
from neuralnetworkcommon.perceptron import TrainingSet
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
        pass
    pass
pass

