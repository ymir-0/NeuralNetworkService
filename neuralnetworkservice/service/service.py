# coding=utf-8
# import
from flask import Flask
from flask_restful import Api
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
from neuralnetworkservice.service.perceptron import RandomPerceptron, GlobalPerceptron, SpecificPerceptron
from flask import jsonify
import logging
# contants
currentDirectory = realpath(__file__).rsplit(sep, 1)[0]
configurationFile=join(currentDirectory,"..","conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(configurationFile)
configuration=configurationLoader.loadedConfiguration
# initialize service
application = Flask(__name__)
API = Api(application)
endpoint=configuration["service"]["endpoint"]
API.add_resource(RandomPerceptron, "/".join(("",endpoint,"perceptron","random",)))
API.add_resource(GlobalPerceptron, "/".join(("",endpoint,"perceptron",)))
API.add_resource(SpecificPerceptron, "/".join(("",endpoint,"perceptron","<int:perceptronId>",)))
# set log
handler = logging.FileHandler(configuration["http_logger"]["file"])
handler.setLevel(configuration["http_logger"]["level"])
application.logger.addHandler(handler)
log = logging.getLogger("werkzeug")
log.setLevel(configuration["http_logger"]["level"])
log.addHandler(handler)
# utilities
def responseError(exception):
    responseError = jsonify(exception.args)
    responseError.status_code = 500
    return responseError
pass
