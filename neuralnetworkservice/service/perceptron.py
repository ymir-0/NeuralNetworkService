# coding=utf-8
# import
from flask_restful import Resource
from flask import request
from neuralnetworkcommon.perceptron import Perceptron
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder, ComplexJsonDecoder
from json import loads, dumps
from neuralnetworkservice.database.perceptron import PerceptronDB
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
        dumpedPerceptron = ComplexJsonEncoder.dumpComplexObject(rawPerceptron)
        # INFO : it is important to load to avoid embedded string
        loadedPerceptron = loads(dumpedPerceptron)
        # return
        return loadedPerceptron
# global perceptron resource
class GlobalPerceptron(Resource):
    # create a perceptron
    def post(self):
        # parse parameters
        loadedPerceptron = request.get_json()
        # INFO : it is important to dumps to have requested string type
        dumpedPerceptron = dumps(loadedPerceptron)
        rawPerceptron = ComplexJsonDecoder.loadComplexObject(dumpedPerceptron)
        # insert perceptron
        PerceptronDB.insert(rawPerceptron)
        # return
        return rawPerceptron.id
    pass
    # get all perceptrons IDs
    def get(self):
        return {'hello': 'world'}
    pass
# specific perceptron resource
class SpecificPerceptron(Resource):
    # select a perceptron
    def get(self,perceptronId):
        rawPerceptron = PerceptronDB.selectById(perceptronId)
        dumpedPerceptron = ComplexJsonEncoder.dumpComplexObject(rawPerceptron)
        # INFO : it is important to load to avoid embedded string
        loadedPerceptron = loads(dumpedPerceptron)
        # return
        return loadedPerceptron
    pass
pass