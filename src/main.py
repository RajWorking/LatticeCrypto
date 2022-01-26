from hashlib import sha256
import numpy as np
import time
from config import *
from Agg import Aggregator
from IOT import IOT_device
from KGC import KGC
import os
import sys
np.set_printoptions(threshold=sys.maxsize)


def timeit(code, title):
    st = time.time()
    res = code()
    end = time.time()
    t = end - st
    print(title, '-', t, '(s)')
    return res, t


kgc = KGC()
signers, t = timeit(lambda: kgc.KeyGen(), 'keygen')
print('----')

hash_inp = np.empty(0)
t_sign = 0
t_ver = 0
for device in range(M):
    print('id', device)
    message = os.urandom(70000)
    print(message)

    iot = IOT_device(signers['priv'][device], signers['pub'][device])
    sig, t = timeit(lambda: iot.LSign(msg=message), 'Lsign')
    t_sign += t

    print('priv', list(iot.sk))
    print('pub', iot.pk)
    print('signature', sig, "\n")

    agg = Aggregator(signers['priv'][-1], signers['pub'][-1])
    res, t = timeit(lambda: agg.LVer(message, sig, iot.pk), 'LVer')
    t_ver += t
    print('VERIFIED' if res else 'ROGUE')

    y = np.concatenate((sig[0], sig[1], sig[2]))
    hash_inp = np.concatenate((hash_inp, y))

    print('-------\n')

print('sign avg:', t_sign/M)
print('ver avg:', t_ver/M)
print(agg.AggSign(sha256(hash_inp).digest()))
