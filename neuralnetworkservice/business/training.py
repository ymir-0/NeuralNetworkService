# coding=utf-8
# import
from random import shuffle
# trainer
class Trainer():
    # training
    def passForwardBackwardSequence(self,trainingElements):
        # initialize errors
        errors = list()
        # INFO : randomize to be sure we do not train following the same path
        shuffle(trainingElements)
        # run forward & backward for each training input / expected output
        for trainingElement in trainingElements:
            error = self.perceptron.passForwardBackward(trainingElement.input, trainingElement.expectedOutput)
            errors.append(error)
        # return
        return errors
    # TODO : create others check methods (not only match maximum element)
    def checkTraining(self,trainingElements):
        # initialize errors
        outputErrorCounter = 0
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
            if outputError: outputErrorCounter+=1
        # return
        return outputErrorCounter
    pass
    #constructors
    # INFO : test ration between 0 (no data used to test, all for training) and 1 (no data used to training, all for test)
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
