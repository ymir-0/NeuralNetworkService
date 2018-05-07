#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from test import commonUtilities
from random import random, randint
from neuralnetworkservice.business.training import Trainer
# test trainer
class testPerceptronDB(TestCase):
    def testCheckTraining(self):
        # randomize perceptron and training set
        perceptron = commonUtilities.randomPerceptron()
        inputDimension = len(perceptron.layers[0].weights[0])
        outputDimension = len(perceptron.layers[-1].weights)
        trainingSize = randint(15, 95)
        trainingSubSet = commonUtilities.randomTrainingSet(inputDimension, outputDimension, trainingSize)
        # sequence outputs
        # check training
        trainer = Trainer(perceptron,commonUtilities.randomTrainingSet(),0)
        outputErrorCounter = trainer.checkTraining(trainingSubSet.trainingElements)
        pass
    def testPassForwardBackwardSequence(self):
        # randomize perceptron and training set
        perceptron = commonUtilities.randomPerceptron()
        inputDimension = len(perceptron.layers[0].weights[0])
        outputDimension = len(perceptron.layers[-1].weights)
        trainingSize = randint(15, 95)
        trainingSubSet = commonUtilities.randomTrainingSet(inputDimension, outputDimension, trainingSize)
        # test pass forward/backward
        trainer = Trainer(perceptron,commonUtilities.randomTrainingSet(),0)
        errors = trainer.passForwardBackwardSequence(trainingSubSet.trainingElements)
        # check pass forward/backward
        self.assertEqual(len(errors),trainingSize, "ERROR : pass forward/back for subsequence does not match")
        pass
    # test constructors
    def testDefaultConstructor(self):
        # randomize perceptron and training set
        perceptron = commonUtilities.randomPerceptron()
        trainingSet = commonUtilities.randomTrainingSet()
        expectedDataSet = set(trainingSet.trainingElements)
        # generate trainer
        trainer = Trainer(perceptron,trainingSet,random())
        # check trainer
        actualTrainingSet = set(trainer.trainingSet)
        actualTestSet = set(trainer.testSet)
        commonData = actualTrainingSet.intersection(actualTestSet)
        actualDataSet = actualTrainingSet.union(actualTestSet)
        self.assertSetEqual(commonData, set(), "ERROR : test & training data collides")
        self.assertSetEqual(actualDataSet,expectedDataSet, "ERROR : merged test & training data does not fill data set")
        pass
    pass
pass
