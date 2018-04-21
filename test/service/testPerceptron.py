#!/usr/bin/env python3
# coding=utf-8
# import
from json import dumps
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder
from neuralnetworkcommon.perceptron import Perceptron
from test.service import service
from test import commonUtilities
# test perceptron
resource = "/perceptron"
class testPerceptronWS(service.TestService):
    # test random generation
    def testRandomGetOk(self):
        # get randomized perceptron
        dimensions, comments = commonUtilities.genereteRandomPerceptronParameters()
        response = service.clientApplication.get("/".join((resource, "random",)),data=dumps({"dimensions": dimensions,"comments":comments}),content_type=service.contentType)
        perceptron = service.loadData(response.data)
        # check perceptron
        self.assertEqual(response.status_code,200,"ERROR : response status does not match")
        self.assertTrue(type(perceptron)==Perceptron,"ERROR : perceptron type does not match")
    # test CRUD OK
    def testCrudOK(self):
        # randomize initial perceptron
        dimensions, comments = commonUtilities.genereteRandomPerceptronParameters()
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
        dimensions, comments = commonUtilities.genereteRandomPerceptronParameters()
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
    pass
pass
