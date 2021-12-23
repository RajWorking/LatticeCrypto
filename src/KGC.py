''' This code executes the key-generation algorithm run by the KGC
'''

from config import *
import util
import numpy as np


class KGC:
    def __init__(self):
        self.mpk = None
        self.msk = None

    def KeyGen(self):
        self.__gen_master_keys()
        priv_keys = self.__gen_signer_priv_keys()
        pub_keys = self.__gen_signer_pub_keys(priv_keys)
        return {'priv': priv_keys, 'pub': pub_keys}

    def __gen_master_keys(self):
        s1 = util.gen_random_vector(N)
        s2 = util.gen_random_vector(N)
        a = util.gen_random_vector(N)
        self.msk = np.array([s1, s2])
        self.mpk = a

    def __gen_signer_priv_keys(self):
        # M signer keys and 1 aggregator key
        k = np.random.choice(np.arange(1, np.sqrt(p)),
                             size=M + 1, replace=False)
        higher_orders = (self.msk.reshape(-1, 1) // (2 * k + 1) +
                         (self.msk.reshape(-1, 1) % (2 * k + 1) > k)).T.reshape(k.shape[0], 2, -1)
        assert np.all(((2 * k + 1)[:, None, None] * higher_orders -
                       self.msk).reshape(k.shape[0], -1) <= k[:, None]), "Code has a bug"
        assert np.all(((2 * k + 1)[:, None, None] * higher_orders -
                       self.msk).reshape(k.shape[0], -1) >= -k[:, None]), "Code has a bug"
        return higher_orders

    def __gen_signer_pub_keys(self, priv_keys):
        pub_keys = np.empty((M + 1, N))
        for i in range(M + 1):
            res = util.poly_op(self.mpk, priv_keys[i, 0], priv_keys[i, 1])
            pub_keys[i] = np.pad(res, (N - len(res), 0))
        return pub_keys
