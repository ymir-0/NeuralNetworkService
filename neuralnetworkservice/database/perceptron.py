# coding=utf-8
__version__ = '0.0.0'
# import
from psycopg2 import connect
from neuralnetworkcommon.perceptron import Perceptron
# constants
connection = connect(host="yggdrasil", port="5433", dbname="neuronnetwork", user="neuronnetwork", password="neuronnetwork")
# perceptron
class PerceptronDB():
    @staticmethod
    def create(perceptron):
        statement = "INSERT INTO neuronnetwork.PERCEPTRON (COMMENTS) VALUES (%s) RETURNING ID"
        parameters = (perceptron.comments,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        perceptron.id = id
        pass
    @staticmethod
    def getById(id):
        statement = "SELECT ID, COMMENTS FROM neuronnetwork.PERCEPTRON WHERE ID=%s"
        cur = connection.cursor()
        cur.execute(statement, (id,))
        attributs = cur.fetchone()
        cur.close()
        perceptron = Perceptron.constructFromAttributes(id=attributs[0],comments=attributs[1])
        return perceptron
    pass
pass
# TODO : insert/select layer and use in perceptron
