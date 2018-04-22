#!/usr/bin/env python3
# coding=utf-8
# import
from neuralnetworkservice.service import service
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
# contants
currentDirectory = realpath(__file__).rsplit(sep, 1)[0]
configurationFile=join(currentDirectory,"conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(configurationFile)
configuration=configurationLoader.loadedConfiguration["service"]
# start service
if __name__ == "__main__":
    service.application.run(configuration["host"],int(configuration["port"]),debug=configuration.getboolean(configuration["debug"]))
pass
