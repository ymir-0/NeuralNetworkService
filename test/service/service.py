# coding=utf-8
# import
from unittest import TestCase
from neuralnetworkservice.service.service import application
from pythoncommontools.jsonEncoderDecoder.complexJsonEncoderDecoder import ComplexJsonDecoder
# services test utilities
clientApplication = application.test_client()
contentType = "application/json"
def loadData(data):
    decodedData = data.decode().strip()
    loadedObject = ComplexJsonDecoder.loadComplexObject(decodedData)
    return loadedObject
    pass
class TestService(TestCase):
    @classmethod
    def setUpClass(cls):
        clientApplication.testing = True
    pass
pass
