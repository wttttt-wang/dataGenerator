import pandas as pd
import matplotlib.pyplot as plt
from mysql.readData import *
import MySQLdb


def plot_data(timeseries):
    dta = pd.Series(timeseries)
    plt.plot(dta)
    plt.show()


if __name__ == '__main__':
    # apps = [['application_1513994030877_0149', 'application_1513994030877_0165', 'application_1513994030877_0320'],
    #         ['application_1513994030877_0189', 'application_1513994030877_0224', 'application_1513994030877_0379']]
    # containers = ['container_1513994030877_0160_01_000001', 'container_1513994030877_0160_01_000002',
    #               'container_1513994030877_0153_02_000002', 'container_1513994030877_0153_02_000001',
    #               'container_1513994030877_0353_01_000002', 'container_1513994030877_0353_01_000003',
    #               'container_1513994030877_0279_01_000003', 'container_1513994030877_0279_01_000002',
    #               'container_1513994030877_0266_01_000002', 'container_1513994030877_0266_01_000003',
    #               'container_1513994030877_0417_01_000002', 'container_1513994030877_0417_01_000003']
    conn = MySQLdb.connect(user='root', db='paperData')
    apps, containers = {}, {}
    for name in ['NaiveBayesExample', 'JavaKMeansExam', 'RandomForestTestRegress',
                 'JavaGradientBoostedTreeClassifierExample', 'JavaGeneralizedLinearRegressionExample',
                 'GMMExample', 'JavaModelSelectionViaTrainValidationSplitExample']:
        apps[name] = get_appId_by_name(conn, name, 3)
    for name in apps:
        containers[name] = []
        for aid in apps[name]:
            containers[name] += getContainerId(conn, aid, 2)
    print apps, containers
    for name in containers:
        print '-----', name
        for c in containers[name]:
            s = getMetrics(conn, 'ProcessCpuLoad', c)
            plot_data(s)
