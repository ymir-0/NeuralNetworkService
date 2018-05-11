#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from test import commonUtilities
from random import random, randint
from neuralnetworkservice.business.training import Trainer
from neuralnetworkservice.database.perceptron import PerceptronDB
from neuralnetworkservice.database.trainingSet import TrainingSetDB
from neuralnetworkservice.database.trainingSession import TrainingSessionDB
from neuralnetworkcommon.trainingSession import TrainingSession
# test trainer
class testPerceptronDB(TestCase):
    def testTrainSubSequence(self):
        # randomize perceptron and training set
        perceptron = commonUtilities.randomPerceptron()
        PerceptronDB.insert(perceptron)
        inputDimension = len(perceptron.layers[0].weights[0])
        outputDimension = len(perceptron.layers[-1].weights)
        trainingSize = randint(10, 15)
        trainingSet = commonUtilities.randomTrainingSet(inputDimension, outputDimension, trainingSize)
        TrainingSetDB.insert(trainingSet)
        trainingElements = trainingSet.trainingElements
        # initialize training session & trainer
        trainingSession = TrainingSession.constructFromTrainingSet(perceptron.id,trainingSet,random())
        TrainingSessionDB.insert(trainingSession)
        trainer = Trainer(perceptron,commonUtilities.randomTrainingSet(),0)
        # check training initial session
        fetchedInitialReport = TrainingSessionDB.selectByPerceptronId(perceptron.id)
        self.assertIsNone(fetchedInitialReport.meanDifferantialErrors,"ERROR : initial meanDifferantialError does not match")
        self.assertIsNone(fetchedInitialReport.trainedElementsNumbers,"ERROR : initial trainedElementsNumber does not match")
        self.assertIsNone(fetchedInitialReport.errorElementsNumbers,"ERROR : initial errorElementsNumber does not match")
        # train subsequence
        trainedElementsNumber = trainer.trainSubSequence(trainingElements)
        # check training
        self.assertGreater(trainedElementsNumber, 0, "ERROR : negative trained elements number")
        self.assertLessEqual(trainedElementsNumber, len(trainingElements), "ERROR : trained elements number greater than training set")
        # check training session update
        fetchedUpdatedReport = TrainingSessionDB.selectByPerceptronId(perceptron.id)
        self.assertEqual(len(fetchedUpdatedReport.meanDifferantialErrors),1,"ERROR : updated meanDifferantialError does not match")
        self.assertEqual(len(fetchedUpdatedReport.trainedElementsNumbers),1,"ERROR : updated trainedElementsNumber does not match")
        self.assertEqual(len(fetchedUpdatedReport.errorElementsNumbers),1,"ERROR : updated errorElementsNumber does not match")
        # clean database
        TrainingSessionDB.deleteById(perceptron.id)
        PerceptronDB.deleteById(perceptron.id)
        TrainingSetDB.deleteById(trainingSet.id)
        pass
    def testCheckTraining(self):
        # randomize perceptron and training set
        perceptron = commonUtilities.randomPerceptron()
        inputDimension = len(perceptron.layers[0].weights[0])
        outputDimension = len(perceptron.layers[-1].weights)
        trainingSize = randint(15, 95)
        trainingSet = commonUtilities.randomTrainingSet(inputDimension, outputDimension, trainingSize)
        trainingElements = trainingSet.trainingElements
        # generate errors
        expectedErrorNumber = randint(1, trainingSize)
        errorCounter = 0
        for trainingElement in trainingSet.trainingElements:
            actualOutput = perceptron.passForward(trainingElement.input)
            actualOutput = [float(_) for _ in actualOutput]
            # generate error (if not enought yet)
            maximumValue = max(actualOutput)
            maximumValueIndex = actualOutput.index(maximumValue)
            if errorCounter < expectedErrorNumber:
                actualOutput[maximumValueIndex] = maximumValue + 1
                errorCounter += 1
            else:
                actualOutput[maximumValueIndex] = maximumValue - 1
            trainingElement.expectedOutput = actualOutput
            pass
        # run training checking
        trainer = Trainer(perceptron,commonUtilities.randomTrainingSet(),0)
        actualErrorNumber = trainer.checkTraining(trainingElements)
        # check training checking
        self.assertEqual(actualErrorNumber, expectedErrorNumber, "ERROR : error counter does not match")
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
