# coding=utf-8
__version__ = '0.0.0'
# import
from psycopg2 import connect
from neuralnetworkcommon.perceptron import Perceptron
# constants
connection = connect(host="yggdrasil", port="5433", dbname="neuronnetwork", user="neuronnetwork", password="neuronnetwork")
# layer
class LayerDB():
    @staticmethod
    def create(idPerceptron, depthIndex, layer):
        # cast arrays elements to float
        biases = [float(_) for _ in layer.biases]
        weights = [[float(__) for __ in _] for _ in layer.weights]
        # insert layer
        statement = "INSERT INTO neuronnetwork.LAYER (ID_PERCEPTRON,DEPTH_INDEX,WEIGHTS,BIASES) VALUES (%s,%s,%s,%s)"
        parameters = (idPerceptron,depthIndex,weights,biases,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        connection.commit()
        cursor.close()
        pass
    pass
# perceptron
class PerceptronDB():
    # TODO : add a compensation / full rollback system if failure
    @staticmethod
    def create(perceptron):
        # insert perceptron
        statement = "INSERT INTO neuronnetwork.PERCEPTRON (COMMENTS) VALUES (%s) RETURNING ID"
        parameters = (perceptron.comments,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        # insert each layer
        for depthIndex, layer in enumerate(perceptron.layers):
            LayerDB.create(id, depthIndex, layer)
            pass
        # set perceptron id
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
