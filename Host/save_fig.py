import logging
from io import BytesIO
import numpy as np
import socket
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

from utils import recv_msg, recvall

applogger = logging.getLogger('picamera')
applogger.setLevel(logging.INFO)
shandler = logging.StreamHandler()
shandler.setLevel(logging.INFO)
applogger.addHandler(shandler)
now = datetime.now().strftime('%y%m%d%H%M%S')
filename = './log/' + now + '.log'
fhandler = logging.FileHandler(filename, delay=True)
fformat = logging.Formatter('%(asctime)s::%(levelname)s::%(name)s - %(message)s')
fhandler.setFormatter(fformat)
fhandler.setLevel(logging.DEBUG)
applogger.addHandler(fhandler)

if __name__=='__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.0.47', 49152))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        fig = plt.figure()

        for i in range(3):
            data = recv_msg(s)

            data = np.load(BytesIO(data), allow_pickle=True)
            plt.imshow(data)
            dt = datetime.now().strftime(f'%Y%m%d_%H%H%S_{i}')
            plt.savefig(f'output/'+ dt +'.png')
