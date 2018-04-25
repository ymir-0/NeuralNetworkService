#!/usr/bin/env python3
# coding=utf-8
# import
from neuralnetworkcommon.trainingSet import TrainingSet, TrainingElement
from test.service import service
from test import commonUtilities
from random import randint
from neuralnetworkservice.service import service as nnservice
from json import loads, dumps
# create bad training set
badTrainingElement = TrainingElement.constructFromAttributes(["a"],[0])
rawBadTrainingSet = TrainingSet.constructFromAttributes(None,[badTrainingElement], "")
jsonTrainingSet = rawBadTrainingSet.jsonMarshall()
dumpedBadTrainingSet = dumps(jsonTrainingSet)
# test training set
resource = "/"+nnservice.endpoint+"/trainingset"
class testTrainingSetWS(service.TestService):
    # test CRUD OK
    def testCrudOK(self):
        # randomize initial training set
        trainingElements, comments = commonUtilities.genereteTrainingSetParameters()
        rawInitialTrainingSet = TrainingSet.constructFromAttributes(None,trainingElements,comments)
        jsonTrainingSet = rawInitialTrainingSet.jsonMarshall()
        dumpedInitialTrainingSet = dumps(jsonTrainingSet)
        # precheck
        self.assertIsNone(rawInitialTrainingSet.id,"ERROR : trainingSet has id")
        # create training set
        response = service.clientApplication.post(resource,data=dumpedInitialTrainingSet,content_type=service.contentType)
        trainingSetId = int(response.data)
        # check creation
        self.assertIsNotNone(trainingSetId,"ERROR : trainingSet has no id")
        rawInitialTrainingSet.id = trainingSetId
        specificResource = "/".join((resource, str(trainingSetId),))
        # read training set
        response = service.clientApplication.get(specificResource)
        jsonTrainingSet = loads(response.data)
        fetchedInsertedTrainingSet = TrainingSet.jsonUnmarshall(**jsonTrainingSet)
        # check reading
        self.assertEqual(rawInitialTrainingSet,fetchedInsertedTrainingSet,"ERROR : inserted trainingSet does not match")
        # update training set
        trainingElements, comments = commonUtilities.genereteTrainingSetParameters()
        rawNewTrainingSet = TrainingSet.constructFromAttributes(None,trainingElements,comments)
        jsonTrainingSet = rawNewTrainingSet.jsonMarshall()
        dumpedNewTrainingSet = dumps(jsonTrainingSet)
        service.clientApplication.put(specificResource,data=dumpedNewTrainingSet,content_type=service.contentType)
        # check update
        response = service.clientApplication.get(specificResource)
        jsonTrainingSet = loads(response.data)
        fetchedUpdatedTrainingSet = TrainingSet.jsonUnmarshall(**jsonTrainingSet)
        self.assertNotEqual(fetchedUpdatedTrainingSet,fetchedInsertedTrainingSet,"ERROR : trainingSet not updated")
        rawNewTrainingSet.id = trainingSetId
        self.assertEqual(fetchedUpdatedTrainingSet,rawNewTrainingSet,"ERROR : updated trainingSet does not match")
        # delete training set
        service.clientApplication.delete(specificResource)
        # check deletion
        response = service.clientApplication.get(specificResource)
        jsonTrainingSet = loads(response.data)
        self.assertIsNone(jsonTrainingSet,"ERROR : trainingSet not deleted")
        pass
    # test select/delete all OK
    def testSelectDeleteAll(self):
        # initialize random training sets
        initialIds=set()
        trainingSetNumber = randint(5, 10)
        for _ in range(trainingSetNumber):
            trainingElements, comments = commonUtilities.genereteTrainingSetParameters()
            rawInitialTrainingSet = TrainingSet.constructFromAttributes(None,trainingElements, comments)
            jsonTrainingSet = rawInitialTrainingSet.jsonMarshall()
            dumpedInitialTrainingSet = dumps(jsonTrainingSet)
            response = service.clientApplication.post(resource, data=dumpedInitialTrainingSet, content_type=service.contentType)
            trainingSetId = int(response.data)
            initialIds.add(trainingSetId)
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
    def testPostError(self):
        response = service.clientApplication.post(resource, data=dumpedBadTrainingSet, content_type=service.contentType)
        service.checkError(self,response)
    def testPutError(self):
        response = service.clientApplication.put("/".join((resource, "0",)), data=dumpedBadTrainingSet, content_type=service.contentType)
        service.checkError(self,response)
    pass
pass
