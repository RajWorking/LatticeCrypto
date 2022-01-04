import numpy as np
import hashlib
from config import *
import bitarray


def gen_random_vector(n, lb=-(p-1)/2, ub=(p-1)/2):
    '''
    generate a random vector with
    - Length: n
    - Range: [lb, ub]
    '''
    return np.random.randint(lb, ub+1, n)


def hash_D32(msk, msg, k, n=N):
    '''
    hash function
    (0,1)* -> D_n_32
    D_n_32: vector of length n with all 0s except atmost 32 values +1/-1
    n >= 512
    c <- H(higher_order(msk || msg))
    '''
    ba = bitarray.bitarray()
    ba.frombytes(msg)
    input = np.concatenate((msk, np.array(ba.tolist())))
    input = higher_order_bits(input, k)
    m = hashlib.blake2b(digest_size=20)
    m.update(input)
    hash_output = np.zeros(512)
    digest_bits = (bin(int(m.hexdigest(), base=16))[2:]).zfill(160)
    for i in range(32):
        window = digest_bits[i*5: (i+1)*5]
        hash_output[16*i + int(window[1:5], 2)] = 1 if window[0] == '1' else -1
    hash_output = np.pad(hash_output, n-512)
    return hash_output


def vector_to_Rp(vec, p):
    '''
        polynomial belongs to ring Rp[x]
        coefficients in range[-(p-1)/2, (p-1)/2]
    '''
    res = np.remainder(vec, p)
    np.subtract(res, p, out=res, where=res > (p-1)/2)
    return res


def lower_order_bits(y, k):
    '''
        y = y1 * (2k + 1) + y0
        y0 -> lower order bits [-k, k]
        y1 -> higher order bits
    '''
    tkp1 = 2 * k + 1
    res = y % tkp1
    res = res - tkp1*(res > k)
    assert np.all(res <= k) and np.all(res >= -k), "Code has a bug"
    return res


def higher_order_bits(y, k):
    tkp1 = 2 * k + 1
    res = y // tkp1 + (y % tkp1 > k)
    return res


def poly_mod(exp):
    '''
    exp (mod (x^N + 1))
    '''
    ideal = [1] + (N - 1) * [0] + [1]
    return vector_to_Rp(
        np.polydiv(
            exp,
            ideal
        )[1].astype(int), p)


def poly_op(a, s1, s2):
    '''
    t = a * s1 + s2
    '''
    return poly_mod(np.polyadd(np.convolve(s1, a), s2))


def sign(msg, a, k, s1, s2):
    '''
    y1, y2 chosen from R_{p, k}
    msk: a*y1 + y2
    msg: message to be signed (bytes obj)
    '''
    while 1:
        y1 = gen_random_vector(N, -k, k)
        y2 = gen_random_vector(N, -k, k)
        msk = poly_op(a, y1, y2)
        c = hash_D32(msk, msg, k)
        z1 = poly_op(c, s1, y1)
        z2 = poly_op(c, s2, y2)
        lim = k - 32
        if np.all(-lim <= z1) and np.all(z1 <= lim) and np.all(-lim <= z2) and np.all(z2 <= lim):
            break

    return z1, z2, c
