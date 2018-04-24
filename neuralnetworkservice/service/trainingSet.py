# coding=utf-8
# import
from flask_restful import Resource
from flask import request
from neuralnetworkcommon.trainingSet import TrainingSet
from neuralnetworkservice.database.trainingSet import TrainingSetDB
from neuralnetworkservice.service import service
# global trainingSet resource
class GlobalTrainingSet(Resource):
    # create a trainingSet
    def post(self):
        # parse parameters
        dictTrainingSet = request.get_json()
        service.application.logger.info(dictTrainingSet)
        # insert trainingSet
        response = None
        try:
            trainingSet = TrainingSet.jsonUnmarshall(**dictTrainingSet)
            TrainingSetDB.insert(trainingSet)
            response = trainingSet.id
            service.application.logger.info(response)
        except Exception as exception:
            response = service.responseError(exception)
            service.application.logger.error(exception)
        finally:
            return response
    pass
    # get all trainingSets IDs
    def get(self):
        rawTrainingSetIds = TrainingSetDB.selectAllIds()
        loadedTrainingSetIds = list(rawTrainingSetIds)
        service.application.logger.info(loadedTrainingSetIds)
        return loadedTrainingSetIds
    # delete a trainingSet
    def delete(self):
        TrainingSetDB.deleteAll()
    pass
# specific trainingSet resource
class SpecificTrainingSet(Resource):
    # select a trainingSet
    def get(self,trainingSetId):
        service.application.logger.info(trainingSetId)
        rawTrainingSet = TrainingSetDB.selectById(trainingSetId)
        jsonTrainingSet = None
        if rawTrainingSet:
            jsonTrainingSet = rawTrainingSet.jsonMarshall()
        # return
        service.application.logger.info(jsonTrainingSet)
        return jsonTrainingSet
    # update a trainingSet
    '''
    INFO : we request an explicit trainingSet id because :
     - we update only recorded trainingSet, meaning having an ID
     - we can overwrite a recorded trainingSet from another one
    '''
    def put(self,trainingSetId):
        service.application.logger.info(trainingSetId)
        # parse parameters
        dictTrainingSet = request.get_json()
        service.application.logger.info(dictTrainingSet)
        # insert trainingSet
        response = None
        try:
            trainingSet = TrainingSet.jsonUnmarshall(**dictTrainingSet)
            trainingSet.id = trainingSetId
            TrainingSetDB.update(trainingSet)
            service.application.logger.info(response)
        except Exception as exception:
            response = service.responseError(exception)
            service.application.logger.error(exception)
        finally:
            return response
        pass
    # delete a trainingSet
    def delete(self,trainingSetId):
        service.application.logger.info(trainingSetId)
        TrainingSetDB.deleteById(trainingSetId)
    pass
pass
