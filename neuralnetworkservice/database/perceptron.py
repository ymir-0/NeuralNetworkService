# coding=utf-8
__version__ = '0.0.0'
# import
from psycopg2 import connect
from neuralnetworkcommon.perceptron import Perceptron, Layer
# constants
connection = connect(host="yggdrasil", port="5433", dbname="neuronnetwork", user="neuronnetwork", password="neuronnetwork")
# layer
class LayerDB():
    @staticmethod
    def insertByPerceptronIdAndDepth(perceptronId, depthIndex, layer):
        # cast arrays elements to float
        weights = [[float(__) for __ in _] for _ in layer.weights]
        biases = [float(_) for _ in layer.biases]
        # insert layer
        statement = "INSERT INTO neuronnetwork.LAYER (ID_PERCEPTRON,DEPTH_INDEX,WEIGHTS,BIASES) VALUES (%s,%s,%s,%s)"
        parameters = (perceptronId,depthIndex,weights,biases,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        connection.commit()
        cursor.close()
        pass
    @staticmethod
    def selectAllByPerceptronId(perceptronId):
        # initialize layers
        layers=list()
        # select all layers
        statement = "SELECT WEIGHTS,BIASES FROM neuronnetwork.LAYER WHERE ID_PERCEPTRON=%s ORDER BY DEPTH_INDEX ASC"
        parameters = (perceptronId,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        # construct each layer
        for attribut in cursor:
            # def insert current layer
            weights = [[float(__) for __ in _] for _ in attribut[0]]
            biases = [float(_) for _ in attribut[1]]
            layer=Layer.constructFromAttributes(weights,biases)
            # fill layers
            layers.append(layer)
        # close cursor
        cursor.close()
        # return
        return layers
    @staticmethod
    def updateByPerceptronId(perceptronId, layers):
        # delete all layers
        # INFO : we do not want any old layers to remains if there is less layers
        LayerDB.deleteAllByPerceptronId(perceptronId)
        # insert each layer
        for depthIndex, layer in enumerate(layers): LayerDB.insertByPerceptronIdAndDepth(perceptronId, depthIndex, layer)
    @staticmethod
    def deleteAllByPerceptronId(perceptronId):
        # delete all layers
        statement = "DELETE FROM neuronnetwork.LAYER WHERE ID_PERCEPTRON=%s"
        parameters = (perceptronId,)
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
    def insert(perceptron):
        # insert perceptron
        statement = "INSERT INTO neuronnetwork.PERCEPTRON (COMMENTS) VALUES (%s) RETURNING ID"
        parameters = (perceptron.comments,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        # insert each layer
        for depthIndex, layer in enumerate(perceptron.layers): LayerDB.insertByPerceptronIdAndDepth(id, depthIndex, layer)
        # set perceptron id
        perceptron.id = id
        pass
    @staticmethod
    def selectById(id):
        # select perceptron
        statement = "SELECT ID, COMMENTS FROM neuronnetwork.PERCEPTRON WHERE ID=%s"
        parameters = (id,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        attributs = cursor.fetchone()
        cursor.close()
        # select layers
        layers=LayerDB.selectAllByPerceptronId(id)
        # construct & return perceptron
        perceptron = Perceptron.constructFromAttributes(attributs[0],layers,attributs[1])
        return perceptron
    @staticmethod
    def update(perceptron):
        # update all layers
        LayerDB.updateByPerceptronId(perceptron.id, perceptron.layers)
        # update perceptron
        statement = "UPDATE neuronnetwork.PERCEPTRON SET COMMENTS=%s WHERE ID=%s"
        parameters = (perceptron.comments,perceptron.id,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        connection.commit()
        cursor.close()
        pass
    pass
pass
