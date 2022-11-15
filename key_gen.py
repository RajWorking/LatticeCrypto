import time
import json

from src.roles import KGC
from src.config import *

kgc = KGC.KGC()

st = time.time()
signers = kgc.KeyGen()
print("Time: ", time.time() - st)

for i in range(N+1):
    keys = {}
    s1, s2 = signers['priv'][i]
    t, a, k = signers['pub'][i]

    keys["priv"] = {'s1': s1.tolist(), 's2': s2.tolist()}
    keys["pub"] = {'t': t.tolist(), 'a': a.tolist(), 'k': k.item()}

    with open('keys%d.json' % i, 'w') as f:
        f.write(json.dumps(keys))
