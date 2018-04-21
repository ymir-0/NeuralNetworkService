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
# test perceptron
class testPerceptronWS(TestCase):
    APPLICATION = application.test_client()
    CONTENT_TYPE = "application/json"
    # test random generation
    def testRandomGetOk(self):
        # get randomized perceptron
        dimensions, comments = testPerceptronWS.genereteRandomPerceptronParameters()
        response = testPerceptronWS.APPLICATION.get("/perceptron/random",data=dumps({"dimensions": dimensions,"comments":comments}),content_type=testPerceptronWS.CONTENT_TYPE)
        dumpedPerceptron = response.data.decode()
        rawPerceptron = ComplexJsonDecoder.loadComplexObject(dumpedPerceptron)
        # check perceptron
        self.assertEqual(response.status_code,200,"ERROR : response status does not match")
        self.assertTrue(type(rawPerceptron)==Perceptron,"ERROR : perceptron type does not match")
    # test CRUD OK
    def testCrudOK(self):
        # randomize initial perceptron
        dimensions, comments = testPerceptronWS.genereteRandomPerceptronParameters()
        rawInitialPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        dumpedInitialPerceptron = ComplexJsonEncoder.dumpComplexObject(rawInitialPerceptron)
        # precheck
        self.assertFalse(hasattr(rawInitialPerceptron,"id"),"ERROR : perceptron has id")
        # create perceptron
        response = testPerceptronWS.APPLICATION.post("/perceptron",data=dumpedInitialPerceptron,content_type=testPerceptronWS.CONTENT_TYPE)
        perceptronId = int(response.data)
        # check creation
        self.assertIsNotNone(perceptronId,"ERROR : perceptron has no id")
        rawInitialPerceptron.id = perceptronId
        # read perceptron
        response = testPerceptronWS.APPLICATION.get("/perceptron/"+str(perceptronId))
        dumpedPerceptron = response.data.decode()
        rawFetchedInsertedPerceptron = ComplexJsonDecoder.loadComplexObject(dumpedPerceptron)
        # check reading
        self.assertEqual(rawInitialPerceptron,rawFetchedInsertedPerceptron,"ERROR : inserted perceptron does not match")
        # update perceptron
        dimensions, comments = testPerceptronWS.genereteRandomPerceptronParameters()
        rawNewPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        dumpedNewPerceptron = ComplexJsonEncoder.dumpComplexObject(rawNewPerceptron)
        testPerceptronWS.APPLICATION.put("/perceptron/"+str(perceptronId),data=dumpedNewPerceptron,content_type=testPerceptronWS.CONTENT_TYPE)
        # check update
        response = testPerceptronWS.APPLICATION.get("/perceptron/"+str(perceptronId))
        dumpedPerceptron = response.data.decode()
        rawFetchedUpdatedPerceptron = ComplexJsonDecoder.loadComplexObject(dumpedPerceptron)
        self.assertNotEqual(rawFetchedUpdatedPerceptron,rawFetchedInsertedPerceptron,"ERROR : perceptron not updated")
        rawNewPerceptron.id = perceptronId
        self.assertEqual(rawFetchedUpdatedPerceptron,rawNewPerceptron,"ERROR : updated perceptron does not match")
        #
        pass
    # utilities
    @classmethod
    def setUpClass(cls):
        testPerceptronWS.APPLICATION.testing = True
    @staticmethod
    def genereteRandomPerceptronParameters():
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        return dimensions, comments
    pass
pass
