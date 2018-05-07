#!/usr/bin/env python3
# coding=utf-8
# import
from random import randint
from neuralnetworkcommon.perceptron import Layer
from neuralnetworkservice.database.perceptron import PerceptronDB, LayerDB
from unittest import TestCase
from test import commonUtilities
# test perceptron
class testPerceptronDB(TestCase):
    # test CRUD OK
    def testCrudOK(self):
        # initialize random perceptron
        initialPerceptron = commonUtilities.randomPerceptron()
        # precheck
        self.assertFalse(hasattr(initialPerceptron,"id"),"ERROR : perceptron has id")
        # call DB insert
        PerceptronDB.insert(initialPerceptron)
        # check DB insert
        self.assertTrue(hasattr(initialPerceptron,"id"),"ERROR : perceptron has no id")
        # call DB select by id
        fetchedInsertedPerceptron = PerceptronDB.selectById(initialPerceptron.id)
        # check DB select by id
        self.assertEqual(initialPerceptron,fetchedInsertedPerceptron,"ERROR : inserted perceptron does not match")
        # call DB update
        newPerceptron = commonUtilities.randomPerceptron()
        newPerceptron.id = initialPerceptron.id
        PerceptronDB.update(newPerceptron)
        # check DB update
        fetchedUpdatedPerceptron = PerceptronDB.selectById(initialPerceptron.id)
        self.assertNotEqual(fetchedUpdatedPerceptron,fetchedInsertedPerceptron,"ERROR : perceptron not updated")
        self.assertEqual(fetchedUpdatedPerceptron,newPerceptron,"ERROR : updated perceptron does not match")
        # call DB delete
        PerceptronDB.deleteById(initialPerceptron.id)
        # check DB delete
        deletedPerceptron = PerceptronDB.selectById(initialPerceptron.id)
        self.assertIsNone(deletedPerceptron,"ERROR : perceptron not deleted")
        pass
    # test select/delete all OK
    def testSelectDeleteAll(self):
        # initialize random perceptrons
        initialIds=set()
        perceptronNumber = randint(5, 10)
        for _ in range(perceptronNumber):
            perceptron = commonUtilities.randomPerceptron()
            PerceptronDB.insert(perceptron)
            initialIds.add(perceptron.id)
            pass
        # select IDs
        fetchedIds = PerceptronDB.selectAllIds()
        # check IDs
        self.assertTrue(initialIds.issubset(fetchedIds),"ERROR : IDs selection does not match")
        # delete all
        PerceptronDB.deleteAll()
        # check IDs
        deletedIds = PerceptronDB.selectAllIds()
        self.assertEqual(len(deletedIds),0,"ERROR : complete deletion failed")
        pass
    # test layer error
    def testLayerInsertByPerceptronIdAndDepthError(self):
        try:
            LayerDB.insertByPerceptronIdAndDepth("", 0, Layer(0,0))
            raise Exception("ERROR : Exception not raised")
        except Exception as exception: self.assertIsNotNone(exception,"ERROR : Exception not raised")
    def testLayerSelectAllByPerceptronIdError(self):
        try:
            LayerDB.selectAllByPerceptronId("")
            raise Exception("ERROR : Exception not raised")
        except Exception as exception: self.assertIsNotNone(exception,"ERROR : Exception not raised")
    def testLayerDeleteAllByPerceptronIdError(self):
        try:
            LayerDB.deleteAllByPerceptronId("")
            raise Exception("ERROR : Exception not raised")
        except Exception as exception: self.assertIsNotNone(exception,"ERROR : Exception not raised")
    # test perceptron error
    def testPerceptronInsertError(self):
        try:
            PerceptronDB.insert("")
            raise Exception("ERROR : Exception not raised")
        except Exception as exception: self.assertIsNotNone(exception,"ERROR : Exception not raised")
    def testPerceptronSelectByIdError(self):
        try:
            PerceptronDB.selectById("")
            raise Exception("ERROR : Exception not raised")
        except Exception as exception: self.assertIsNotNone(exception,"ERROR : Exception not raised")
    def testPerceptronUpdateError(self):
        try:
            PerceptronDB.update("")
            raise Exception("ERROR : Exception not raised")
        except Exception as exception: self.assertIsNotNone(exception,"ERROR : Exception not raised")
    def testPerceptronDeleteByIdError(self):
        try:
            PerceptronDB.deleteById("")
            raise Exception("ERROR : Exception not raised")
        except Exception as exception: self.assertIsNotNone(exception,"ERROR : Exception not raised")
    pass
pass
