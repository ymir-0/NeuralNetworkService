# coding=utf-8
# import
from neuralnetworkcommon.perceptron import TrainingElement
from neuralnetworkservice.database import database
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
    pass
pass

