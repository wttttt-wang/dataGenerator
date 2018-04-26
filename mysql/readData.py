import MySQLdb

from algorithm.distance import data_similarity

JMX_METRICS_TABLE = "core_job_jmx_metrics"
CONTAINER_INFO_TABLE = "core_job_container_info"
SPARK_JOBS_TABLE = "core_spark_jobs"


def get_all_spark_jobs(conn):
    sql = "select yarn_id, streaming_name from {} where state='finished'".format(SPARK_JOBS_TABLE)
    res = {}
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for appId, name in rows:
        if name not in res:
            res[name] = []
        res[name].append(appId)
    return res


def get_appId_by_name(conn, name, num):
    sql = "select yarn_id from core_spark_jobs WHERE streaming_name='{}' limit {}".format(name, num)
    res = []
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for r in rows:
        res.append(r[0])
    return res


def getContainerId(conn, appId, num):
    sql = "select containerId from {} where appId='{}' and isDriver=0 limit {}".format(CONTAINER_INFO_TABLE, appId, num)
    cursor = conn.cursor()
    cursor.execute(sql)
    res = []
    rows = cursor.fetchall()
    for r in rows:
        res.append(r[0])
    return res


def getMetrics(conn, column, containerId):
    res = []
    sql = "select {} from {} where containerId='{}' order by ts".format(column, JMX_METRICS_TABLE, containerId)

    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for r in rows:
        res.append(r[0])
    return res


def get_all_metrics_partitioned_by_name(conn, column):
    """
    :param conn: mysql connection
    :param column: the column of the targeted metrics
    :return: dict: {streaming_name: {appId: [metSer]}}
    """
    data = {}  # name: {appId: {[metSer]}}

    spark_jobs = get_all_spark_jobs(conn)
    print "all_spark_jobs", spark_jobs

    for name in spark_jobs:
        apps = spark_jobs[name]
        data[name] = {}
        for appId in apps:
            data[name][appId] = []
            containers = getContainerId(conn, appId, 2)
            for containerId in containers:
                metSer = getMetrics(conn, column, containerId)
                data[name][appId].append(metSer)
    return data


def get_all_metrics(conn, column):
    data = {}  # appId: [[]]
    spark_jobs = get_all_spark_jobs(conn)
    print "all_spark_jobs", spark_jobs

    for name in spark_jobs:
        for appId in spark_jobs[name]:
            data[appId] = []
            containers = getContainerId(conn, appId)
            for containerId in containers:
                metSer = getMetrics(conn, column, containerId)
                data[appId].append(metSer)
    return data


def get_all_metrics_containerId(conn, column):
    data = {}  # contanerId
    spark_jobs = get_all_spark_jobs(conn)
    print "all_spark_jobs", spark_jobs

    for name in spark_jobs:
        for appId in spark_jobs[name]:
            containers = getContainerId(conn, appId, 3)
            for containerId in containers:
                metSer = getMetrics(conn, column, containerId)
                data[containerId] = metSer
    return data


def get_app_confs(conn):
    res = []
    sql = "select yarn_id, inputSize, driverMem, exeNum, exeCores, exeMem, (finish_time - start_time) as execTime " \
          "from {} where state='finished'".format(SPARK_JOBS_TABLE)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for r in rows:
        res.append(r)
    return res


def contId_series(conn, column):
    # only get state == 'finished'
    # cont2ind map from container id to index of this container metrics in data
    data, contIds, app2cons, cont2ind = [], [], {}, {}
    sql = "select containerId, appId FROM {} a JOIN {} b on a.appId=b.yarn_id " \
          "where state='finished'".format(CONTAINER_INFO_TABLE, SPARK_JOBS_TABLE)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        contIds.append(row[0])
        if row[1] not in app2cons:
            app2cons[row[1]] = []
        app2cons[row[1]].append(row[0])
    # print contIds
    for contId in contIds:
        sql2 = "select {} from {} where containerId='{}' order by ts".format(column, JMX_METRICS_TABLE, contId)
        cursor.execute(sql2)
        tmpRows, tmpSeries = cursor.fetchall(), []
        for r in tmpRows:
            tmpSeries.append(r[0])
        cont2ind[contId] = len(data)
        data.append(tmpSeries)
        # print len(tmpSeries), tmpSeries
    return data, contIds, app2cons, cont2ind


def print_sim(data, simi):
    prevNameSer = None
    sumApp, cntApp, sumName, cntName = 0, 0, 0, 0
    for name in data:
        if data[name] and data[name].values()[0]:
            if prevNameSer:
                vv1 = data_similarity.get_sim(simi, prevNameSer, data[name].values()[0][0])
                if vv1 is not None:
                    cntName += 1
                    sumName += vv1
                    print 'diff streaming name', vv1
            prevNameSer = data[name].values()[0][0]
        prevAppSer = None
        for appId in data[name]:
            if data[name][appId]:
                if prevAppSer:
                    vv2 = data_similarity.get_sim(simi, prevAppSer, data[name][appId][0])
                    if vv2 is not None:
                        cntApp += 1
                        sumApp += vv2
                        print "diff app with same name", vv2
                prevAppSer = data[name][appId][0]
    print 'Avg simi for same Name: ', sumApp * 1.0 / cntApp
    print 'Avg simi for different Name: ', sumName * 1.0 / cntName


if __name__ == "__main__":
    conn = MySQLdb.connect(user='root', db='paperData')
    contId_series(conn, 'ProcessCpuTime')
    # data = get_all_metrics_partitioned_by_name(conn, 'ProcessCpuLoad')  # usedHeapMem
    #
    # print print_sim(data, 'dtw')

    # series = getMetrics(conn, 'usedHeapMem', 'container_1513994030877_0149_01_000002')
    # print series

    # afterNorm = norm.normed([series])[0]
    # print afterNorm
    # print max(afterNorm), min(afterNorm)
