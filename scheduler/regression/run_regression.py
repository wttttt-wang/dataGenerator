import run_dt_reg
import run_linear_rege
import run_random_forest_reg
import run_JavaModelSelectionViaTrainValidationSplit


data_path = "/home/testData/reg1.txt"
hdfs_path = "/testData/reg1.txt"

run_linear_rege.gen_data(data_path, hdfs_path)

run_linear_rege.run_jar(hdfs_path)
run_random_forest_reg.run_jar(hdfs_path)
run_dt_reg.run_jar(hdfs_path)
run_JavaModelSelectionViaTrainValidationSplit.run_jar(hdfs_path)
