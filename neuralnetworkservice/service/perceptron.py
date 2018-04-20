# coding=utf-8
# import
from flask import Flask
from flask_restful import Resource
# global perceptron resource
class GlobalPerceptron(Resource):
    def get(self):
        return {'hello': 'world'}
    pass
