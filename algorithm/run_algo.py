from mysql.readData import *
import MySQLdb
from algorithm.Preprocess import series_normalization
from algorithm.cluster import kmeans_cluster
import numpy as np
from algorithm.cluster import ts_kmeans
import time
from tslearn.clustering import TimeSeriesKMeans
from tslearn.clustering import cdist_dtw
from algorithm.regression.regression_algos import *


def run_for_metrics(conn, column):
    res = {}  # map from appId to it's type of `column`
    # 1. read data, only state == 'finished'
    data, contIds, app2conts, cont2id = contId_series(conn, column)   # labels is appId

    # 2. sampling
    sample_num, skip_thre, newData = 20, 9, []
    for i in range(len(data)):
        if len(data[i]) > skip_thre:
            if len(data[i]) < sample_num:
                newData.append(data[i] + [0] * (sample_num - len(data[i])))  # simply append 0s
            else:
                newData.append(series_normalization.interval_sampling(data[i], sample_num))

    # 3. normalization
    newData = series_normalization.normed(newData)
    # print newData

    # 4. run cluster
    '''kmeans cluster 1'''
    # cluster = kmeans_cluster.KMeansClassifier(dis_metrics='dtwdist')
    # cluster.fit(np.array(newData))
    # print cluster.get_centroids()
    '''kmeans cluster 2'''
    # s1 = time.time()
    # num_class, num_iter = 5, 300
    # cluster = ts_kmeans.ts_cluster(num_class)
    # cluster.k_means_clust(newData, num_iter, None)
    # print 'cluster time spent: ', time.time() - s1
    # print cluster.get_centroids()
    '''kmeans cluster 3'''
    km = TimeSeriesKMeans(n_clusters=7, metric='dtw', max_iter=10).fit(newData)  # 3:0.007, 5:0.003, 7:0.002, 11:0.001
    # print km.cluster_centers_
    # print contIds
    # print km.labels_
    # dists = cdist_dtw(newData, km.cluster_centers_)
    # print dists
    for app in app2conts:
        cntOccurs, type = {}, None  # put the max-occurs type as type for each application
        for cot in app2conts[app]:
            if cot not in cont2id:
                continue
            label = km.labels_[cont2id[cot]]
            cntOccurs[label] = cntOccurs.get(label, 0) + 1
            if not type or cntOccurs[label] > cntOccurs[type]:
                type = label
        res[app] = type
    return res


if __name__ == "__main__":
    conn = MySQLdb.connect(user='root', db='paperData')
    type_mem = run_for_metrics(conn, 'usedHeapMem')  # usedHeapMem, ProcessCpuTime, ProcessCpuLoad
    print type_mem
    type_cpu = run_for_metrics(conn, 'ProcessCpuLoad')
    print type_cpu
    confs = get_app_confs(conn)  # [appId, inputSize, driverMem, exeNum, exeCores, exeMem, execution_time]
    print confs

    # [appId], [inputSize, driverMem, exeNum, exeCores, exeMem, type_mem, type_cpu], [execution_time]
    reg_X, reg_y, apps = [], [], []
    for row in confs:
        apps.append(row[0])
        reg_y.append(row[-1])
        reg_X.append(row[1: -1])
    print 'apps: ', apps
    print 'confs input:', confs
    print 'execution time: ', reg_y

    svr(reg_X, reg_y)
