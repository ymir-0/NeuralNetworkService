#!/usr/bin/env python3
# coding=utf-8
# import
from neuralnetworkcommon.perceptron import Perceptron
from test.service import service
from test import commonUtilities
from random import randint
from neuralnetworkservice.service import service as nnservice
from json import loads, dumps
# create bad perceptron
rawBadPerceptron = Perceptron.constructRandomFromDimensions([1, 1], "")
rawBadPerceptron.layers[0].weights[0][0] = ""
jsonPerceptron = rawBadPerceptron.jsonMarshall()
dumpedBadPerceptron = dumps(jsonPerceptron)
# test perceptron
resource = "/"+nnservice.endpoint+"/perceptron"
class testPerceptronWS(service.TestService):
    # test random generation
    def testRandomPostOk(self):
        # get randomized perceptron
        dimensions, comments = commonUtilities.genereteRandomPerceptronParameters()
        response = service.clientApplication.post("/".join((resource, "random",)),data=dumps({"dimensions": dimensions,"comments":comments}),content_type=service.contentType)
        jsonPerceptron = loads(response.data)
        perceptron = Perceptron.jsonUnmarshall(**jsonPerceptron)
        # check perceptron
        self.assertEqual(response.status_code,200,"ERROR : response status does not match")
        self.assertTrue(type(perceptron)==Perceptron,"ERROR : perceptron type does not match")
    # test CRUD OK
    def testCrudOK(self):
        # randomize initial perceptron
        dimensions, comments = commonUtilities.genereteRandomPerceptronParameters()
        rawInitialPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        jsonPerceptron = rawInitialPerceptron.jsonMarshall()
        dumpedInitialPerceptron = dumps(jsonPerceptron)
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
        jsonPerceptron = loads(response.data)
        fetchedInsertedPerceptron = Perceptron.jsonUnmarshall(**jsonPerceptron)
        # check reading
        self.assertEqual(rawInitialPerceptron,fetchedInsertedPerceptron,"ERROR : inserted perceptron does not match")
        # update perceptron
        dimensions, comments = commonUtilities.genereteRandomPerceptronParameters()
        rawNewPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        jsonPerceptron = rawNewPerceptron.jsonMarshall()
        dumpedNewPerceptron = dumps(jsonPerceptron)
        service.clientApplication.put(specificResource,data=dumpedNewPerceptron,content_type=service.contentType)
        # check update
        response = service.clientApplication.get(specificResource)
        jsonPerceptron = loads(response.data)
        fetchedUpdatedPerceptron = Perceptron.jsonUnmarshall(**jsonPerceptron)
        self.assertNotEqual(fetchedUpdatedPerceptron,fetchedInsertedPerceptron,"ERROR : perceptron not updated")
        rawNewPerceptron.id = perceptronId
        self.assertEqual(fetchedUpdatedPerceptron,rawNewPerceptron,"ERROR : updated perceptron does not match")
        # delete perceptron
        service.clientApplication.delete(specificResource)
        # check deletion
        response = service.clientApplication.get(specificResource)
        jsonPerceptron = loads(response.data)
        self.assertIsNone(jsonPerceptron,"ERROR : perceptron not deleted")
        pass
    # test select/delete all OK
    def testSelectDeleteAll(self):
        # initialize random perceptrons
        initialIds=set()
        perceptronNumber = randint(5, 10)
        for _ in range(perceptronNumber):
            dimensions, comments = commonUtilities.genereteRandomPerceptronParameters()
            rawInitialPerceptron = Perceptron.constructRandomFromDimensions(dimensions, comments)
            jsonPerceptron = rawInitialPerceptron.jsonMarshall()
            dumpedInitialPerceptron = dumps(jsonPerceptron)
            response = service.clientApplication.post(resource, data=dumpedInitialPerceptron, content_type=service.contentType)
            perceptronId = int(response.data)
            initialIds.add(perceptronId)
        # select IDs
        response = service.clientApplication.get(resource)
        fetchedIds = loads(response.data)
        # check IDs
        self.assertTrue(initialIds.issubset(fetchedIds),"ERROR : IDs selection does not match")
        # delete all
        service.clientApplication.delete(resource)
        # check IDs
        response = service.clientApplication.get(resource)
        deletedIds = loads(response.data)
        self.assertEqual(len(deletedIds),0,"ERROR : complete deletion failed")
        pass
    # test error
    def testRandomPostError(self):
        response = service.clientApplication.post("/".join((resource, "random",)), data=dumpedBadPerceptron, content_type=service.contentType)
        service.checkError(self,response)
    def testPostError(self):
        response = service.clientApplication.post(resource, data=dumpedBadPerceptron, content_type=service.contentType)
        service.checkError(self,response)
    def testPutError(self):
        response = service.clientApplication.put("/".join((resource, "0",)), data=dumpedBadPerceptron, content_type=service.contentType)
        service.checkError(self,response)
    pass
pass
