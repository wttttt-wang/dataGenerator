from random import randint
import os


lineCnt = randint(2000000, 7000000)
columnCnt = randint(1, 30)
classCnt = randint(5, 27)

# 1. generate test data
data_path = "/home/testData/lda/lda1.txt"
hdfs_path = "/testData/lda/lda1.txt"
# 1.1 gen local data
os.system("rm -f {0}".format(data_path))
print 'generating testData, path: ', data_path
os.system("python /root/wttttt/data/dataGenerator/ForLDA.py {0} {1} {2} {3}"
          .format(data_path, lineCnt, columnCnt, classCnt))
# 1.2 copy to hdfs
os.system("hdfs dfs -rm {0}".format(hdfs_path))
print 'copying to hdfs, path: ', hdfs_path
os.system("hdfs dfs -copyFromLocal {0} {1}".format(data_path, hdfs_path))


# 2. run jar
driver_mem = randint(1, 8)
exe_mem = randint(2, 8)
exe_cores = randint(1, 5)
# <Input> <K> <maxIter>
k = randint(classCnt - 2, classCnt + 10)
maxIter = randint(70, 500)

cmd = '/home/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --class JavaLDAExample ' \
      '--conf "spark.executor.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  --conf "spark.driver.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  ' \
      '--master yarn --deploy-mode cluster  --driver-memory {0}g  --executor-memory {1}g   ' \
      '--executor-cores {2} ~/wttttt/spark-examples/spark-examples-2.0-SNAPSHOT.jar {3} {4} {5}'\
    .format(driver_mem, exe_mem, exe_cores, hdfs_path, k, maxIter)
print 'running spark..., cmd: ', cmd
os.system(cmd)
