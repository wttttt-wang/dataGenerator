# like sample_linear_regression_data.txt

import random
import sys


def generate(fileName, lineCnt, dotCnt):
    with open(fileName, 'w') as fi:
        for i in range(1, lineCnt):
            line = "{0} {1}\n".format(random.randint(1, dotCnt), random.randint(1, dotCnt))
            fi.write(line)


# if len(sys.argv) < 3:
#     print 'python ForLinearRegression <output> <line> <columnNum>'
#     sys.exit(-1)
out = sys.argv[1] if len(sys.argv) >= 2 else 'prData.txt'
lineCnt = int(sys.argv[2]) if len(sys.argv) >= 3 else 100
dotCnt = int(sys.argv[3]) if len(sys.argv) >= 4 else 100
generate(out, lineCnt, dotCnt)
