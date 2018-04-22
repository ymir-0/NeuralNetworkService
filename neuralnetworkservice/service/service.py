# coding=utf-8
# import
from flask import Flask
from flask_restful import Api
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
from neuralnetworkservice.service.perceptron import RandomPerceptron, GlobalPerceptron, SpecificPerceptron
from flask import jsonify
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
def responseError(exception):
    responseError = jsonify(exception.args)
    responseError.status_code = 500
    return responseError
pass
