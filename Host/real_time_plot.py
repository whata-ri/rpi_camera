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
        ax = fig.add_subplot(1,1,1)

        try:
            plt.ion()

            for i in range(10):
                data = recv_msg(s)

                data = np.load(BytesIO(data), allow_pickle=True)
                if i == 0:
                    im = ax.imshow(data)
                else:
                    im.set_data(data)
                plt.pause(0.1)
        finally:
            plt.ioff()