# coding=utf-8
# import
from flask_restful import Resource
from flask import request
from neuralnetworkcommon.perceptron import Perceptron
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder
from json import loads
# random perceptron resource
class RandomPerceptron(Resource):
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
    pass
    # get all perceptrons IDs
    def get(self):
        return {'hello': 'world'}
    pass
# specific perceptron resource
class SpecificPerceptron(Resource):
    # select a perceptron
    def get(self):
        return {'hello': 'world'}
    pass
pass