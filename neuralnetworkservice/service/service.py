# coding=utf-8
# import
from flask import Flask
from flask_restful import Api
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
from neuralnetworkservice.service.perceptron import RandomPerceptron, GlobalPerceptron, SpecificPerceptron
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonEncoder, ComplexJsonDecoder
from json import loads, dumps
from flask import request, jsonify
# contants
CURRENT_DIRECTORY = realpath(__file__).rsplit(sep, 1)[0]
CONFIGURATION_FILE=join(CURRENT_DIRECTORY,"..","conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(CONFIGURATION_FILE)
CONFIGURATION=configurationLoader.loadedConfiguration["service"]
# initialize service
application = Flask(__name__)
API = Api(application)
endpoint=CONFIGURATION["endpoint"]
API.add_resource(RandomPerceptron, "/".join(("",endpoint,"perceptron","random",)))
API.add_resource(GlobalPerceptron, "/".join(("",endpoint,"perceptron",)))
API.add_resource(SpecificPerceptron, "/".join(("",endpoint,"perceptron","<int:perceptronId>",)))
# utilities
def dumpObject(rawObject):
    dumpedObject = ComplexJsonEncoder.dumpComplexObject(rawObject)
    # INFO : it is important to load to avoid embedded string
    loadedObject = loads(dumpedObject)
    return loadedObject
def loadObject(request):
    loadedObject = request.get_json()
    # INFO : it is important to dumps to have requested string type
    dumpedObject = dumps(loadedObject)
    rawObject = ComplexJsonDecoder.loadComplexObject(dumpedObject)
    return rawObject
def responseError(exception):
    responseError = jsonify(exception.args)
    responseError.status_code = 500
    return responseError
pass
