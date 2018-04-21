#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from json import dumps
from random import randint, choice
from string import ascii_letters
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder, ComplexJsonDecoder
from neuralnetworkcommon.perceptron import Perceptron
from test.service import service
# test perceptron
resource = "/perceptron"
class testPerceptronWS(TestCase):
    # test random generation
    def testRandomGetOk(self):
        # get randomized perceptron
        dimensions, comments = testPerceptronWS.genereteRandomPerceptronParameters()
        response = service.clientApplication.get(resource+"/random",data=dumps({"dimensions": dimensions,"comments":comments}),content_type=service.contentType)
        perceptron = service.loadData(response.data)
        # check perceptron
        self.assertEqual(response.status_code,200,"ERROR : response status does not match")
        self.assertTrue(type(perceptron)==Perceptron,"ERROR : perceptron type does not match")
    # test CRUD OK
    def testCrudOK(self):
        # randomize initial perceptron
        dimensions, comments = testPerceptronWS.genereteRandomPerceptronParameters()
        rawInitialPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        dumpedInitialPerceptron = ComplexJsonEncoder.dumpComplexObject(rawInitialPerceptron)
        # precheck
        self.assertFalse(hasattr(rawInitialPerceptron,"id"),"ERROR : perceptron has id")
        # create perceptron
        response = service.clientApplication.post(resource,data=dumpedInitialPerceptron,content_type=service.contentType)
        perceptronId = int(response.data)
        # check creation
        self.assertIsNotNone(perceptronId,"ERROR : perceptron has no id")
        rawInitialPerceptron.id = perceptronId
        specificResource = "/".join((resource, str(perceptronId),))
        # read perceptron
        response = service.clientApplication.get(specificResource)
        fetchedInsertedPerceptron = service.loadData(response.data)
        # check reading
        self.assertEqual(rawInitialPerceptron,fetchedInsertedPerceptron,"ERROR : inserted perceptron does not match")
        # update perceptron
        dimensions, comments = testPerceptronWS.genereteRandomPerceptronParameters()
        rawNewPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        dumpedNewPerceptron = ComplexJsonEncoder.dumpComplexObject(rawNewPerceptron)
        service.clientApplication.put(specificResource,data=dumpedNewPerceptron,content_type=service.contentType)
        # check update
        response = service.clientApplication.get(specificResource)
        fetchedUpdatedPerceptron = service.loadData(response.data)
        self.assertNotEqual(fetchedUpdatedPerceptron,fetchedInsertedPerceptron,"ERROR : perceptron not updated")
        rawNewPerceptron.id = perceptronId
        self.assertEqual(fetchedUpdatedPerceptron,rawNewPerceptron,"ERROR : updated perceptron does not match")
        # delete perceptron
        service.clientApplication.delete(specificResource)
        # check deletion
        response = service.clientApplication.get(specificResource)
        deletedPerceptron = service.loadData(response.data)
        self.assertIsNone(deletedPerceptron,"ERROR : perceptron not deleted")
        pass
    # utilities
    @classmethod
    def setUpClass(cls):
        service.clientApplication.testing = True
    @staticmethod
    def genereteRandomPerceptronParameters():
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        return dimensions, comments
    pass
pass
