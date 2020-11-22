import logging
from io import BytesIO
import numpy as np
import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
from datetime import datetime

logger = logging.getLogger(__name__)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]

    return recvall(sock, msglen)

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

if __name__=='__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.0.47', 49152))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        fig = plt.figure()

        for i in range(3):
            data = recv_msg(s)

            data = np.load(BytesIO(data), allow_pickle=True)
            plt.imshow(data)
            dt = datetime.now().strftime('%Y%m%d_%H%H%S')
            plt.savefig(f'output/'+ dt +'.png')
