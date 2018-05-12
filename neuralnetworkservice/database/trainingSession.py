# coding=utf-8
# import
from neuralnetworkservice.database import database
from neuralnetworkcommon.trainingElement import mergeData
from neuralnetworkcommon.trainingSession import TrainingSession
# training session
class TrainingSessionDB():
    TABLE=database.schema+".TRAINING_SESSION"
    @staticmethod
    def insert(trainingSession):
        # insert trainingSession
        statement = "INSERT INTO "+TrainingSessionDB.TABLE+" (PERCEPTRON_ID,TRAINING_SET_ID,TRAINING_CHUNK_SIZE,TRAINING_INPUTS,TRAINING_EXPECTED_OUTPUTS,TEST_INPUTS,TEST_EXPECTED_OUTPUTS,COMMENTS) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        trainingInputs, trainingExpectedOutputs, testInputs, testExpectedOutputs = trainingSession.separateData()
        parameters = (trainingSession.perceptronId, trainingSession.trainingSessionId, trainingSession.trainingChunkSize, trainingInputs, trainingExpectedOutputs,testInputs, testExpectedOutputs,trainingSession.comments,)
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
        statement = "SELECT TRAINING_SET_ID,TRAINING_CHUNK_SIZE,TRAINING_INPUTS,TRAINING_EXPECTED_OUTPUTS,TEST_INPUTS,TEST_EXPECTED_OUTPUTS,STATUS,PID,MEAN_DIFFERENTIAL_ERRORS,TRAINED_ELEMENTS_NUMBERS,ERROR_ELEMENTS_NUMBERS,COMMENTS FROM "+TrainingSessionDB.TABLE+" WHERE PERCEPTRON_ID=%s"
        parameters = (perceptronId,)
        connection = database.connectDatabase()
        cursor = connection.cursor()
        try:
            cursor.execute(statement, parameters)
            attributs = cursor.fetchone()
            # create training set if need
            trainingSession = None
            if attributs:
                trainingInputs = [[float(__) for __ in _] for _ in attributs[2]]
                trainingExpectedOutput = [[float(__) for __ in _] for _ in attributs[3]]
                trainingSet = mergeData(trainingInputs,trainingExpectedOutput)
                testInputs = [[float(__) for __ in _] for _ in attributs[4]]
                testExpectedOutput = [[float(__) for __ in _] for _ in attributs[5]]
                meanDifferentialErrors = [float(_) for _ in attributs[8]] if attributs[8] is not None else None
                testSet = mergeData(testInputs,testExpectedOutput)
                trainingSession = TrainingSession.constructFromAttributes(perceptronId,attributs[0],attributs[1],trainingSet,testSet,attributs[6],attributs[7],meanDifferentialErrors,attributs[9],attributs[10],attributs[11])
        finally:
            cursor.close()
            connection.close()
        return trainingSession
    @staticmethod
    def updateReport(perceptronId,meanDifferentialError,trainedElementsNumber,errorElementsNumber):
        # update report
        statement = "UPDATE "+TrainingSessionDB.TABLE+" SET MEAN_DIFFERENTIAL_ERRORS=MEAN_DIFFERENTIAL_ERRORS||%s,TRAINED_ELEMENTS_NUMBERS=TRAINED_ELEMENTS_NUMBERS||%s,ERROR_ELEMENTS_NUMBERS=ERROR_ELEMENTS_NUMBERS||%s WHERE PERCEPTRON_ID=%s"
        parameters = (meanDifferentialError,trainedElementsNumber,errorElementsNumber,perceptronId,)
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
    def updateStatus(perceptronId,status,pid):
        # update status
        statement = "UPDATE "+TrainingSessionDB.TABLE+" SET STATUS=%s,PID=%s WHERE PERCEPTRON_ID=%s"
        parameters = (status,pid,perceptronId,)
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
    def updateUserDetails(perceptronId,trainingChunkSize,comments):
        # update status
        statement = "UPDATE "+TrainingSessionDB.TABLE+" SET TRAINING_CHUNK_SIZE=%s,COMMENTS=%s WHERE PERCEPTRON_ID=%s"
        parameters = (trainingChunkSize,comments,perceptronId,)
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
            statement = "DELETE FROM "+TrainingSessionDB.TABLE+" WHERE PERCEPTRON_ID=%s"
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
        statement = "SELECT PERCEPTRON_ID FROM "+TrainingSessionDB.TABLE+" ORDER BY PERCEPTRON_ID ASC"
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
            statement = "DELETE FROM "+TrainingSessionDB.TABLE
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
