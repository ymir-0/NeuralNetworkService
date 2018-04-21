# coding=utf-8
# import
from psycopg2 import connect
from neuralnetworkcommon.perceptron import Perceptron, Layer
from neuralnetworkservice.database.database import Database
# layer
class LayerDB(Database):
    @staticmethod
    def insertByPerceptronIdAndDepth(perceptronId, depthIndex, layer):
        # cast arrays elements to float
        weights = [[float(__) for __ in _] for _ in layer.weights]
        biases = [float(_) for _ in layer.biases]
        # insert layer
        statement = "INSERT INTO "+Database.SCHEMA+".LAYER (ID_PERCEPTRON,DEPTH_INDEX,WEIGHTS,BIASES) VALUES (%s,%s,%s,%s)"
        parameters = (perceptronId,depthIndex,weights,biases,)
        cursor = Database.CONNECTION.cursor()
        raisedException = None
        try:
            cursor.execute(statement, parameters)
            Database.CONNECTION.commit()
        except Exception as exception :
            Database.CONNECTION.rollback()
            raisedException = exception
        finally:
            cursor.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def selectAllByPerceptronId(perceptronId):
        # initialize layers
        layers=list()
        # select all layers
        statement = "SELECT WEIGHTS,BIASES FROM "+Database.SCHEMA+".LAYER WHERE ID_PERCEPTRON=%s ORDER BY DEPTH_INDEX ASC"
        parameters = (perceptronId,)
        cursor = Database.CONNECTION.cursor()
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
        statement = "DELETE FROM "+Database.SCHEMA+".LAYER WHERE ID_PERCEPTRON=%s"
        parameters = (perceptronId,)
        cursor = Database.CONNECTION.cursor()
        raisedException = None
        try:
            cursor.execute(statement, parameters)
            Database.CONNECTION.commit()
        except Exception as exception :
            Database.CONNECTION.rollback()
            raisedException = exception
        finally:
            cursor.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def deleteAll():
        # delete all layers
        statement = "DELETE FROM "+Database.SCHEMA+".LAYER"
        cursor = Database.CONNECTION.cursor()
        raisedException = None
        try:
            cursor.execute(statement)
            Database.CONNECTION.commit()
        except Exception as exception :
            Database.CONNECTION.rollback()
            raisedException = exception
        finally:
            cursor.close()
            if raisedException : raise raisedException
        pass
    pass
# perceptron
class PerceptronDB(Database):
    # TODO : add a compensation / full rollback system if failure
    @staticmethod
    def insert(perceptron):
        # insert perceptron
        statement = "INSERT INTO "+Database.SCHEMA+".PERCEPTRON (COMMENTS) VALUES (%s) RETURNING ID"
        parameters = (perceptron.comments,)
        cursor = Database.CONNECTION.cursor()
        raisedException = None
        try:
            cursor.execute(statement, parameters)
            id = cursor.fetchone()[0]
            # insert each layer
            for depthIndex, layer in enumerate(perceptron.layers): LayerDB.insertByPerceptronIdAndDepth(id, depthIndex, layer)
            # commit when all is fine
            Database.CONNECTION.commit()
        except Exception as exception :
            Database.CONNECTION.rollback()
            raisedException = exception
        finally:
            cursor.close()
            if raisedException : raise raisedException
        # set perceptron id
        perceptron.id = id
        pass
    @staticmethod
    def selectById(id):
        # select perceptron
        statement = "SELECT COMMENTS FROM "+Database.SCHEMA+".PERCEPTRON WHERE ID=%s"
        parameters = (id,)
        cursor = Database.CONNECTION.cursor()
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
        return perceptron
    @staticmethod
    def update(perceptron):
        cursor = Database.CONNECTION.cursor()
        raisedException = None
        try:
            # update all layers
            LayerDB.updateByPerceptronId(perceptron.id, perceptron.layers)
            # update perceptron
            statement = "UPDATE "+Database.SCHEMA+".PERCEPTRON SET COMMENTS=%s WHERE ID=%s"
            parameters = (perceptron.comments, perceptron.id,)
            cursor.execute(statement, parameters)
            Database.CONNECTION.commit()
        except Exception as exception :
            Database.CONNECTION.rollback()
            raisedException = exception
        finally:
            cursor.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def deleteById(perceptronId):
        cursor = Database.CONNECTION.cursor()
        raisedException = None
        try:
            # delete all layers
            LayerDB.deleteAllByPerceptronId(perceptronId)
            # delete all layers
            statement = "DELETE FROM "+Database.SCHEMA+".PERCEPTRON WHERE ID=%s"
            parameters = (perceptronId,)
            cursor.execute(statement, parameters)
            Database.CONNECTION.commit()
        except Exception as exception:
            Database.CONNECTION.rollback()
            raisedException = exception
        finally:
            cursor.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def selectAllIds():
        # select all ids
        statement = "SELECT ID FROM "+Database.SCHEMA+".PERCEPTRON ORDER BY ID ASC"
        cursor = Database.CONNECTION.cursor()
        try:
            cursor.execute(statement)
            attributs = cursor.fetchall()
        finally:
            cursor.close()
        ids = set([ _[0] for _ in attributs])
        return ids
    @staticmethod
    def deleteAll():
        cursor = Database.CONNECTION.cursor()
        raisedException = None
        try:
            # delete all layers
            LayerDB.deleteAll()
            # delete all perceptron
            statement = "DELETE FROM "+Database.SCHEMA+".PERCEPTRON"
            cursor.execute(statement)
            Database.CONNECTION.commit()
        except Exception as exception:
            Database.CONNECTION.rollback()
            raisedException = exception
        finally:
            cursor.close()
            if raisedException : raise raisedException
    pass
pass
