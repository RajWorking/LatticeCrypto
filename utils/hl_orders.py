# higher-lower order bits
import numpy as np


def lower_order_bits(y, k):
    """
        y = y1 * (2k + 1) + y0
        y0 -> lower order bits [-k, k]
        y1 -> higher order bits
    """
    tkp1 = 2 * k + 1  # two k plus one
    res = y % tkp1
    res = res - tkp1 * (res > k)
    assert np.all(res <= k) and np.all(res >= -k), "Bug"
    return res


def higher_order_bits(y, k):
    tkp1 = 2 * k + 1
    res = y // tkp1 + (y % tkp1 > k)
    return res
