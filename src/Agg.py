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
        z1 = sig[0]
        z2 = sig[1]
        c = sig[2]
        t = pub[0]
        a = pub[1]
        k = pub[2]
        lim = k - 32

        if not (np.all(-lim <= z1) and np.all(z1 <= lim) and np.all(-lim <= z2) and np.all(z2 <= lim)):
            print('not in range')
            return False

        msk = util.poly_mod(np.polysub(
            util.poly_op(a, z1, z2), np.polymul(c, t))
        )

        if not np.all(util.hash_D32(msk, msg, k) == c):
            print(np.sum(util.hash_D32(msk, msg, k) != c), 'not matched')
            return False

        return True

    def AggSign(self, msg):
        return util.sign(msg, self.pk[1], self.pk[2], self.sk[0], self.sk[1])
