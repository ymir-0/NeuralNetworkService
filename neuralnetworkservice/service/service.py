#!/usr/bin/env python3
# coding=utf-8
# import
from flask import Flask
from flask_restful import Resource, Api
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
# global perceptron resource
class PerceptronWS(Resource):
    def get(self):
        return {'hello': 'world'}
    pass
# contants
CURRENT_DIRECTORY = realpath(__file__).rsplit(sep, 1)[0]
CONFIGURATION_FILE=join(CURRENT_DIRECTORY,"..","conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(CONFIGURATION_FILE)
CONFIGURATION=configurationLoader.loadedConfiguration["service"]
# initialize service
application = Flask(CONFIGURATION["endpoint"])
API = Api(application)
API.add_resource(PerceptronWS, '/perceptron')
if __name__ == '__main__':
    application.run(CONFIGURATION["host"],int(CONFIGURATION["port"]))
pass
