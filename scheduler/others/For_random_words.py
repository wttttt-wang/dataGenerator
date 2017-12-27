import random
import sys
from random import sample


# int string
def generate(fileName, lineCnt):
    with open(fileName, 'w') as fi:
        for i in range(1, lineCnt):
            line = ""
            for j in range(random.randint(1, 21)):
                line += ''.join(sample('bcDdeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTUV', random.randint(1, 11)))
            line += '\n'
            fi.write(line)


out1 = sys.argv[1] if len(sys.argv) >= 2 else 'words.txt'
lineCnt1 = int(sys.argv[3]) if len(sys.argv) >= 4 else 100

generate(out1, lineCnt1)
