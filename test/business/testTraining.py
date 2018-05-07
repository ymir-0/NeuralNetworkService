#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from test import commonUtilities
from random import random
from neuralnetworkservice.business.training import Trainer
# test trainer
class testPerceptronDB(TestCase):
    # test constructors
    def testDefaultConstructor(self):
        # randomize perceptron and training set
        perceptron = commonUtilities.randomPerceptron()
        trainingSet = commonUtilities.randomTrainingSet()
        trainingElements = trainingSet.trainingElements
        expectedDataSet = set(trainingElements)
        testRatio = random()
        # generate trainer
        trainer = Trainer(perceptron,trainingSet,testRatio)
        # check trainer
        actualTrainingSet = set(trainer.trainingSet)
        actualTestSet = set(trainer.testSet)
        commonData = actualTrainingSet.intersection(actualTestSet)
        actualDataSet = actualTrainingSet.union(actualTestSet)
        self.assertSetEqual(commonData, set(), "ERROR : test & training data collides")
        self.assertSetEqual(actualDataSet,expectedDataSet, "ERROR : merged test & training data does not fill data set")
        pass
