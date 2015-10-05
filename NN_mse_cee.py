from __future__ import division

from collections import namedtuple
import numpy as np

#Che Yeon Hyun
#23836036


TrainingItem = namedtuple("TrainingItem", "x0, y, yl")
TestItem = namedtuple("TestItem", "x0")




def flatten_digit_data(images):
    return images.reshape(images.shape[0] * images.shape[1], images.shape[2])

def convert_input():
    from scipy.io import loadmat
    import numpy as np
    from numpy import save
    test_mat = loadmat('digit-dataset/test.mat')
    test_images = flatten_digit_data(test_mat['test_images']).T
    train_mat = loadmat('digit-dataset/train.mat')
    train_images = flatten_digit_data(train_mat['train_images']).T
    train_labels = train_mat['train_labels'].ravel()
    np.save('digit-dataset/train.x.npy', train_images)
    np.save('digit-dataset/train.y.npy', train_labels)
    np.save('digit-dataset/test.x.npy', test_images)

def load_trains():
    import numpy as np
    from random import shuffle
    from numpy import matrix
    xs = matrix(np.load('digit-dataset/train.x.npy'))/255
    yls = np.load('digit-dataset/train.y.npy')
    items = [TrainingItem(x, label_to_vector(yl), yl) for (x, yl) in zip(xs, yls)]
    shuffle(items)
    return items

def load_tests():
    import numpy as np
    from numpy import matrix
    xs = matrix(np.load('digit-dataset/test.x.npy'))/255
    return [TestItem(x) for x in xs]

def vector_to_label(yv):
    from numpy import argmax
    return argmax(yv)

vectors = [
    [1 if i == label else 0 for i in xrange(10)]
    for label in xrange(10)
]

def label_to_vector(yl):
    return vectors[yl]



def kaggle():
    from hw6code import Neural_Network
    import random
    import csv
    np.random.seed(12)
    random.seed(13)
    trains = load_trains()
    tests = load_tests()
    nnet = Neural_Network()
    nnet.train(trains)

    count = 1
    print("WRITING")
    with open('hw6submit.csv', 'w') as f:
        digitwriter = csv.writer(f, delimiter = ',')
        digitwriter.writerow(['Id', 'Category'])
        for test in tests:
            hv = nnet.predict(test)
            hl = vector_to_label(hv)
            digitwriter.writerow([count, hl])
            count +=1

mselist= list()
ceelist = list()

def training_accuracy():
    from hw6code import Neural_Network, ERROR_CEE, ERROR_MSE
    import random
    np.random.seed(12)
    random.seed(13)
    data = load_trains()
    nnet = Neural_Network(error_function=ERROR_CEE)
    nnet.train(data)
    total = 0
    correct = 0
    for test in data:
        hw = nnet.predict(test)
        hj = vector_to_label(hw)
        if hj == test.yl:
            correct += 1
        total += 1
    print correct/total


def mse_accuracy():
    from hw6code import ERROR_MSE, Neural_Network
    import random
    np.random.seed(12)
    random.seed(13)
    data = load_trains()
    trains = data[:-10000]
    tests = data[-5000:]
    nnet = Neural_Network(error_function = ERROR_MSE)
    nnet.progressive_init(trains)
    def get_accuracy():
        total = 0
        correct = 0
        for test in tests:
            hw = nnet.predict(test)
            hj = vector_to_label(hw)
            if hj == test.yl:
                correct += 1
            total += 1
        return correct/total
    for reps_goal in xrange(0, 300000, 1000):
        nnet.reps = reps_goal
        nnet.prog_train()
        accuracy = get_accuracy()
        print reps_goal, accuracy
        mselist.append(accuracy)

def cee_accuracy():
    from hw6code import ERROR_CEE, Neural_Network
    import random
    np.random.seed(12)
    random.seed(13)
    data = load_trains()
    trains = data[:-10000]
    tests = data[-5000:]
    nnetc = Neural_Network(error_function = ERROR_CEE)
    nnetc.progressive_init(trains)
    def get_accuracy():
        total = 0
        correct = 0
        for test in tests:
            hw = nnetc.predict(test)
            hj = vector_to_label(hw)
            if hj == test.yl:
                correct += 1
            total += 1
        return correct/total
    for reps_goal in xrange(0, 300000, 1000):
        nnetc.reps = reps_goal
        nnetc.prog_train()
        accuracyc = get_accuracy()
        print reps_goal, accuracyc
        ceelist.append(accuracyc)

def plot_stuff(amse, acee):
    import matplotlib.pyplot as plt
    print np.shape(amse), np.shape(acee)
    plt.plot(range(len(acee)), acee, "r", label = "CEE Accuracy")
    plt.plot(range(len(amse)), amse, "k", label = "MSE Accuracy")
    plt.title("Accuracy of MSE & CEE per 1000 Iterations")
    plt.xlabel("iterations (1000)")
    plt.ylabel("Accuracy")
    plt.legend(loc='lower right')
    plt.xscale('log')
    plt.show()
