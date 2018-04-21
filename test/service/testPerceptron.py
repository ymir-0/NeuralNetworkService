#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from neuralnetworkservice.service.service import application
from json import dumps
from random import randint, choice
from string import ascii_letters
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonDecoder
# test perceptron
class testPerceptronWS(TestCase):
    APPLICATION = application.test_client()
    # test CRUD OK
    def testGlobalGetOk(self):
        # randomize layers numbers, dimensions & comments
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        # get randomized perceptron
        response = testPerceptronWS.APPLICATION.post("/perceptron",data=dumps({"dimensions": dimensions,"comments":comments}),content_type='application/json')
        dumpedPerceptron = response.data.decode()
        rawPerceptron = ComplexJsonDecoder.loadComplexObject(dumpedPerceptron)
        #
        pass
    # utilities
    @classmethod
    def setUpClass(cls):
        testPerceptronWS.APPLICATION.testing = True
    pass
pass
