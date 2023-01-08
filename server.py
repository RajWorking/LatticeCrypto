import socket
import time
from _thread import *
import threading
import json
import numpy as np
from collections import Counter
from sys import argv
from src.roles import Agg
from src.config import *

print_lock = threading.Lock()
msg_array = []
chunk_agg = b''

f = open('keys.json', 'r')
obj = json.load(f)
f.close()

sk = np.array([obj['priv']['s1'], obj['priv']['s2']])
pk = (np.array(obj['pub']['t']), obj['pub']['a'], obj['pub']['k'])
agg = Agg.Aggregator(sk, pk)
print('Public parameter k: ', pk[2])


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def threaded(conn, addr):
    global msg_array
    global chunk_agg

    hist = []
    i = 0
    while True:
        data = recvall(conn, 4)
        if not data:
            break

        print(i)
        if i >= 999:
            break
        i += 1

        print_lock.acquire()

        sz = int.from_bytes(data, 'big')
        data = json.loads(recvall(conn, sz).decode())

        # print('\nFrom: ', addr)

        z1 = np.array(data['sig']['z1'])
        z2 = np.array(data['sig']['z2'])
        c = np.array(data['sig']['c'])
        sig = (z1, z2, c)
        msg = data['msg']
        pk = (np.array(data['pk']['t']),
              np.array(data['pk']['a']),
              data['pk']['k'])

        st = time.time()
        ok = agg.LVer(msg.encode(), sig, pk)
        time_ver = time.time() - st

        print("Verification Time: ", time_ver, "s")
        # print('Message: ', msg)
        print('message size (bytes): ', len(msg))
        # print('Verified: ', ok)
        
        time_ver = int(time_ver * 1000)
        hist.append(time_ver)

        msg_array += [msg]
        chunk = b''.join([z1.tobytes(), z2.tobytes(),
                         c.tobytes(), msg.encode()])
        chunk_agg = b''.join([chunk_agg, chunk])

        print_lock.release()

    print(Counter(hist))

    conn.close()


def main():
    global msg_array
    global chunk_agg
    s = socket.socket()

    s.bind(('', int(argv[1])))
    s.listen(N)

    print("Server is listening")

    for _ in range(N):
        conn, addr = s.accept()
        start_new_thread(threaded, (conn, addr))

    print("all devices connected")

    while True:
        if len(msg_array) >= N:

            print("\nMessages: ")

            for msg in msg_array:
                print(msg)

            print("Chunk size: ", len(chunk_agg))

            st = time.time()
            sig = agg.AggSign(chunk_agg)
            print("Aggregate Signing Time: ", time.time() - st, "s")

            st = time.time()
            ok = agg.VerASign(chunk_agg, sig)
            print("Aggregate Verification Time: ", time.time() - st, "s")
            # print("Verified: ", ok)

            msg_array = []
            chunk_agg = b''


if __name__ == '__main__':
    main()
