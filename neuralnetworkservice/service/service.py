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
# contants
CURRENT_DIRECTORY = realpath(__file__).rsplit(sep, 1)[0]
CONFIGURATION_FILE=join(CURRENT_DIRECTORY,"..","conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(CONFIGURATION_FILE)
CONFIGURATION=configurationLoader.loadedConfiguration["service"]
# initialize service
application = Flask(CONFIGURATION["endpoint"])
API = Api(application)
API.add_resource(RandomPerceptron, "/perceptron/random")
API.add_resource(GlobalPerceptron, "/perceptron")
API.add_resource(SpecificPerceptron, "/perceptron/<int:perceptronId>")
# utilities
def dumpObject(rawObject):
    dumpedObject = ComplexJsonEncoder.dumpComplexObject(rawObject)
    # INFO : it is important to load to avoid embedded string
    loadedObject = loads(dumpedObject)
    return loadedObject
def loadObject(loadedObject):
    # INFO : it is important to dumps to have requested string type
    dumpedObject = dumps(loadedObject)
    rawObject = ComplexJsonDecoder.loadComplexObject(dumpedObject)
    return rawObject
pass
