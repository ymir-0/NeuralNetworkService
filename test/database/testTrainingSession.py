#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from test import commonUtilities
from random import random, randint
from string import ascii_letters
from random import choice
from neuralnetworkservice.database.perceptron import PerceptronDB
from neuralnetworkservice.database.trainingSet import TrainingSetDB
from neuralnetworkservice.database.trainingSession import TrainingSessionDB
from neuralnetworkcommon.trainingSession import TrainingSession
# test training session
class testTrainingSessionDB(TestCase):
    # test CRUD OK
    def testCrudOK(self):
        # initialize random perceptron & training set
        perceptron = commonUtilities.randomPerceptron()
        PerceptronDB.insert(perceptron)
        trainingSet = commonUtilities.randomTrainingSet()
        TrainingSetDB.insert(trainingSet)
        # initialize random training session
        initialComments = "".join([choice(ascii_letters) for _ in range(15)])
        initialTrainingSession = TrainingSession.constructFromTrainingSet(perceptron.id,trainingSet,random(),initialComments)
        # call DB insert
        TrainingSessionDB.insert(initialTrainingSession)
        # call DB select by id
        fetchedInsertedTrainingSession = TrainingSessionDB.selectByPerceptronId(perceptron.id)
        expectedInsertedTrainingSession = TrainingSession.constructFromAttributes(perceptron.id,trainingSet.id,initialTrainingSession.trainingSet,initialTrainingSession.testSet,"INITIALIZED",None,None,None,None,initialComments)
        # check DB select by id
        self.assertEqual(expectedInsertedTrainingSession,fetchedInsertedTrainingSession,"ERROR : inserted trainingSession does not match")
        # call DB update report
        meanDifferantialError = (random()-.5)*10
        trainedElementsNumber = randint(1,10)
        errorElementsNumber = randint(1,10)
        TrainingSessionDB.updateReport(perceptron.id, meanDifferantialError, trainedElementsNumber, errorElementsNumber)
        # check DB update report
        fetchedUpdatedReport = TrainingSessionDB.selectByPerceptronId(perceptron.id)
        self.assertListEqual(fetchedUpdatedReport.meanDifferantialErrors,[meanDifferantialError],"ERROR : meanDifferantialError does not match")
        self.assertListEqual(fetchedUpdatedReport.trainedElementsNumbers,[trainedElementsNumber],"ERROR : trainedElementsNumber does not match")
        self.assertListEqual(fetchedUpdatedReport.errorElementsNumbers,[errorElementsNumber],"ERROR : errorElementsNumber does not match")
        # call DB update status
        status = "".join([choice(ascii_letters) for _ in range(11)])
        pid = randint(1,1e3)
        TrainingSessionDB.updateStatus(perceptron.id,status,pid)
        # check DB update status
        fetchedUpdatedStatus = TrainingSessionDB.selectByPerceptronId(perceptron.id)
        self.assertEqual(fetchedUpdatedStatus.status,status,"ERROR : status does not match")
        self.assertEqual(fetchedUpdatedStatus.pid,pid,"ERROR : PID does not match")
        # call DB update comments
        updatedComments = "".join([choice(ascii_letters) for _ in range(15)])
        TrainingSessionDB.updateComments(perceptron.id,updatedComments)
        # check DB update comments
        fetchedUpdatedComments = TrainingSessionDB.selectByPerceptronId(perceptron.id)
        self.assertEqual(fetchedUpdatedComments.comments,updatedComments,"ERROR : comments does not match")
        # call DB delete
        TrainingSessionDB.deleteById(perceptron.id)
        # check DB delete
        deletedTrainingSession = TrainingSessionDB.selectByPerceptronId(perceptron.id)
        self.assertIsNone(deletedTrainingSession,"ERROR : trainingSet not deleted")
        pass
    # test select/delete all OK
    def testSelectDeleteAll(self):
        # initialize random training sessions
        initialIds=set()
        trainingSessionNumber = randint(5, 10)
        for _ in range(trainingSessionNumber):
            # initialize random perceptron & training set
            perceptron = commonUtilities.randomPerceptron()
            PerceptronDB.insert(perceptron)
            trainingSet = commonUtilities.randomTrainingSet()
            TrainingSetDB.insert(trainingSet)
            # initialize random training session
            initialComments = "".join([choice(ascii_letters) for _ in range(15)])
            trainingSession = TrainingSession.constructFromTrainingSet(perceptron.id, trainingSet, random(), initialComments)
            TrainingSessionDB.insert(trainingSession)
            initialIds.add(perceptron.id)
            pass
        # select IDs
        fetchedIds = TrainingSessionDB.selectAllIds()
        # check IDs
        self.assertTrue(initialIds.issubset(fetchedIds),"ERROR : IDs selection does not match")
        # delete all
        TrainingSessionDB.deleteAll()
        # check IDs
        deletedIds = TrainingSessionDB.selectAllIds()
        self.assertEqual(len(deletedIds),0,"ERROR : complete deletion failed")
        pass
    pass
pass
