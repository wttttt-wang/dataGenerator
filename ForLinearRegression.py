# like sample_linear_regression_data.txt

import random
import sys


def generate(fileName, columnNum, lineCnt):
    with open(fileName, 'w') as fi:
        for i in range(1, lineCnt):
            value = random.uniform(0, 1)
            line = "{0} ".format(value)
            for j in range(1, columnNum + 1):
                line += "{0}:{1} ".format(j, random.uniform(0, 1))
            fi.write(line + "\n")


# if len(sys.argv) < 3:
#     print 'python ForLinearRegression <output> <line> <columnNum>'
#     sys.exit(-1)
out = sys.argv[1] if len(sys.argv) >= 2 else 'linearReg.txt'
lineCnt = int(sys.argv[2]) if len(sys.argv) >= 3 else 100
columnNum = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
generate(out, columnNum, lineCnt)
