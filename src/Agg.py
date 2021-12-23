''' This code executes the algorithm by Aggregator
'''

from config import *
import numpy as np


class Aggregator:
    def __init__(self, s1, s2, t):
        self.sk = np.array(s1, s2)
        self.pk = t

    def LVer(self, m, a, z1, z2, c):
        '''
        a: master public key
        m: signed message
        (z1, z2, c): signature
        '''
        pass
    
    def AggSign(self, m, a):
        '''
        m: message to be signed
        a: master public key
        '''
        pass