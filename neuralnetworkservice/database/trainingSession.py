# coding=utf-8
# import
from neuralnetworkservice.database import database
from neuralnetworkcommon.utils import mergeData
from neuralnetworkcommon.trainingSession import TrainingSession
# training session
class TrainingSessionDB():
    TABLE=database.schema+".TRAINING_SESSION"
    @staticmethod
    def insert(trainingSession):
        # insert trainingSession
        statement = "INSERT INTO "+TrainingSessionDB.TABLE+" (PERCEPTRON_ID,TRAINING_SET_ID,TRAINING_INPUTS,TRAINING_EXPECTED_OUTPUTS,TEST_INPUTS,TEST_EXPECTED_OUTPUTS,COMMENTS) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        trainingInputs, trainingExpectedOutputs, testInputs, testExpectedOutputs = trainingSession.separateData()
        parameters = (trainingSession.perceptronId, trainingSession.trainingSessionId, trainingInputs, trainingExpectedOutputs,testInputs, testExpectedOutputs,trainingSession.comments,)
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
    def selectByPerceptronId(perceptronId):
        # select perceptron
        statement = "SELECT TRAINING_SET_ID,TRAINING_INPUTS,TRAINING_EXPECTED_OUTPUTS,TEST_INPUTS,TEST_EXPECTED_OUTPUTS,STATUS,PID,MEAN_DIFFERENTIAL_ERRORS,TRAINED_ELEMENTS_NUMBERS,ERROR_ELEMENTS_NUMBERS,COMMENTS FROM "+TrainingSessionDB.TABLE+" WHERE PERCEPTRON_ID=%s"
        parameters = (perceptronId,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement, parameters)
            attributs = cursor.fetchone()
            # create training set if need
            trainingSession = None
            if attributs:
                trainingInputs = [[float(__) for __ in _] for _ in attributs[1]]
                trainingExpectedOutput = [[float(__) for __ in _] for _ in attributs[2]]
                trainingSet = mergeData(trainingInputs,trainingExpectedOutput)
                testInputs = [[float(__) for __ in _] for _ in attributs[3]]
                testExpectedOutput = [[float(__) for __ in _] for _ in attributs[4]]
                testSet = mergeData(testInputs,testExpectedOutput)
                trainingSession = TrainingSession.constructFromAttributes(perceptronId,attributs[0],trainingSet,testSet,attributs[5],attributs[6],attributs[7],attributs[8],attributs[9],attributs[10])
        finally:
            cursor.close()
            connection.close()
        return trainingSession
    pass
pass
