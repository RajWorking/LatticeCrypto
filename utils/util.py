# helpers
import random
import numpy as np
from config import *


def gen_random_vector(n, lb=-(p - 1) // 2, ub=(p - 1) // 2):
    """
    generate a random vector with
    - Length: n
    - Range: [lb, ub]
    """
    # return np.random.randint(lb, ub+1, n)
    return np.array([random.randrange(lb, ub + 1) for _ in range(n)])


def vector_to_Rp(vec):
    """
        polynomial belongs to ring Rp[x]
        coefficients in range[-(p-1)/2, (p-1)/2]
    """
    res = vec % p
    np.subtract(res, p, out=res, where=res > (p - 1) / 2)
    return res

# def int_cast(vec):
#     return np.array([int(x) for x in vec])
