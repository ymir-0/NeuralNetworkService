# coding=utf-8
# import
from psycopg2 import connect
from abc import ABC
# database
class Database(ABC):
    # static values
    CONNECTION = connect(host="yggdrasil", port="5433", dbname="neuronnetwork", user="neuronnetwork", password="neuronnetwork")
    pass
pass
