# coding=utf-8
# import
from random import shuffle
# trainer
class Trainer():
    # training
    def passForwardBackwardSequence(self,trainingSubSet):
        # initialize errors
        errors = list()
        # INFO : randomize to be sure we do not train following the same path
        trainingElements = trainingSubSet.trainingElements
        shuffle(trainingElements)
        # run forward & backward for each training input / expected output
        for trainingElement in trainingElements:
            error = self.perceptron.passForwardBackward(trainingElement.input, trainingElement.expectedOutput)
            errors.append(error)
        # return
        return errors
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
