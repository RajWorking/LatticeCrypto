import socket
from _thread import *
import threading
import json
import numpy as np
from sys import argv
from src.roles import Agg
from src.config import *

print_lock = threading.Lock()
msg_array = []

f = open('keys.json', 'r')
obj = json.load(f)
f.close()

sk = np.array([obj['priv']['s1'], obj['priv']['s2']])
pk = (np.array(obj['pub']['t']), obj['pub']['a'], obj['pub']['k'])
agg = Agg.Aggregator(sk, pk)


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

    while True:
        data = recvall(conn, 4)
        if not data:
            break

        print_lock.acquire()

        len = int.from_bytes(data, 'big')
        data = json.loads(recvall(conn, len).decode())

        print('from: ', addr)

        z1 = np.array(data['sig']['z1'])
        z2 = np.array(data['sig']['z2'])
        c = np.array(data['sig']['c'])
        sig = (z1, z2, c)
        msg = data['msg']
        pk = (np.array(data['pk']['t']),
              np.array(data['pk']['a']),
              data['pk']['k'])

        print('message: ', msg)
        print('verified: ', agg.LVer(msg.encode(), sig, pk))

        msg_array += [msg]

        print_lock.release()

    conn.close()


def main():
    global msg_array
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
            print(msg_array)
            msg_array = []


if __name__ == '__main__':
    main()
