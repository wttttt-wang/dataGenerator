# from tslearn.generators import random_walks
# from tslearn.clustering import TimeSeriesKMeans
# from tslearn.clustering import cdist_dtw
# import numpy
#
# X = random_walks(n_ts=50, sz=32, d=1)
# km = TimeSeriesKMeans(n_clusters=3, metric='dtw', max_iter=10).fit(X)
# print km.cluster_centers_
# print km.cluster_centers_.shape
# dists = cdist_dtw(X, km.cluster_centers_)
# print numpy.alltrue(km.labels_ == dists.argmin(axis=1))
# print numpy.alltrue(km.labels_ == km.predict(X))


import matplotlib.pyplot as plt
plt.plot([1, 3, 4])
plt.plot([2, 3, 4])
plt.show()
