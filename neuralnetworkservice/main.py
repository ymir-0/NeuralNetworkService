#!/usr/bin/env python3
# coding=utf-8
# import
from neuralnetworkservice.service import service
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
# contants
CURRENT_DIRECTORY = realpath(__file__).rsplit(sep, 1)[0]
CONFIGURATION_FILE=join(CURRENT_DIRECTORY,"conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(CONFIGURATION_FILE)
CONFIGURATION=configurationLoader.loadedConfiguration["service"]
# start service
if __name__ == "__main__":
    service.application.run(CONFIGURATION["host"],int(CONFIGURATION["port"]))
pass
