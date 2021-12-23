''' This code executes the signing algorithm by IOT device
'''

from config import *
import numpy as np


class IOT_device:
    def __init__(self, s1, s2, t):
        self.sk = np.array(s1, s2)
        self.pk = t

    def LSign(self, m, a):
        '''
        m: message to be signed
        a: master public key
        '''
        pass
