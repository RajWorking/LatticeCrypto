from .poly import *
from .hashers import *


def sign(msg, sk, pk):
    """
    y1, y2 chosen from R_{p, k}
    msk: a*y1 + y2
    msg: message to be signed (bytes obj)
    """
    s1, s2 = sk
    t, a, k = pk

    lim = 2 * k - 32
    while 1:
        y1 = gen_random_vector(f, -k, k)
        y2 = gen_random_vector(f, -k, k)
        msk = poly_op(a, y1, y2)
        c = hash_D32(msk, msg, k)
        z1 = poly_op(c, s1, 2 * y1)
        z2 = poly_op(c, s2, 2 * y2)
        if np.all(-lim <= z1) and np.all(z1 <= lim) and np.all(-lim <= z2) and np.all(z2 <= lim):
            break

    return z1.astype(int), z2.astype(int), c.astype(int)
