#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from random import randint, choice
from string import ascii_letters
from neuralnetworkcommon.perceptron import Perceptron
from neuralnetworkservice.database.perceptron import PerceptronDB
# test perceptron
class testPerceptronDB(TestCase):
    # test CRUD OK
    def testCrudOK(self):
        # initialize random perceptron
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        perceptron = Perceptron(dimensions,comments)
        # call DB create
        PerceptronDB.create(perceptron)
        pass
    pass
pass
