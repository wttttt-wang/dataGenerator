from random import randint
import os


def gen_data(data_path, hdfs_path):
    lineCnt = randint(5000000, 12000000)
    columnCnt = randint(1, 30)
    classCnt = randint(5, 27)
    # 1.1 gen local data
    os.system("rm -f {0}".format(data_path))
    print 'generating testData, path: ', data_path
    os.system("python ForCluster.py {0} {1} {2} {3}"
              .format(data_path, lineCnt, columnCnt, classCnt))
    # 1.2 copy to hdfs
    os.system("hdfs dfs -rm {0}".format(hdfs_path))
    print 'copying to hdfs, path: ', hdfs_path
    os.system("hdfs dfs -copyFromLocal {0} {1}".format(data_path, hdfs_path))


def run_jar(hdfs_path, local_path):
    driver_mem = randint(1, 3)
    exe_mem = randint(2, 8)
    exe_cores = randint(1, 5)
    # <Input> <maxIter>
    k = randint(16, 87)

    cmd = '/home/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --class JavaGaussianMixtureExample ' \
          '--conf "spark.executor.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  --conf "spark.driver.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  ' \
          '--master yarn --deploy-mode cluster --num-executors {0} --driver-memory {1}g  --executor-memory {2}g   ' \
          '--executor-cores {3} ~/wttttt/spark-examples/spark-examples-2.0-SNAPSHOT.jar {4} {5}' \
        .format(randint(1, 6), driver_mem, exe_mem, exe_cores, hdfs_path, k)
    print 'running spark..., cmd: ', cmd
    print 'input file size: ', os.path.getsize(local_path)
    os.system(cmd)


if __name__ == "__main__":
    # 1. generate test data
    data_path = "/home/testData/kmeans111.txt"
    hdfs_path = "/home/testData/kmeans1111.txt"
    gen_data(data_path, hdfs_path)
    run_jar(hdfs_path, data_path)

