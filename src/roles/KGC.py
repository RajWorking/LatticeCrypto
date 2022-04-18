"""
This code executes the key-generation
algorithm run by the KGC
"""

import numpy as np
from ..config import *
from ..utils import hl_orders, hashers, poly, util


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
        s1 = util.gen_random_vector(f)
        s2 = util.gen_random_vector(f)
        a = util.gen_random_vector(f)
        self.msk = np.array([s1, s2])
        self.mpk = a

    def __gen_signer_priv_keys(self):
        # N signer keys and 1 aggregator key
        k = np.random.choice(np.arange(K_MIN, K_MAX),
                             size=N + 1, replace=False).reshape(-1, 1)
        lower_orders = hl_orders.lower_order_bits(self.msk.flatten(), k)
        lower_orders = lower_orders.reshape(-1, f)
        lower_orders = np.array([hashers.hash_R1(lo) for lo in lower_orders])
        lower_orders = lower_orders.reshape((-1, 2, f))
        return lower_orders, k

    def __gen_signer_pub_keys(self, priv_keys, k):
        pub_keys = []
        for i in range(N + 1):
            t = poly.poly_op(self.mpk, priv_keys[i, 0], priv_keys[i, 1])
            t = np.pad(t, (f - len(t), 0))
            pub_keys += [(t, self.mpk, k[i][0])]
        return pub_keys
