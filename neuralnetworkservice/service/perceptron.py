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
    def get(self):
        # parse parameters
        parameters = request.get_json()
        dimensions = parameters["dimensions"]
        comments = parameters["comments"]
        # generate & format random perceptron
        rawPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        loadedPerceptron = service.dumpObject(rawPerceptron)
        # return
        return loadedPerceptron
# global perceptron resource
class GlobalPerceptron(Resource):
    # create a perceptron
    def post(self):
        # parse parameters
        loadedPerceptron = request.get_json()
        rawPerceptron = service.loadObject(loadedPerceptron)
        # insert perceptron
        PerceptronDB.insert(rawPerceptron)
        # return
        return rawPerceptron.id
    pass
    # get all perceptrons IDs
    def get(self):
        rawPerceptronIds = PerceptronDB.selectAllIds()
        loadedPerceptronIds = service.dumpObject(rawPerceptronIds)
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
        loadedPerceptron = service.dumpObject(rawPerceptron)
        # return
        return loadedPerceptron
    # update a perceptron
    '''
    INFO : we request an explicit perceptron id because :
     - we update only recorded perceptron, meaning having an ID
     - we can overwrite a recorded perceptron from another one
    '''
    def put(self,perceptronId):
        # parse parameters
        loadedPerceptron = request.get_json()
        rawPerceptron = service.loadObject(loadedPerceptron)
        # set explicit ID
        rawPerceptron.id = perceptronId
        # insert perceptron
        PerceptronDB.update(rawPerceptron)
    # delete a perceptron
    def delete(self,perceptronId):
        PerceptronDB.deleteById(perceptronId)
    pass
pass
