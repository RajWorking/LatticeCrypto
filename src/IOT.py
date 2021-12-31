''' This code executes the signing algorithm by IOT device
'''

from config import *
import util
import numpy as np


class IOT_device:
    def __init__(self, sk, pk):
        '''
        sk = (s1, s2)
        pk = (t, a, k)
        '''
        self.sk = sk
        self.pk = pk

    def LSign(self, m):
        '''
        m: message to be signed
        '''
        a = self.pk[1]
        k = self.pk[2]
        y1 = util.gen_random_vector(N, -k, k)
        y2 = util.gen_random_vector(N, -k, k)
        # util.poly_op(a, y1, y2)
        # c = util.hash_D32()
        pass
