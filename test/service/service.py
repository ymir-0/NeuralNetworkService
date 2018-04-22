# coding=utf-8
# import
from unittest import TestCase
from neuralnetworkservice.service.service import application
from json import loads
# services test utilities
clientApplication = application.test_client()
contentType = "application/json"
def checkError(testInstance,response):
    testInstance.assertEqual(response.status_code, 500, "ERROR : Status code not expected")
    error = loads(response.data)
    testInstance.assertNotIn("Internal Server Error", error[0], "ERROR : Error message not expected")
class TestService(TestCase):
    @classmethod
    def setUpClass(cls):
        clientApplication.testing = True
    pass
pass
