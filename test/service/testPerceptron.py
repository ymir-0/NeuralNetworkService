#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from neuralnetworkservice.service.service import application
# test perceptron
class testPerceptronWS(TestCase):
    APPLICATION = application.test_client()
    # test CRUD OK
    def testGlobalGetOk(self):
        #
        result = testPerceptronWS.APPLICATION.get("/perceptron")
        pass
    # utilities
    @staticmethod
    def tearDownClass():
        testPerceptronWS.APPLICATION.testing = True
    pass
pass
