"""
This code executes the signing
algorithm by IOT device
"""

from ..utils import sign


class IOT_device:
    def __init__(self, sk, pk):
        """
        sk: (s1, s2)
        pk: (t, a, k)
        """
        self.sk = sk
        self.pk = pk

    def LSign(self, msg):
        return sign.sign(msg, self.sk, self.pk)
