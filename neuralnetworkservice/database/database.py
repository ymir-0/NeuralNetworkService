# coding=utf-8
# import
from psycopg2 import connect
from abc import ABC
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
CONFIGURATION=configurationLoader.loadedConfiguration["database"]
# database
class Database(ABC):
    # static values
    CONNECTION = connect(
        host=CONFIGURATION["host"],
        port=CONFIGURATION["port"],
        dbname=CONFIGURATION["database"],
        user=CONFIGURATION["user"],
        password=CONFIGURATION["password"]
    )
    SCHEMA=password=CONFIGURATION["schema"]
    # close connection
    @staticmethod
    def closeConnection():
        Database.CONNECTION.close()
    pass
pass
