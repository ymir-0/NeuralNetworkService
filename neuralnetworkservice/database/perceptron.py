# coding=utf-8
# import
from psycopg2 import connect
from neuralnetworkcommon.perceptron import Perceptron, Layer
from neuralnetworkservice.database import database
# layer
class LayerDB():
    @staticmethod
    def insertByPerceptronIdAndDepth(perceptronId, depthIndex, layer):
        # cast arrays elements to float
        weights = [[float(__) for __ in _] for _ in layer.weights]
        biases = [float(_) for _ in layer.biases]
        # insert layer
        statement = "INSERT INTO "+database.schema+".LAYER (ID_PERCEPTRON,DEPTH_INDEX,WEIGHTS,BIASES) VALUES (%s,%s,%s,%s)"
        parameters = (perceptronId,depthIndex,weights,biases,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            cursor.execute(statement, parameters)
            connection.commit()
        except Exception as exception :
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def selectAllByPerceptronId(perceptronId):
        # initialize layers
        layers=list()
        # select all layers
        statement = "SELECT WEIGHTS,BIASES FROM "+database.schema+".LAYER WHERE ID_PERCEPTRON=%s ORDER BY DEPTH_INDEX ASC"
        parameters = (perceptronId,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement, parameters)
            # construct each layer
            for attribut in cursor:
                # def insert current layer
                weights = [[float(__) for __ in _] for _ in attribut[0]]
                biases = [float(_) for _ in attribut[1]]
                layer=Layer.constructFromAttributes(weights,biases)
                # fill layers
                layers.append(layer)
        finally:
            cursor.close()
            connection.close()
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
        statement = "DELETE FROM "+database.schema+".LAYER WHERE ID_PERCEPTRON=%s"
        parameters = (perceptronId,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            cursor.execute(statement, parameters)
            connection.commit()
        except Exception as exception :
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def deleteAll():
        # delete all layers
        statement = "DELETE FROM "+database.schema+".LAYER"
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            cursor.execute(statement)
            connection.commit()
        except Exception as exception :
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
        pass
    pass
# perceptron
class PerceptronDB():
    # TODO : add a compensation / full rollback system if failure
    @staticmethod
    def insert(perceptron):
        # insert perceptron
        statement = "INSERT INTO "+database.schema+".PERCEPTRON (COMMENTS) VALUES (%s) RETURNING ID"
        parameters = (perceptron.comments,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            cursor.execute(statement, parameters)
            connection.commit()
            id = cursor.fetchone()[0]
            # insert each layer
            for depthIndex, layer in enumerate(perceptron.layers): LayerDB.insertByPerceptronIdAndDepth(id, depthIndex, layer)
            # commit when all is fine
        except Exception as exception :
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
        # set perceptron id
        perceptron.id = id
        pass
    @staticmethod
    def selectById(id):
        # select perceptron
        statement = "SELECT COMMENTS FROM "+database.schema+".PERCEPTRON WHERE ID=%s"
        parameters = (id,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement, parameters)
            attributs = cursor.fetchone()
            # create perceptron if need
            perceptron = None
            if attributs:
                # select layers
                layers=LayerDB.selectAllByPerceptronId(id)
                # construct & return perceptron
                perceptron = Perceptron.constructFromAttributes(id,layers,attributs[0])
        finally:
            cursor.close()
            connection.close()
        return perceptron
    @staticmethod
    def update(perceptron):
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            # update all layers
            LayerDB.updateByPerceptronId(perceptron.id, perceptron.layers)
            # update perceptron
            statement = "UPDATE "+database.schema+".PERCEPTRON SET COMMENTS=%s WHERE ID=%s"
            parameters = (perceptron.comments, perceptron.id,)
            cursor.execute(statement, parameters)
            connection.commit()
        except Exception as exception :
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def deleteById(perceptronId):
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            # delete all layers
            LayerDB.deleteAllByPerceptronId(perceptronId)
            # delete all layers
            statement = "DELETE FROM "+database.schema+".PERCEPTRON WHERE ID=%s"
            parameters = (perceptronId,)
            cursor.execute(statement, parameters)
            connection.commit()
        except Exception as exception:
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def selectAllIds():
        # select all ids
        statement = "SELECT ID FROM "+database.schema+".PERCEPTRON ORDER BY ID ASC"
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement)
            attributs = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
        ids = set([ _[0] for _ in attributs])
        return ids
    @staticmethod
    def deleteAll():
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            # delete all layers
            LayerDB.deleteAll()
            # delete all perceptron
            statement = "DELETE FROM "+database.schema+".PERCEPTRON"
            cursor.execute(statement)
            connection.commit()
        except Exception as exception:
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
    pass
pass
