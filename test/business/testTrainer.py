#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from test import commonUtilities
from random import random, randint, shuffle
from neuralnetworkcommon.trainingSession import TrainingSession
from neuralnetworkservice.business.trainer import Trainer
from neuralnetworkservice.database.perceptron import PerceptronDB
from neuralnetworkservice.database.trainingSet import TrainingSetDB
from neuralnetworkservice.database.trainingSession import TrainingSessionDB
from copy import deepcopy
# test trainer
class testTrainer(TestCase):
    '''
    INFO : create a usable and simple sequence to train a neural network
     - input : there is a 10*10 grid on wich we put horizontal and vertical legs
       a leg is a length 4 vector
     - output : is the leg horizontal or vertical ?
       we use a length 2 vector :
        - horizontal : (1,0)
        - vertical : (0,1)
    '''
    def createCompleteDummyTrainingElements(self):
        # inialize elements list
        trainingElements = list()
        # run over all grid
        gridBorder = 10
        for length in range(1,gridBorder+1):
            for startPoint in range(gridBorder-1):
                for fixedPoint in range(gridBorder):
                    # set the 4 legs touching this point
                    endPoint = startPoint+length
                    trainingElement_h0 = ()
                    trainingElement_h1 = ()
                    trainingElement_v0 = ()
                    trainingElement_v1 = ()
                    trainingElements = trainingElements + [trainingElement_h0,trainingElement_h1,trainingElement_v0,trainingElement_v1]
                    pass
                pass
            pass
        # remove duplicates
        trainingElements = list(set(trainingElements))
        # shuffle and return training elements
        shuffle(trainingElements)
        return trainingElements
    def testTrainCompleteSequence(self):
        pass
    def testTrainSubSequence(self):
        # randomize perceptron and training set
        perceptron = commonUtilities.randomPerceptron()
        initialPerceptron = deepcopy(perceptron)
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
        trainer = Trainer(perceptron)
        # check initial training session
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
        # check parceptron update record
        fetchedUpdatedPerceptron = PerceptronDB.selectById(perceptron.id)
        self.assertNotEqual(initialPerceptron,fetchedUpdatedPerceptron,"ERROR : perceptron not updated")
        self.assertEqual(perceptron,fetchedUpdatedPerceptron,"ERROR : updated perceptron does not match")
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
        trainer = Trainer(perceptron)
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
        trainer = Trainer(perceptron)
        errors = trainer.passForwardBackwardSequence(trainingSubSet.trainingElements)
        # check pass forward/backward
        self.assertEqual(len(errors),trainingSize, "ERROR : pass forward/back for subsequence does not match")
        pass
    pass
pass
