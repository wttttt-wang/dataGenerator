from random import randint
import os


lineCnt = randint(2000000, 7000000)
lineCnt2 = randint(2000000, 10000000)
classCnt = randint(5, 27)

# 1. generate test data
data_path = "/home/testData/join1.csv"
data_path2 = "/home/testData/join2.csv"
hdfs_path = "/testData/join1.csv"
hdfs_path2 = "/testData/join2.csv"

# 1.1 gen local data
os.system("rm -f {0}".format(data_path))
print 'generating testData, path: ', data_path
os.system("python ForJoinCsv.py {0} {1} {2} {3} {4}"
          .format(data_path, data_path2, lineCnt, lineCnt2, classCnt))
# 1.2 copy to hdfs
os.system("hdfs dfs -rm {0}".format(hdfs_path))
os.system("hdfs dfs -rm {0}".format(hdfs_path2))
print 'copying to hdfs, path: ', hdfs_path
os.system("hdfs dfs -copyFromLocal {0} {1}".format(data_path, hdfs_path))
os.system("hdfs dfs -copyFromLocal {0} {1}".format(data_path, hdfs_path2))


# 2. run jar
driver_mem = randint(1, 3)
exe_mem = randint(2, 8)
exe_cores = randint(1, 5)

cmd = '/home/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --class BasicJoinCsv ' \
      '--conf "spark.executor.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  --conf "spark.driver.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  ' \
      '--master yarn --deploy-mode cluster  --driver-memory {0}g  --executor-memory {1}g   ' \
      '--executor-cores {2} ~/wttttt/spark-examples/spark-examples-2.0-SNAPSHOT.jar {3} {4}'\
    .format(driver_mem, exe_mem, exe_cores, hdfs_path, hdfs_path2)
print 'running spark..., cmd: ', cmd
os.system(cmd)

