import run_word_count
import run_ngram


data_path = "/home/testData/others1.txt"
hdfs_path = "/testData/others1.txt"
run_ngram.gen_data(data_path, hdfs_path)

run_ngram.run_jar(hdfs_path)
run_word_count.run_jar(hdfs_path)
