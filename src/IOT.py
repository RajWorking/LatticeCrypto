''' This code executes the signing algorithm by IOT device
'''

from config import *
import util
import numpy as np


class IOT_device:
    def __init__(self, sk, pk):
        '''
        sk: (s1, s2)
        pk: (t, a, k)
        '''
        self.sk = sk
        self.pk = pk

    def LSign(self, msg):
        return util.sign(msg, self.sk, self.pk)
