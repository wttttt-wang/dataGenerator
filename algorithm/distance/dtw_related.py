import dtw
from numpy import *
from numpy.linalg import *


x = array([0, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
y = array([1, 1, 1, 2, 2, 2, 2, 3, 2, 0]).reshape(-1, 1)


# 1. first, we need normalization

dist, cost, acc, path = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
print 'Minimum distance found:', dist


# another distance
dist1, cost1, acc1, path1 = dtw(x, y, dist=norm)


# The sequences used can be of different length
x = range(10)
y = [0] * 5 + x

x = array(x).reshape(-1, 1)
y = array(y).reshape(-1, 1)
dist, cost, acc, path = dtw(x, y, dist=lambda x, y: norm(x - y, ord=1))
print dist, cost, acc, path
