# coding=utf-8
# import
from neuralnetworkservice.database import database
from neuralnetworkcommon.trainingSet import mergeData, TrainingSet
# training set
class TrainingSetDB():
    # TODO : add a compensation / full rollback system if failure
    @staticmethod
    def insert(trainingSet):
        # insert trainingSet
        statement = "INSERT INTO "+database.schema+".TRAINING_SET (INPUTS,EXPECTED_OUTPUTS,COMMENTS) VALUES (%s,%s,%s) RETURNING ID"
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
        statement = "SELECT INPUTS,EXPECTED_OUTPUTS,COMMENTS FROM "+database.schema+".TRAINING_SET WHERE ID=%s"
        parameters = (id,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement, parameters)
            attributs = cursor.fetchone()
            # convert from decimal to float
            inputs = [[float(__) for __ in _] for _ in attributs[0]]
            expectedOutput = [[float(__) for __ in _] for _ in attributs[1]]
            # create training set if need
            trainingSet = None
            if attributs:
                trainingElements = mergeData(inputs,expectedOutput)
                trainingSet = TrainingSet.constructFromAttributes(id, trainingElements, attributs[2])
        finally:
            cursor.close()
            connection.close()
        return trainingSet
    pass
    @staticmethod
    def update(trainingSet):
        # insert trainingSet
        statement = "UPDATE "+database.schema+".TRAINING_SET SET INPUTS=%s,EXPECTED_OUTPUTS=%s,COMMENTS=%s WHERE ID=%s"
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
    pass
pass

