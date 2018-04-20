#!/usr/bin/env python3
# coding=utf-8
# import
from flask import Flask
from flask_restful import Api
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
from neuralnetworkservice.service.perceptron import GlobalPerceptron
# contants
CURRENT_DIRECTORY = realpath(__file__).rsplit(sep, 1)[0]
CONFIGURATION_FILE=join(CURRENT_DIRECTORY,"..","conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(CONFIGURATION_FILE)
CONFIGURATION=configurationLoader.loadedConfiguration["service"]
# initialize service
application = Flask(CONFIGURATION["endpoint"])
API = Api(application)
API.add_resource(GlobalPerceptron, '/perceptron')
if __name__ == '__main__':
    application.run(CONFIGURATION["host"],int(CONFIGURATION["port"]))
pass
