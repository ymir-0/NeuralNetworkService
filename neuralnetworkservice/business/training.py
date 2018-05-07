# coding=utf-8
# import
from random import shuffle
# trainer
class Trainer():
    # training
    def passForwardBackwardSequence(self,trainingSet):
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
