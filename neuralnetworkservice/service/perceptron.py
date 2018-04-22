# coding=utf-8
# import
from flask_restful import Resource
from flask import request
from neuralnetworkcommon.perceptron import Perceptron
from neuralnetworkservice.database.perceptron import PerceptronDB
from neuralnetworkservice.service import service
# random perceptron resource
class RandomPerceptron(Resource):
    # TODO : delete or make optionnal the comments
    def post(self):
        # parse parameters
        parameters = request.get_json()
        service.application.logger.info(parameters)
        # generate & format random perceptron
        response = None
        try:
            dimensions = parameters["dimensions"]
            comments = parameters["comments"]
            rawPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
            response = rawPerceptron.jsonMarshall()
            service.application.logger.info(response)
        except Exception as exception:
            response = service.responseError(exception)
            service.application.logger.error(exception)
        finally:
            return response
# global perceptron resource
class GlobalPerceptron(Resource):
    # create a perceptron
    def post(self):
        # parse parameters
        dictPerceptron = request.get_json()
        service.application.logger.info(dictPerceptron)
        # insert perceptron
        response = None
        try:
            perceptron = Perceptron.jsonUnmarshall(**dictPerceptron)
            PerceptronDB.insert(perceptron)
            response = perceptron.id
            service.application.logger.info(response)
        except Exception as exception:
            response = service.responseError(exception)
            service.application.logger.error(exception)
        finally:
            return response
    pass
    # get all perceptrons IDs
    def get(self):
        rawPerceptronIds = PerceptronDB.selectAllIds()
        loadedPerceptronIds = list(rawPerceptronIds)
        service.application.logger.info(loadedPerceptronIds)
        return loadedPerceptronIds
    # delete a perceptron
    def delete(self):
        PerceptronDB.deleteAll()
    pass
# specific perceptron resource
class SpecificPerceptron(Resource):
    # select a perceptron
    def get(self,perceptronId):
        service.application.logger.info(perceptronId)
        rawPerceptron = PerceptronDB.selectById(perceptronId)
        jsonPerceptron = None
        if rawPerceptron:
            jsonPerceptron = rawPerceptron.jsonMarshall()
        # return
        service.application.logger.info(jsonPerceptron)
        return jsonPerceptron
    # update a perceptron
    '''
    INFO : we request an explicit perceptron id because :
     - we update only recorded perceptron, meaning having an ID
     - we can overwrite a recorded perceptron from another one
    '''
    def put(self,perceptronId):
        service.application.logger.info(perceptronId)
        # parse parameters
        dictPerceptron = request.get_json()
        service.application.logger.info(dictPerceptron)
        # insert perceptron
        response = None
        try:
            perceptron = Perceptron.jsonUnmarshall(**dictPerceptron)
            perceptron.id = perceptronId
            PerceptronDB.update(perceptron)
            service.application.logger.info(response)
        except Exception as exception:
            response = service.responseError(exception)
            service.application.logger.error(exception)
        finally:
            return response
        pass
    # delete a perceptron
    def delete(self,perceptronId):
        service.application.logger.info(perceptronId)
        PerceptronDB.deleteById(perceptronId)
    pass
pass
