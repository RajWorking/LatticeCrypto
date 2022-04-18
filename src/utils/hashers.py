# hashing functions
import hashlib
import bitarray
from ..config import *
from .hl_orders import *


def hash_R1(msg, n=f):
    """
    msg: message in bytes
    """
    hash_output = np.zeros(n, dtype=int)
    hash_base = int(hashlib.sha512(msg).hexdigest(), base=16)
    hash_base = np.array(list(np.base_repr(hash_base, 3))).astype(int)
    hash_base[hash_base == 2] = -1

    i = 0
    while i < n:
        m = min(len(hash_base), n - i)
        hash_output[i:i + m] = hash_base[:m]
        i += m

    return hash_output


def hash_D32(msk, msg, k, n=f):
    """
    hash function
    (0,1)* -> D_n_32
    D_n_32: vector of length n with all 0s except atmost 32 values +1/-1
    n >= 512
    c <- H(higher_order(msk || msg))
    """
    ba = bitarray.bitarray()
    ba.frombytes(msg)
    hash_input = np.concatenate((msk, np.array(ba.tolist())))
    hash_input = higher_order_bits(hash_input, k)
    hash_input = bytes(np.array_str(hash_input), 'utf-8')
    m = hashlib.blake2b(hash_input, digest_size=20)
    hash_output = np.zeros(512, dtype=int)
    digest_bits = (bin(int(m.hexdigest(), base=16))[2:]).zfill(160)
    for i in range(32):
        window = digest_bits[i * 5: (i + 1) * 5]
        hash_output[16 * i + int(window[1:5], 2)] = 1 if window[0] == '1' else -1
    hash_output = np.pad(hash_output, (n - 512, 0))
    return hash_output
