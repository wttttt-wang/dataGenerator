# like data/mllib/sample_libsvm_data.txt

import random
import sys


def generate(fileName):
    with open(fileName, 'w') as fi:
        for i in range(1, int(sys.argv[1])):

            line = "{0} {1} {2} {3} {4}\n".format(i, random.random(), random.random(), random.random(), random.random())
            fi.write(line)

if len(sys.argv) < 2:
    print 'python ForRegression <output> <line>'
    sys.exit(-1)

generate(sys.argv[0])
