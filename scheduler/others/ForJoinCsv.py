import random
import sys
import csv
from random import sample


# int string
def generate(fileName, lineCnt, classNum):
    with open(fileName, 'w') as fi:
        writer = csv.writer(fi)
        for i in range(1, lineCnt):
            class_type = random.randint(1, classNum)
            writer.writerow([class_type, ''.join(sample('bcDdeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTUV', random.randint(1, 8)))])


# if len(sys.argv) < 3:
#     print 'python ForLinearRegression <output> <line> <columnNum>'
#     sys.exit(-1)
out1 = sys.argv[1] if len(sys.argv) >= 2 else 'join1.csv'
out2 = sys.argv[2] if len(sys.argv) >= 3 else 'join2.csv'
lineCnt1 = int(sys.argv[3]) if len(sys.argv) >= 4 else 100
lineCnt2 = int(sys.argv[4]) if len(sys.argv) >= 5 else 100
classNum = int(sys.argv[5]) if len(sys.argv) >= 6 else 100

generate(out1, lineCnt1, classNum)
generate(out2, lineCnt2, classNum)
