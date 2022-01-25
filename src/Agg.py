''' This code executes the algorithm by Aggregator
'''

from config import *
import util
import numpy as np


class Aggregator:
    def __init__(self, sk, pk):
        '''
        sk: (s1, s2)
        pk: (t, a, k)
        '''
        self.sk = sk
        self.pk = pk

    def LVer(self, msg, sig, pub) -> bool:
        '''
        msg: signed message
        sig: (z1, z2, c) signature
        pub: (t, a, k) public key
        '''
        z1, z2, c = sig
        t, a, k = pub
        lim = 2 * k - 32

        if not (np.all(-lim <= z1) and np.all(z1 <= lim) and np.all(-lim <= z2) and np.all(z2 <= lim)):
            print('not in range')
            return False

        msk = util.poly_mod(
            np.polysub(
                util.poly_op(a, z1, z2),
                np.convolve(c, t)
            ) * pow(2, -1, p)
        )

        c_new = util.hash_D32(msk, msg, k)
        if not np.all(c_new == c):
            # print(np.sum(c_new != c), 'not matched')
            return False

        return True

    def AggSign(self, msg):
        return util.sign(msg, self.sk, self.pk)
