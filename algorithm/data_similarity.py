import algorithm.series_normalization as series_norm
from numpy import *
from numpy.linalg import *
from dtw import dtw
from algorithm.distance import frechet_dis
from algorithm.distance import hausdorff_dis


def aligned_sampling(ser1, ser2):
    pro = len(ser1) / len(ser2)
    if pro < 1:
        t1, t2 = aligned_sampling(ser2, ser1)
        return t2, t1
    if pro < 2:
        return ser1, ser2
    newSer1 = []
    for i in range(0, len(ser1), pro):
        newSer1.append(ser1[i])
    return newSer1, ser2


def get_sim(type, ser1, ser2):
    if not ser1 or not ser2:
        return
    # 1. data norm
    ser1_norm = series_norm.normed([ser1])[0]
    ser2_norm = series_norm.normed([ser2])[0]

    # optional: aligned sampling to make two series with same length
    ser1_norm, ser2_norm = aligned_sampling(ser1_norm, ser2_norm)

    # 2. calculate similarity
    if type == 'dtw':
        ser1_norm = array(ser1_norm).reshape(-1, 1)
        ser2_norm = array(ser2_norm).reshape(-1, 1)
        dist, cost, acc, path = dtw(ser1_norm, ser2_norm, dist=lambda x, y: norm(x-y, ord=1))
        return dist
    elif type == 'frechet':
        ser1_norm = list(enumerate(ser1_norm))
        ser2_norm = list(enumerate(ser2_norm))
        dist = frechet_dis.frechet_distance(ser1_norm, ser2_norm)
        return dist
    elif type == 'hausdorff':
        ser1_norm = list(enumerate(ser1_norm))
        ser2_norm = list(enumerate(ser2_norm))
        dist = hausdorff_dis.hausdorff_distance(ser1_norm, ser2_norm)
        return dist
    else:
        print "Wrong similarity type assigned."


if __name__ == "__main__":
    s1 = [1,2]
    s2 = [1,2,3,4]
    print aligned_sampling(s1, s2)

    # get_sim("dtw", [2,3,4,5,6], [1,2,3,4,5])
    # get_sim("dtw", [2,3,4,5,9,1,5,2], [7,5,4,2])
