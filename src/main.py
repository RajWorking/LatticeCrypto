from hashlib import sha256
import numpy as np
import time
from config import *
from Agg import Aggregator
from IOT import IOT_device
from KGC import KGC
# import sys
# np.set_printoptions(threshold=sys.maxsize)


def timeit(code, title):
    st = time.time()
    res = code()
    end = time.time()
    print(title, '-', end - st, '(s)')
    return res


kgc = KGC()
signers = timeit(lambda: kgc.KeyGen(), 'keygen')
print('----')

hash_inp = np.empty(0)
for device in range(M):
    print('id', device)

    iot = IOT_device(signers['priv'][device], signers['pub'][device])
    sig = timeit(lambda: iot.LSign(msg=b'hello'), 'Lsign')

    # print('signature', sig, "\n")

    agg = Aggregator(signers['priv'][-1], signers['pub'][-1])
    res = timeit(lambda: agg.LVer(b'hello', sig, iot.pk), 'LVer')
    print('VERIFIED' if res else 'ROGUE')

    y = np.concatenate((sig[0], sig[1], sig[2]))
    hash_inp = np.concatenate((hash_inp, y))

    print('-------\n')

print(agg.AggSign(sha256(hash_inp).digest()))
