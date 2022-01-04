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
        priv_keys, k = self.__gen_signer_priv_keys()
        pub_keys = self.__gen_signer_pub_keys(priv_keys, k)
        return {'priv': priv_keys, 'pub': pub_keys}

    def __gen_master_keys(self):
        s1 = util.gen_random_vector(N, -1, 1)
        s2 = util.gen_random_vector(N, -1, 1)
        a = util.gen_random_vector(N)
        self.msk = np.array([s1, s2])
        self.mpk = a

    def __gen_signer_priv_keys(self):
        # M signer keys and 1 aggregator key
        k = np.random.choice(np.arange(K_MIN, K_MAX),
                             size=M + 1, replace=False).reshape(-1, 1)
        lower_orders = util.lower_order_bits(self.msk.reshape(1, -1), k)
        lower_orders = lower_orders.reshape(k.shape[0], 2, -1)
        return lower_orders, k

    def __gen_signer_pub_keys(self, priv_keys, k):
        pub_keys = [None] * (M + 1)
        for i in range(M + 1):
            t = util.poly_op(self.mpk, priv_keys[i, 0], priv_keys[i, 1])
            t = np.pad(t, (N - len(t), 0))
            pub_keys[i] = (t, self.mpk, k[i][0])
        return pub_keys
