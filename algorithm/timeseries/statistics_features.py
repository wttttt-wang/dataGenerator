# -*- coding:utf-8 -*-
import numpy as np
from scipy.stats import kurtosis, skew


def get_mean(nums):
    return np.mean(nums)


def get_cov(nums):
    return np.cov(nums)


def get_var(nums):
    print np.var(nums)


def get_skew_kur(nums):
    # kurtosis: 峭度
    return skew(nums), kurtosis(nums)


if __name__ == "__main__":
    nums1 = [1, 2, 3, 4]
    print get_cov(nums1)
