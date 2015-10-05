from __future__ import division
##Che Yeon Hyun
##23836036
#### Libraries
# Standard library
import random
import sys
from collections import namedtuple
from math import log
import csv
import random

# Third-party libraries
import numpy as np


ForwardVar = namedtuple("ForwardVar", "x0, x0p, x1, x1p, x2")
TestItem = namedtuple("TestItem", "x0")
TrainingItem = namedtuple("TrainingItem", "x0, y")

ERROR_MSE = "mse"
ERROR_CEE = "cee"


def augment(x):
    from numpy import matrix, insert
    assert x.shape[0] == 1
    return insert(x, x.shape[1], 1)

def deaugment(xp):
    from numpy import matrix, delete
    return delete(xp, -1)

def multiply(*matrices):
    from numpy import multiply
    return reduce(multiply, matrices)



#### Main Network class
class Neural_Network(object):
    def __init__(self, reps = 500000, rate = 0.01, error_function = ERROR_CEE):
        self.inputLayerSize = 784
        self.outputLayerSize = 10
        self.hiddenLayerSize = 200
        self.reps = reps
        self.rate = rate
        self.error_function = error_function

        self.w1p = np.matrix(np.random.uniform(low = -0.01, high = 0.01, size = (self.inputLayerSize+1,self.hiddenLayerSize)))
        self.w2p = np.matrix(np.random.uniform(low = -0.1, high = 0.1, size = (self.hiddenLayerSize+1,self.outputLayerSize)))

    def forward(self, x0):
        """Return the output of the network if ``a`` is input."""
        from numpy import tanh
        x0p = augment(x0)
        x1 = tanh(x0p*self.w1p)
        x1p = augment(x1)
        x2 = sigmoid(x1p*self.w2p)
        return ForwardVar(x0=x0, x0p=x0p, x1=x1, x1p=x1p, x2=x2)

    # z2 = np.dot(X, W1)
    # a2 = sigmoid(z2)
    # z3 = np.dot(a2, W2)
    # yHat = sigmoid(z3) 
    # return yHat

    def backprop(self, y, forward_vars):
        import numpy as np
        from numpy import square
        x0, x0p, x1, x1p, x2 = forward_vars
        if self.error_function is ERROR_MSE:
            d2 = multiply(x2,(1-x2),(x2-y))
        elif self.error_function is ERROR_CEE:
            d2 = (x2-y)
        else:
            raise ValueError
        self.w2p -= self.rate *  x1p.T * d2
        d1= multiply((1- square(x1)), deaugment(np.dot(self.w2p, d2.T).T))
        self.w1p -= self.rate * x0p.T * d1


    def predict(self, test):
        return self.forward(test.x0).x2

    def train(self, trains):
        from random import choice
        for rep in xrange(self.reps):
            train = choice(trains)
            forward_vars = self.forward(train.x0)
            self.backprop(train.y, forward_vars)
            if (rep % 1000 == 0):
                print(rep)

    def progressive_init(self, trains):
        self.trains = trains
        self.rep = 0

    def prog_train(self):
        from random import choice
        while self.rep <= self.reps:
            train = choice(self.trains)
            forward_vars = self.forward(train.x0)
            self.backprop(train.y, forward_vars)
            self.rep += 1


def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))


def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))
