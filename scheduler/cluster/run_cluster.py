import run_gmm
import run_kmeans
import run_GaussianMixture

data_path = "/home/testData/cluster1.txt"
hdfs_path = "/testData/cluster1.txt"
run_gmm.gen_data(data_path, hdfs_path)

run_gmm.run_jar(hdfs_path)
run_kmeans.run_jar(hdfs_path)
run_GaussianMixture.run_jar(hdfs_path)