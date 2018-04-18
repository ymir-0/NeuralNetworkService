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
        statement = "INSERT INTO neuronnetwork.PERCEPTRON (COMMENTS) VALUES (%s) RETURNING ID"
        parameters = (perceptron.comments,)
        cursor = connection.cursor()
        cursor.execute(statement, parameters)
        id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        perceptron.id = id
        pass
    pass
pass
