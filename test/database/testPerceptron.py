#!/usr/bin/env python3
# coding=utf-8
# import
from unittest import TestCase
from random import randint, choice
from string import ascii_letters
from neuralnetworkcommon.perceptron import Perceptron
from neuralnetworkservice.database.perceptron import PerceptronDB
# test perceptron
class testPerceptronDB(TestCase):
    # test CRUD OK
    def testCrudOK(self):
        # initialize random perceptron
        layersNumber = randint(2,12)
        dimensions = [randint(2,100) for _ in range(layersNumber)]
        comments = "".join([choice(ascii_letters) for _ in range(15)])
        initialPerceptron = Perceptron(dimensions,comments)
        # precheck
        self.assertFalse(hasattr(initialPerceptron,"id"),"ERROR : perceptron has id")
        # call DB create
        PerceptronDB.create(initialPerceptron)
        # check DB create
        self.assertTrue(hasattr(initialPerceptron,"id"),"ERROR : perceptron has no id")
        # call DB get by id
        fetchedPerceptron = PerceptronDB.getById(initialPerceptron.id)
        self.assertEqual(initialPerceptron,fetchedPerceptron,"ERROR : perceptron are different")
        pass
    pass
pass
