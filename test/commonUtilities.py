# coding=utf-8
# import
from random import random, randint, choice
from string import ascii_letters
from neuralnetworkcommon.trainingSet import TrainingElement, TrainingSet
from neuralnetworkcommon.perceptron import Perceptron
# test utilities
# INFO : those utilities are not merged with common neural network one because test modules are not deployed in libraries
def genereteRandomPerceptronParameters():
    layersNumber = randint(2, 12)
    dimensions = [randint(2, 100) for _ in range(layersNumber)]
    comments = "".join([choice(ascii_letters) for _ in range(15)])
    return dimensions, comments
def randomPerceptron():
    dimensions, comments = genereteRandomPerceptronParameters()
    perceptron = Perceptron.constructRandomFromDimensions(dimensions, comments)
    return perceptron
def genereteTrainingSetParameters(inputDimension=randint(20, 100), outputDimension=randint(20, 100), trainingSize=randint(15, 95)):
    # generate training elements
    trainingElements = list()
    for _ in range(trainingSize):
        input = [(random() - .5) * 2 for _ in range(inputDimension)]
        expectedOutput = [(random() - .5) * 2 for _ in range(outputDimension)]
        trainingElement = TrainingElement.constructFromAttributes(input,expectedOutput)
        trainingElements.append(trainingElement)
    # comments
    comments = "".join([choice(ascii_letters) for _ in range(15)])
    # return
    return trainingElements, comments
def randomTrainingSet(inputDimension=randint(20, 100), outputDimension=randint(20, 100), trainingSize=randint(15, 95)):
    trainingElements, comments = genereteTrainingSetParameters(inputDimension, outputDimension, trainingSize)
    trainingSet = TrainingSet.constructFromAttributes(None, trainingElements, comments)
    return trainingSet
pass
