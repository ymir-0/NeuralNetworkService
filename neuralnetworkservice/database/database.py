# coding=utf-8
# import
from psycopg2 import connect
from pythoncommontools.configurationLoader import configurationLoader
from os import sep
from os.path import join, realpath
# database
'''
INFO : I do not use any other SQL library such as
 - python-sql to construct SQL statement
 - SQLAlchemy for object mapping
because it can complexify code without any benefits at this moment
'''
# contants
CURRENT_DIRECTORY = realpath(__file__).rsplit(sep, 1)[0]
CONFIGURATION_FILE=join(CURRENT_DIRECTORY,"..","conf","neuralnetworkservice.conf")
# load configuration
configurationLoader.loadConfiguration(CONFIGURATION_FILE)
configuration=configurationLoader.loadedConfiguration["database"]
schema = configuration["schema"]
# connect
def connectDatabase():
    connection = connect(
        host=configuration["host"],
        port=configuration["port"],
        dbname=configuration["database"],
        user=configuration["user"],
        password=configuration["password"]
    )
    return connection
pass
