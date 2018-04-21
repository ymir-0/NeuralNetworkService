# coding=utf-8
# import
from random import randint, choice
from string import ascii_letters
# test utilities
# INFO : those utilities are not merged with common neural network one because test modules are not deployed in libraries
def genereteRandomPerceptronParameters():
    layersNumber = randint(2, 12)
    dimensions = [randint(2, 100) for _ in range(layersNumber)]
    comments = "".join([choice(ascii_letters) for _ in range(15)])
    return dimensions, comments
pass
