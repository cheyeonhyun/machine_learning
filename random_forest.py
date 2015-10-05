from __future__ import division
import scipy.io
from random import randrange
from collections import Counter
from collections import namedtuple
from scipy.io import loadmat
from math import log
import csv
import np as np

spam = loadmat('spam-dataset/spam_data.mat')
trains_features = spam['training_data']
trains_label = spam['training_labels'][0]
tests_features = spam['test_data']

feat_size = len(trains_features[1])
max_depth = 12

class theSet(object):
  x = None
  label = None
  def __init__(self, x, label):
    self.x = x
    self.label = label

class TreeNode(object):
  feature = -1
  dire = -1
  threshold = ""
  left, right = None, None
  def __init__(self, feature, dire, threshold, left, right):
    self.feature = feature
    self.dire = dire
    self.threshold = threshold
    self.left = left
    self.right = right


def calc_impurity(S):
  if len(S.label) == 0:
    return 0
  n0 = 0
  for label in S.label:
    if label == 0:
      n0 = n0 + 1
  P = n0/len(S.label)
  NP = 1-P
  if P == 0.0 or P == 1.0:
    return 0
  return -1 * P * log(P) + -1 * (NP) * log(NP)

def sample(sSet, n):
  size = len(sSet.x)
  l_sample = list()
  sample_size = size
  for i in range(n):
    S_feature = np.zeros(shape = (sample_size, feat_size))
    S_label = np.zeros(shape = (sample_size, 1))
    for j in range(sample_size):
      rand_index = randrange(0, size)
      S_feature[j] = sSet.feature[rand_index]
      S_label[j] = sSet.label[rand_index]
    l_sample.append(theSet(S_feature, S_label))
  return l_sample


def themean(Sset,a):
  n0, n1, mean0, mean1 = 0, 0, 0, 0
  for i in range(len(Sset.x)):
    if Sset.label[i] == 0:
      mean0 = mean0 + Sset.x[i][a]
      n0 = n0 + 1
    else:
      mean1 = mean1 + Sset.x[i][a]
      n1 = n1 + 1
  mean0 = mean0 /n0
  mean1 = mean1 /n1
  if mean0 <= mean1:
    return ((mean0 + mean1)/2, 0)
  else:
    return ((mean0 + mean1)/2, 1)  

def split_set(Sset, k):
  mean = themean(Sset,k)
  const = mean[0]
  dire = mean[1]
  if dire == 0:
    Z_ind = np.where(Sset.x[:,k] <= const)[0]
    One_ind = np.where(Sset.x[:,k] > const)[0]
  else:
    Z_ind = np.where(Sset.x[:,k] >= const)[0]
    One_ind = np.where(Sset.x[:,k] < const)[0]
  Sset_0feat = np.delete(Sset.x, One_ind, 0)
  Sset_0label = np.delete(Sset.label, One_ind)
  Sset_1feat = np.delete(Sset.x, Z_ind, 0)
  Sset_1label = np.delete(Sset.label, Z_ind)
  return (theSet(Sset_0feat, Sset_0label), theSet(Sset_1feat, Sset_1label))

def best_split(S,depth):
  best_info = 0
  best_j = -1
  ent = calc_impurity(S)
  for j in range(feat_size):
    sets = split_set(S,j)
    ent_0 = calc_impurity(sets[0])
    ent_1 = calc_impurity(sets[1])
    info = ent - (len(sets[0].x))/(len(S.x))*ent_0 - (len(sets[1].x))/(len(S.x))*ent_1
    if info >= best_info:
      best_info = info
      best_j = j
  return best_j


def check_dat(S):
  data = S.x[0]
  n0 = 0
  for i in range(len(S.x)):
    if (S.x[i] == data).all():
      if S.label[i] == 0:
        n0 = n0 + 1
    else:
      return -1
  if n0 >= len(S.x) - n0:
    return 0
  else:
    return 1

def make_decisiontree(S, depth):
  if depth >= max_depth:
    n0 = 0
    for i in range(len(S.label)):
      if S.label[i] == 0:
        n0 = n0 + 1
    if n0 >= len(S.label) - n0:
      return TreeNode(-1, -1, 0, None, None)
    else:
      return TreeNode(-1, -1, 1, None, None)
  thesum = 0
  for i in range(len(S.label)):
    thesum += S.label[i]
  if thesum == 0:
    return TreeNode(-1, -1, 0, None, None)
  elif thesum == len(S.label):
    return TreeNode(-1, -1, 1, None, None)    
  else:
    same_x = check_dat(S)
    if same_x == 0:
      return TreeNode(-1, -1, 0, None, None)
    elif same_x == 1:
      return TreeNode(-1, -1, 1, None, None)
    bsp = best_split(S,depth)
    if bsp == -1:
      return TreeNode(-1, -1, 0, None, None)
    sets = split_set(S,bsp)
    mean = themean(S,bsp)
    return TreeNode(bsp, mean[1], mean[0], make_decisiontree(sets[0], depth + 1), make_decisiontree(sets[1], depth + 1))

def traverse(x, r):
  while r.feature != -1:
    if r.dire == 0:
      if x[r.feature] <= r.threshold:
        r = r.left
      else:
        r = r.right
    elif r.dire == 1:
      if x[r.feature] < r.threshold:
        r = r.right
      else:
        r = r.left
  return r.threshold

def learn(train_list):
  dec_tree = list()
  for train_set in train_list:
    dec_tree.append(make_decisiontree(train_set, 0))
  return dec_tree

def RandomForest_predict(forest, test_set):
  l = list()
  for x in test_set:
    prd = list()
    for root in forest:
      prd.append(traverse(x, root))
    if (sum(prd) > len(prd) / 2):
      l.append(1)
    else:
      l.append(0)
  return l

n = 500
S = theSet(trains_features, trains_label)
dat_samp = list()

sample_trda = sample(S, n)
random_forest = learn(sample_trda)
prd = RandomForest_predict(random_forest, tests_features)

for i in range(len(prd)):
  dat_samp.append([i+1, prd[i]])

with open('submit.csv', 'w') as f:
  spamwriter = csv.writer(f, delimiter = ',')
  spamwriter.writerow(['Id', 'Category'])
  spamwriter.writedat_samp(dat_samp)
