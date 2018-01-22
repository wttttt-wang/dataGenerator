"""
Hausdorff Distance
@ Definition: given A = {a1, a2, ..., an}, B = {b1, b2, ..., bm}
              dis: H(A, B) = max{h(A, B), h(B, A)}
              h(A, B): For each point a in A, 1. get the nearest(for a) b in A, the dis=dist(a, b) (Euclidean Dis)
"""
from math import sqrt


def euclidean_metric(pa, pb):
    """
    Calculate Euclidean Distance.
    pa & pb are list/tuple of same length
    :param pa:
    :param pb:
    :return:
    """
    return sqrt((pa[0] - pb[0])**2 + (pa[1] - pb[1])**2)


def one_way_hausdorff_distance(sa, sb):
    """
    Calculate unidirectional hausdorff dis.
    :param sa:
    :param sb:
    :return:
    """
    distance = 0.0
    for pa in sa:
        shortest = 9999999
        for pb in sb:
            dis = euclidean_metric(pa, pb)
            if dis < shortest:
                shortest = dis
        if shortest > distance:
            distance = shortest
    return distance


def hausdorff_distance(sa, sb):
    """
    Calculate hausdorff distance
    :param sa:
    :param sb:
    :return:
    """
    dis_a = one_way_hausdorff_distance(sa, sb)
    dis_b = one_way_hausdorff_distance(sb, sa)
    return dis_a if dis_a > dis_b else dis_b


if __name__ == '__main__':
    assert(euclidean_metric((1, 1), (1, 6)) == 5)
    A = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    B = [(0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (4, 2)]
    C = [(4, 2), (4, 1), (4, 0)]
    D = [(0, 2), (1, 2), (2, 2), (2, 3), (2, 4)]
    print hausdorff_distance(A, B)
