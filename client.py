import socket
import sys
import numpy as np
import json
from src.roles import IOT
from src.config import *

f = open('keys.json', 'r')
obj = json.load(f)
f.close()

sk = np.array([obj['priv']['s1'], obj['priv']['s2']])
pk = (np.array(obj['pub']['t']), np.array(obj['pub']['a']), obj['pub']['k'])
iot = IOT.IOT_device(sk, pk)
print(pk[2])

s = socket.socket()
s.connect((sys.argv[2], int(sys.argv[1])))

print('Type "exit" to quit the program.')
while True:
    msg = input(">>>  ")
    if msg == 'exit':
        break

    sig = iot.LSign(msg=msg.encode())
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


s.close()
