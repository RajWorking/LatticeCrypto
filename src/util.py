import numpy as np
import hashlib
from config import *
import bitarray
import random

#############################################
# helpers


def gen_random_vector(n, lb=-(p-1)/2, ub=(p-1)/2):
    '''
    generate a random vector with
    - Length: n
    - Range: [lb, ub]
    '''
    # return np.random.randint(lb, ub+1, n)
    return np.array([random.randrange(lb, ub + 1) for _ in range(n)])


def vector_to_Rp(vec):
    '''
        polynomial belongs to ring Rp[x]
        coefficients in range[-(p-1)/2, (p-1)/2]
    '''
    res = vec % p
    np.subtract(res, p, out=res, where=res > (p-1)/2)
    return res


# def int_cast(vec):
#     return np.array([int(x) for x in vec])

#############################################
# hashers


def hash_R1(msg, n=N):
    '''
    msg: message in bytes
    '''
    hash_output = np.zeros(n, dtype=int)
    hash_base = int(hashlib.sha512(msg).hexdigest(), base=16)
    hash_base = np.array(list(np.base_repr(hash_base, 3))).astype(int)
    hash_base[hash_base == 2] = -1

    i = 0
    while i < n:
        m = min(len(hash_base), n - i)
        hash_output[i:i+m] = hash_base[:m]
        i += m

    return hash_output


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
    hash_input = np.concatenate((msk, np.array(ba.tolist())))
    hash_input = higher_order_bits(hash_input, k)
    hash_input = bytes(np.array_str(hash_input), 'utf-8')
    m = hashlib.blake2b(hash_input, digest_size=20)
    hash_output = np.zeros(512, dtype=int)
    digest_bits = (bin(int(m.hexdigest(), base=16))[2:]).zfill(160)
    for i in range(32):
        window = digest_bits[i*5: (i+1)*5]
        hash_output[16*i + int(window[1:5], 2)] = 1 if window[0] == '1' else -1
    hash_output = np.pad(hash_output, n-512)
    return hash_output


#############################################
# upper-lower-bits


def lower_order_bits(y, k):
    '''
        y = y1 * (2k + 1) + y0
        y0 -> lower order bits [-k, k]
        y1 -> higher order bits
    '''
    tkp1 = 2 * k + 1
    res = y % tkp1
    res = res - tkp1 * (res > k)
    assert np.all(res <= k) and np.all(res >= -k), "Code has a bug"
    return res


def higher_order_bits(y, k):
    tkp1 = 2 * k + 1
    res = y // tkp1 + (y % tkp1 > k)
    return res

##############################################
# polynomial_operations


# def poly_mod(exp):
#     '''
#     expression (mod (x^N + 1))
#     '''
#     ideal = [1] + (N - 1) * [0] + [1]
#     ideal = sp.Poly(ideal, sp.symbols('x'))
#     exp = sp.Poly(exp, sp.symbols('x'))
#     q, r = sp.div(exp, ideal)
#     # mod_output = int_cast(np.polydiv(exp, ideal)[1])
#     mod_output = np.array(r.all_coeffs())
#     mod_output = np.pad(mod_output, (N - len(mod_output), 0))
#     return vector_to_Rp(mod_output)

def poly_mod(exp):
    '''
    expression (mod (x^N + 1))
    '''
    m = len(exp) - 1
    res = exp % p
    for i in range(0, m-N+1):
        d = res[i]
        res[i] -= d
        res[i + N] -= d
    res = res[-N:]
    return vector_to_Rp(res)


def poly_op(a, s1, s2):
    '''
    t = a * s1 + s2
    '''
    return poly_mod(np.polyadd(np.convolve(s1, a), s2))

#############################################


def sign(msg, sk, pk):
    '''
    y1, y2 chosen from R_{p, k}
    msk: a*y1 + y2
    msg: message to be signed (bytes obj)
    '''
    s1, s2 = sk
    t, a, k = pk

    lim = 2 * k - 32
    while 1:
        y1 = gen_random_vector(N, -k, k)
        y2 = gen_random_vector(N, -k, k)
        msk = poly_op(a, y1, y2)
        c = hash_D32(msk, msg, k)
        z1 = poly_op(c, s1, 2*y1)
        z2 = poly_op(c, s2, 2*y2)
        if np.all(-lim <= z1) and np.all(z1 <= lim) and np.all(-lim <= z2) and np.all(z2 <= lim):
            break

    return z1, z2, c
