import os
import socket
import sys
import time
import numpy as np
import json
from collections import Counter
from src.roles import IOT
from src.config import *

f = open('keys.json', 'r')
obj = json.load(f)
f.close()

sk = np.array([obj['priv']['s1'], obj['priv']['s2']])
pk = (np.array(obj['pub']['t']), np.array(obj['pub']['a']), obj['pub']['k'])
iot = IOT.IOT_device(sk, pk)
print('Public parameter k: ', pk[2])

s = socket.socket()
s.connect(('127.0.0.1', int(sys.argv[1])))

print('Type "exit" to quit the program.\n')
while True:
    msg = input(">>>  ")
    if msg == 'exit':
        break

    #####
    # testing message sizes
    msg_len =  20000  # 256 KB
    #####

    #####
    # testing number of messages
    num = 1000 # int(msg) # 4
    hist = []
    #####

    timesum = 0
    for _ in range(num):

        #####
        # random message
        msg = (os.urandom(msg_len)).hex()
        #####

        st = time.time()
        sig = iot.LSign(msg=msg.encode())
        end = time.time()
        print(end - st)
        time_sign = int((end - st) * 1000)
        hist.append(time_sign)

        z1, z2, c = sig

        sig = {'z1': z1.tolist(),
               'z2': z2.tolist(),
               'c': c.tolist()}

        data = {'sig': sig,
                'msg': msg,
                'pk': obj['pub']}

        sz = len(json.dumps(data).encode())  # length of object
        s.sendall(sz.to_bytes(4, byteorder='big'))
        s.sendall(json.dumps(data).encode())

    print("Signing Time Histogram: (s)")
    print(Counter(hist))

s.close()
