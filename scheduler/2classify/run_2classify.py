import run_decision_tree_2class
import run_naive_bayes
import run_random_forest_class
import run_grad_bt


data_path = "/home/testData/2classify1.txt"
hdfs_path = "/home/testData/2classify1.txt"
run_decision_tree_2class.gen_data(data_path, hdfs_path)

run_decision_tree_2class.run_jar(hdfs_path, data_path)
run_naive_bayes.run_jar(hdfs_path, data_path)
run_random_forest_class.run_jar(hdfs_path, data_path)
# run_grad_bt.run_jar(hdfs_path, data_path)
