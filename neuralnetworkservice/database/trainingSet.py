# coding=utf-8
# import
from neuralnetworkservice.database import database
from neuralnetworkcommon.trainingSet import mergeData, TrainingSet
# training set
class TrainingSetDB():
    TABLE=database.schema+".TRAINING_SET"
    @staticmethod
    def insert(trainingSet):
        # insert trainingSet
        statement = "INSERT INTO "+TrainingSetDB.TABLE+" (INPUTS,EXPECTED_OUTPUTS,COMMENTS) VALUES (%s,%s,%s) RETURNING ID"
        inputs, expectedOutputs = trainingSet.separateData()
        parameters = (inputs, expectedOutputs, trainingSet.comments,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            cursor.execute(statement, parameters)
            connection.commit()
            id = cursor.fetchone()[0]
            trainingSet.id = id
        except Exception as exception :
            connection.rollback()
            raisedException = exception
        finally:
            cursor.close()
            connection.close()
            if raisedException : raise raisedException
        pass
    @staticmethod
    def selectById(id):
        # select perceptron
        statement = "SELECT INPUTS,EXPECTED_OUTPUTS,COMMENTS FROM "+TrainingSetDB.TABLE+" WHERE ID=%s"
        parameters = (id,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement, parameters)
            attributs = cursor.fetchone()
            # create training set if need
            trainingSet = None
            if attributs:
                inputs = [[float(__) for __ in _] for _ in attributs[0]]
                expectedOutput = [[float(__) for __ in _] for _ in attributs[1]]
                trainingElements = mergeData(inputs,expectedOutput)
                trainingSet = TrainingSet.constructFromAttributes(id, trainingElements, attributs[2])
        finally:
            cursor.close()
            connection.close()
        return trainingSet
    @staticmethod
    def update(trainingSet):
        # insert trainingSet
        statement = "UPDATE "+TrainingSetDB.TABLE+" SET INPUTS=%s,EXPECTED_OUTPUTS=%s,COMMENTS=%s WHERE ID=%s"
        inputs, expectedOutputs = trainingSet.separateData()
        parameters = (inputs, expectedOutputs, trainingSet.comments, trainingSet.id,)
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
    def deleteById(id):
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            # delete all layers
            statement = "DELETE FROM "+TrainingSetDB.TABLE+" WHERE ID=%s"
            parameters = (id,)
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
        statement = "SELECT ID FROM "+TrainingSetDB.TABLE+" ORDER BY ID ASC"
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement)
            attributs = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
        ids = [ _[0] for _ in attributs]
        return ids
    @staticmethod
    def deleteAll():
        connection = database.connectDatabase()
        cursor = connection.cursor()
        raisedException = None
        try:
            # delete all perceptron
            statement = "DELETE FROM "+TrainingSetDB.TABLE
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

