# coding=utf-8
# import
from psycopg2 import connect
from abc import ABC
# database
'''
INFO : I do not use any other SQL library such as
 - python-sql to construct SQL statement
 - SQLAlchemy for object mapping
because it can complexify code without any benefits at this moment
'''
class Database(ABC):
    # static values
    CONNECTION = connect(host="yggdrasil", port="5433", dbname="neuronnetwork", user="neuronnetwork", password="neuronnetwork")
    # close connection
    @staticmethod
    def closeConnection():
        Database.CONNECTION.close()
    pass
pass
