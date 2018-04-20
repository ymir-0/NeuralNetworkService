# coding=utf-8
# import
from flask import Flask
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
#
parser = RequestParser()
parser.add_argument('name', type=str, help='Test')
# global perceptron resource
class GlobalPerceptron(Resource):
    # generate a random perceptron
    def post(self):
        args = parser.parse_args()
        return {'hello': 'world ' + args["name"]}
    # get all perceptrons IDs
    #def get(self):
    #    args = RequestParser().parse_args()
    #    return {'hello': 'world ' + args["name"]}
    pass
