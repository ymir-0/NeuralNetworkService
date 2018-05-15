# coding=utf-8
# import
from numpy import mean
from random import shuffle
from neuralnetworkservice.database.trainingSession import TrainingSessionDB
from neuralnetworkservice.database.perceptron import PerceptronDB
# trainer
class Trainer():
    def trainCompleteSequence(self,trainingElements, trainingChunkSize):
        # INFO : randomize to be sure we do not train following the same path
        shuffle(trainingElements)
        # train step by step over complete sequence
        completeSequenceSize=len(trainingElements)
        subSequenceSize=trainingChunkSize if trainingChunkSize<=completeSequenceSize else completeSequenceSize
        lastTrainedElementsNumber = 0
        while subSequenceSize<=completeSequenceSize:
            # train current sub sequence
            # INFO : current sub sequence contains previous elements to avoid lossing previous training
            currentTrainedElementsNumber = self.trainSubSequence(trainingElements[:subSequenceSize])
            # increase sub sequence (if needed)
            if currentTrainedElementsNumber > lastTrainedElementsNumber:
                if subSequenceSize != completeSequenceSize:
                    subSequenceSize += currentTrainedElementsNumber-lastTrainedElementsNumber
                    lastTrainedElementsNumber = currentTrainedElementsNumber
                    if subSequenceSize > completeSequenceSize : subSequenceSize = completeSequenceSize
                # otherwise, stop training
                else: break
            pass
        pass
    pass
    def trainSubSequence(self,trainingElements):
        # initialize training context
        partiallyTrained = False
        trainingElementsNumber = len(trainingElements)
        # train as many as necessary
        while not partiallyTrained:
            # train once
            differentialError = self.passForwardBackwardSequence(trainingElements)
            errorElementsNumber = self.checkTraining(trainingElements)
            # TODO : add parameters to save after time or loop number
            # fill report
            meanDifferentialError = mean(differentialError)
            trainedElementsNumber = trainingElementsNumber - errorElementsNumber
            TrainingSessionDB.updateReport(self.perceptron.id, meanDifferentialError, trainedElementsNumber, errorElementsNumber)
            # save perceptron
            PerceptronDB.update(self.perceptron)
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
    def __init__(self, perceptron):
        self.perceptron = perceptron
        pass
    pass
pass
