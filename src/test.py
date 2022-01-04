from hashlib import sha256
import numpy as np
import time
from config import *
from Agg import Aggregator
from IOT import IOT_device
from KGC import KGC


def timeit(code, title):
    st = time.time()
    res = eval(code)
    end = time.time()
    print(title, '-', end - st, '(s)')
    return res


kgc = KGC()
signers = timeit("kgc.KeyGen()", 'keygen')
print('----')

hash_inp = np.empty(0)
for device in range(M):
    iot = IOT_device(signers['priv'][device], signers['pub'][device])
    sig = timeit("iot.LSign(msg=b'hello')", 'Lsign')

    agg = Aggregator(signers['priv'][-1], signers['pub'][-1])
    res = timeit("agg.LVer(b'hello', sig, iot.pk)", 'LVer')
    print(device, 'Verified' if res else 'Illegal')

    y = np.concatenate((sig[0], sig[1], sig[2]))
    hash_inp = np.concatenate((hash_inp, y))

print(agg.AggSign(sha256(hash_inp).digest()))
print(np.sum(signers['priv'][0] - signers['priv'][1]))
