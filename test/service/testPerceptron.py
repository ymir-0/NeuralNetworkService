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
        kw = {"name": "ymir"}
        result = testPerceptronWS.APPLICATION.post("/perceptron",data={"name": "ymir"})
        pass
    # utilities
    @classmethod
    def setUpClass(cls):
        testPerceptronWS.APPLICATION.testing = True
    pass
pass
