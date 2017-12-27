from random import randint
import os


def gen_data(data_path, hdfs_path):
    lineCnt = randint(7000000, 30000000)
    columnCnt = randint(5, 30)
    # 1.1 gen local data
    os.system("rm -f {0}".format(data_path))
    print 'generating testData, path: ', data_path
    os.system("python /root/wttttt/data/dataGenerator/ForLinearRegression.py {0} {1} {2}"
              .format(data_path, lineCnt, columnCnt))
    # 1.2 copy to hdfs
    os.system("hdfs dfs -rm {0}".format(hdfs_path))
    print 'copying to hdfs, path: ', hdfs_path
    os.system("hdfs dfs -copyFromLocal {0} {1}".format(data_path, hdfs_path))


def run_jar(hdfs_path):
    driver_mem = randint(1, 3)
    exe_mem = randint(2, 8)
    exe_cores = randint(1, 5)
    cmd = '/home/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --class JavaDecisionTreeRegressionExample ' \
          '--conf "spark.executor.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  --conf "spark.driver.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  ' \
          '--master yarn --deploy-mode cluster  --driver-memory {0}g  --executor-memory {1}g   ' \
          '--executor-cores {2} ~/wttttt/spark-examples/spark-examples-2.0-SNAPSHOT.jar {3}' \
        .format(driver_mem, exe_mem, exe_cores, hdfs_path)
    print 'running spark..., cmd: ', cmd
    os.system(cmd)


if __name__ == "__main__":
    # 1. generate test data
    data_path = "/home/testData/lin11.txt"
    hdfs_path = "/testData/lin11.txt"
    gen_data(data_path, hdfs_path)

    # 2. run jar
    run_jar(hdfs_path)


