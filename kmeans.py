from __future__ import division
from scipy.io import loadmat
import numpy
import numpy as np
from scipy.ndimage import imread
import matplotlib.pyplot as plt


class KMeans(object):
    def __init__(self, k, trainImages, imSize, maxIter=10):
        self.k = k
        self.trainImages = trainImages
        self.imSize = imSize
        self.maxIter = maxIter
        self.means = [self.randomMean() for i in range(k)]

    def randomMean(self):
        return np.array([np.random.uniform(feat[0],feat[1]) for feat in self.imSize])

    def dist(self, x, y):
        return np.linalg.norm(x - y)

    def cluster(self):
        for p in xrange(self.maxIter):
            place = [[] for p in range(self.k)]
            for i in range(len(self.trainImages)):
                x = self.trainImages[i]
                cluster = min(range(self.k),key=lambda m:self.dist(x,self.means[m]))
                place[cluster] += [i]
            for k in range(self.k):
                if len(place[k]) > 0:
                    self.means[k] = sum(map(lambda i: self.trainImages[i], place[k]))/float(len(place[k]))
                else:
                    self.means[k] = self.randomMean()
        return place


vectors = [[1 if i == label else 0 for i in xrange(10)] for label in xrange(10)]

def reshaping(images):
    return images.reshape(images.shape[0] * images.shape[1], images.shape[2])

def toImg(vector, size, ind=None):
    if ind is None:
        ind = range(len(vector))
    img = numpy.zeros(size)
    img.put(ind, vector)
    return img

def label_to_vector(yl):
    return vectors[yl]

if __name__ == "__main__":
    images = loadmat('mnist_data/images.mat')
    trainImages = reshaping(images['images']).T
    trainImages = trainImages/255
    imSize = zip(np.amin(trainImages, axis=0), np.amax(trainImages, axis=0))
    kmeans = KMeans(20, trainImages, imSize, maxIter=10)
    kmeans.cluster()
    for i, mean in enumerate(kmeans.means):
        img = toImg(mean, (28,28))
        plt.imshow(img)
        plt.savefig("20_kmean_%d.png" % (i))
