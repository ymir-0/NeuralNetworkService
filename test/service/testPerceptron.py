#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from neuralnetworkservice.service.service import application
from json import dumps
from random import randint, choice
from string import ascii_letters
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder, ComplexJsonDecoder
from neuralnetworkcommon.perceptron import Perceptron
from json import loads
# test perceptron
class testPerceptronWS(TestCase):
    APPLICATION = application.test_client()
    CONTENT_TYPE = "application/json"
    # test random generation
    def testRandomGetOk(self):
        # randomize layers numbers, dimensions & comments
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        # get randomized perceptron
        response = testPerceptronWS.APPLICATION.get("/perceptron/random",data=dumps({"dimensions": dimensions,"comments":comments}),content_type=testPerceptronWS.CONTENT_TYPE)
        dumpedPerceptron = response.data.decode()
        rawPerceptron = ComplexJsonDecoder.loadComplexObject(dumpedPerceptron)
        # check perceptron
        self.assertEqual(response.status_code,200,"ERROR : response status does not match")
        self.assertTrue(type(rawPerceptron)==Perceptron,"ERROR : perceptron type does not match")
    # test CRUD OK
    def testCrudOK(self):
        # randomize initial perceptron
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        rawInitialPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        dumpedInitialPerceptron = ComplexJsonEncoder.dumpComplexObject(rawInitialPerceptron)
        loadedInitialPerceptron = loads(dumpedInitialPerceptron)
        # create perceptron
        initialPerceptronId = testPerceptronWS.APPLICATION.post("/perceptron",data=dumpedInitialPerceptron,content_type=testPerceptronWS.CONTENT_TYPE)
        #
        pass
    # utilities
    @classmethod
    def setUpClass(cls):
        testPerceptronWS.APPLICATION.testing = True
    pass
pass
