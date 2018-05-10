# coding=utf-8
# import
from numpy import mean
from random import shuffle
# trainer
class Trainer():
    def trainSubSequence(self,trainingElements):
        # initialize training context
        partiallyTrained = False
        trainingElementsNumber = len(trainingElements)
        # train as many as necessary
        while not partiallyTrained:
            # train once
            differentialError = self.passForwardBackwardSequence(trainingElements)
            errorElementsNumber = self.checkTraining(trainingElements)
            # fill report
            meanDifferentialError = mean(differentialError)
            trainedElementsNumber = trainingElementsNumber - errorElementsNumber
            # check partial training
            partiallyTrained = errorElementsNumber<trainingElementsNumber
        return trainedElementsNumber
    pass
    # training
    def passForwardBackwardSequence(self,trainingElements):
        # initialize errors
        differentialError = list()
        # INFO : randomize to be sure we do not train following the same path
        shuffle(trainingElements)
        # run forward & backward for each training input / expected output
        for trainingElement in trainingElements:
            error = self.perceptron.passForwardBackward(trainingElement.input, trainingElement.expectedOutput)
            differentialError.append(error)
        # return
        return differentialError
    # TODO : create others check methods (not only match maximum element)
    def checkTraining(self,trainingElements):
        # initialize errors
        errorElementsNumber = 0
        # run forward & backward for each training input / expected output
        for trainingElement in trainingElements:
            expectedOutput = trainingElement.expectedOutput
            maximumExpectedValue = max(expectedOutput)
            expectedIndex = expectedOutput.index(maximumExpectedValue)
            actualOutput = self.perceptron.passForward(trainingElement.input)
            actualOutput = [float(_) for _ in actualOutput]
            maximumActualValue = max(actualOutput)
            actualIndex = actualOutput.index(maximumActualValue)
            outputError = expectedIndex==actualIndex
            if outputError: errorElementsNumber+=1
        # return
        return errorElementsNumber
    pass
    #constructors
    # INFO : test ration between 0 (no data used to test, all for training) and 1 (no data used to training, all for test)
    # TODO : replace splitting data set with test ratio with direct training set
    def __init__(self, perceptron,dataSet,testRatio):
        # set perceptron
        self.perceptron = perceptron
        # dispatch training / test data
        dataElements = dataSet.trainingElements
        shuffle(dataElements)
        testSetLength = int(len(dataElements)*testRatio)
        self.testSet = dataElements[:testSetLength]
        self.trainingSet = dataElements[testSetLength:]
        pass
    pass
pass
