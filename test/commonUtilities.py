# coding=utf-8
# import
from random import random, randint, choice
from string import ascii_letters
from neuralnetworkcommon.trainingSet import TrainingElement
# test utilities
# INFO : those utilities are not merged with common neural network one because test modules are not deployed in libraries
def genereteRandomPerceptronParameters():
    layersNumber = randint(2, 12)
    dimensions = [randint(2, 100) for _ in range(layersNumber)]
    comments = "".join([choice(ascii_letters) for _ in range(15)])
    return dimensions, comments
pass
def genereteTrainingSetParameters():
    # generate training elements
    trainingElements = list()
    dimension = randint(20, 100)
    for trainingSize in range(randint(15, 95)):
        input = [(random() - .5) * 2 for _ in range(dimension)]
        expectedOutput = [(random() - .5) * 2 for _ in range(dimension)]
        trainingElement = TrainingElement.constructFromAttributes(input,expectedOutput)
        trainingElements.append(trainingElement)
    # comments
    comments = "".join([choice(ascii_letters) for _ in range(15)])
    # return
    return trainingElements, comments
pass
