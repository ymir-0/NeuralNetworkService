# coding=utf-8
__version__ = '0.0.0'
# import
import psycopg2
# constants
connection = psycopg2.connect(host="yggdrasil", port="5433", dbname="neuronnetwork", user="neuronnetwork", password="")
# perceptron
class PerceptronDB():
    @staticmethod
    def create(perceptron):
        statement = "INSERT INTO neuronnetwork.PERCEPTRON (COMMENTS) VALUES (%s)"
        parameters = (perceptron.comments,)
        cursor = connection.cursor()
        result = cursor.execute(statement, parameters)
        connection.commit()
        cursor.close()
        pass
    pass
pass