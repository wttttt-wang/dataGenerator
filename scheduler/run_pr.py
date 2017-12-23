from random import randint
from random import random
import os


lineCnt = randint(3000000, 7000000)
dotCnt = randint(lineCnt/randint(5, 7), lineCnt/randint(1, 3))

# 1. generate test data
data_path = "/home/testData/pageRank/pr1.txt"
hdfs_path = "/testData/pageRank/pr1.txt"
# 1.1 gen local data
os.system("rm -f {0}".format(data_path))
print 'generating testData, path: ', data_path
os.system("python /root/wttttt/data/dataGenerator/ForPageRank.py {0} {1} {2}"
          .format(data_path, lineCnt, dotCnt))
# 1.2 copy to hdfs
os.system("hdfs dfs -rm {0}".format(hdfs_path))
print 'copying to hdfs, path: ', hdfs_path
os.system("hdfs dfs -copyFromLocal {0} {1}".format(data_path, hdfs_path))


# 2. run jar
driver_mem = randint(1, 8)
exe_mem = randint(2, 8)
exe_cores = randint(1, 5)
# <input> <output> <algoType> <iter/tol>
type = randint(1, 2)
if type == 1:
    tt1 = random(0, 0.001)
else:
    tt1 = randint(10, 5000)
# 2.1 remove output
output = "/testData/pageRank/out1"
os.system("hdfs dfs -rm -r " + output)
cmd = '/home/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --class JavaPageRank ' \
      '--conf "spark.executor.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  --conf "spark.driver.extraJavaOptions=-XX:+UnlockCommercialFeatures -XX:+FlightRecorder -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.port=0 -Djava.util.logging.config.file=/home/spark-2.1.0-bin-hadoop2.6/conf/jmx.properties"  ' \
      '--master yarn --deploy-mode cluster  --driver-memory {0}g  --executor-memory {1}g   ' \
      '--executor-cores {2} ~/wttttt/spark-examples/spark-examples-2.0-SNAPSHOT.jar {3} {4} {5} {6}'\
    .format(driver_mem, exe_mem, exe_cores, hdfs_path, output, type, tt1)
print 'running spark..., cmd: ', cmd
os.system(cmd)

