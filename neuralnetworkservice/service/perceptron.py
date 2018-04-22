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
        dimensions = parameters["dimensions"]
        comments = parameters["comments"]
        # generate & format random perceptron
        rawPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        jsonPerceptron = rawPerceptron.jsonMarshall()
        # return
        return jsonPerceptron
# global perceptron resource
class GlobalPerceptron(Resource):
    # create a perceptron
    def post(self):
        # parse parameters
        dictPerceptron = request.get_json()
        # insert perceptron
        response = None
        try:
            perceptron = Perceptron.jsonUnmarshall(**dictPerceptron)
            PerceptronDB.insert(perceptron)
            response = perceptron.id
        except Exception as exception:
            response = service.responseError(exception)
        finally:
            return response
    pass
    # get all perceptrons IDs
    def get(self):
        rawPerceptronIds = PerceptronDB.selectAllIds()
        loadedPerceptronIds = list(rawPerceptronIds)
        return loadedPerceptronIds
    # delete a perceptron
    def delete(self):
        PerceptronDB.deleteAll()
    pass
# specific perceptron resource
class SpecificPerceptron(Resource):
    # select a perceptron
    def get(self,perceptronId):
        rawPerceptron = PerceptronDB.selectById(perceptronId)
        jsonPerceptron = None
        if rawPerceptron:
            jsonPerceptron = rawPerceptron.jsonMarshall()
        # return
        return jsonPerceptron
    # update a perceptron
    '''
    INFO : we request an explicit perceptron id because :
     - we update only recorded perceptron, meaning having an ID
     - we can overwrite a recorded perceptron from another one
    '''
    def put(self,perceptronId):
        # parse parameters
        dictPerceptron = request.get_json()
        # insert perceptron
        response = None
        try:
            perceptron = Perceptron.jsonUnmarshall(**dictPerceptron)
            perceptron.id = perceptronId
            PerceptronDB.update(perceptron)
        except Exception as exception:
            response = service.responseError(exception)
        finally:
            return response
        pass
    # delete a perceptron
    def delete(self,perceptronId):
        PerceptronDB.deleteById(perceptronId)
    pass
pass
