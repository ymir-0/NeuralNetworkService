#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from test import commonUtilities
from random import random
from string import ascii_letters
from random import choice
from neuralnetworkservice.database.perceptron import PerceptronDB
from neuralnetworkservice.database.trainingSet import TrainingSetDB
from neuralnetworkservice.database.trainingSession import TrainingSessionDB
from neuralnetworkcommon.trainingSession import TrainingSession
# test training session
class testTrainingSessionDB(TestCase):
    # test CRUD OK
    def testCrudOK(self):
        # initialize random perceptron & training set
        perceptron = commonUtilities.randomPerceptron()
        PerceptronDB.insert(perceptron)
        trainingSet = commonUtilities.randomTrainingSet()
        TrainingSetDB.insert(trainingSet)
        # initialize random training session
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        initialTrainingSession = TrainingSession.constructFromTrainingSet(perceptron.id,trainingSet,random(),comments)
        # call DB insert
        TrainingSessionDB.insert(initialTrainingSession)
        # call DB select by id
        fetchedInsertedTrainingSession = TrainingSessionDB.selectByPerceptronId(initialTrainingSession.perceptronId)
        expectedInsertedTrainingSession = None
        # check DB select by id
        self.assertEqual(expectedInsertedTrainingSession,fetchedInsertedTrainingSession,"ERROR : inserted trainingSession does not match")
        # call DB update
        pass
    pass
pass
