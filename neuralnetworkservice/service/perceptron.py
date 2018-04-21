# coding=utf-8
# import
from flask_restful import Resource
from flask import request
from neuralnetworkcommon.perceptron import Perceptron
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder
from json import loads
# global perceptron resource
class GlobalPerceptron(Resource):
    # generate a random perceptron
    def post(self):
        # parse parameters
        json_data = request.get_json()
        dimensions = json_data["dimensions"]
        comments = json_data["comments"]
        # generate & format random perceptron
        rawPerceptron = Perceptron.constructRandomFromDimensions(dimensions,comments)
        dumpedPerceptron = ComplexJsonEncoder.dumpComplexObject(rawPerceptron)
        # INFO : it is important to load to avoid embedded string
        loadedPerceptron = loads(dumpedPerceptron)
        # return
        return loadedPerceptron
    # get all perceptrons IDs
    #def get(self):
    #    args = RequestParser().parse_args()
    #    return {'hello': 'world ' + args["name"]}
    pass
