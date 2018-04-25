# coding=utf-8
# import
from flask import Flask
from flask_restful import Api
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
from neuralnetworkservice.service.perceptron import RandomPerceptron, GlobalPerceptron, SpecificPerceptron
from neuralnetworkservice.service.trainingSet import GlobalTrainingSet, SpecificTrainingSet
from flask import jsonify
import logging
from logging.handlers import RotatingFileHandler
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
API.add_resource(GlobalTrainingSet, "/".join(("",endpoint,"trainingset",)))
API.add_resource(SpecificTrainingSet, "/".join(("",endpoint,"trainingset","<int:trainingSetId>",)))
# set log
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
httpLoggerConfiguration=configuration["http_logger"]
handler = RotatingFileHandler(httpLoggerConfiguration["file"],int(httpLoggerConfiguration["maximumSize"]),int(httpLoggerConfiguration["backupCount"]))
handler.setFormatter(formatter)
application.logger.addHandler(handler)
application.logger.setLevel(configuration["http_logger"]["level"])
log = logging.getLogger("werkzeug")
log.setLevel(configuration["http_logger"]["level"])
log.addHandler(handler)
# utilities
def responseError(exception):
    responseError = jsonify(exception.args)
    responseError.status_code = 500
    return responseError
pass
