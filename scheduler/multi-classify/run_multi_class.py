import run_MultilayerPerceptronClassifier


data_path = "/home/testData/multi1.txt"
hdfs_path = "/testData/multi1.txt"

run_MultilayerPerceptronClassifier.gen_data(data_path, hdfs_path)

run_MultilayerPerceptronClassifier.run_jar(hdfs_path)
