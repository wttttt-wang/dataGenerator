import run_decision_tree_2class
import run_naive_bayes
import run_random_forest_class


data_path = "/home/testData/2classify1.txt"
hdfs_path = "/testData/2classify1.txt"
run_decision_tree_2class.gen_data(data_path, hdfs_path)

run_decision_tree_2class.run_jar(hdfs_path)
run_naive_bayes.run_jar(hdfs_path)
run_random_forest_class.run_jar(hdfs_path)
