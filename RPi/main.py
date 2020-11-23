import logging
import logging.config
from io import BytesIO
import numpy as np
import time
import socket
import json
from datetime import datetime

from utils import piCamHandler, communicationThread

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
    ComThread = communicationThread(host='192.168.0.47', port=49152)
    PiCamera = piCamHandler(resolution=(608, 608), rotation=0)

    ComThread._open_socket()
    ComThread._connect_socket()
    PiCamera._open_camera()
    PiCamera._open_stream()

    try:
        while True:
            try:
                PiCamera.shoot()
                out = BytesIO()
                np.save(out, PiCamera.buffer)
                binary = out.getvalue()
                ComThread.send(binary)
                out.close()
                time.sleep(0.1)
            except socket.error:
                ComThread._close_conn()
                PiCamera._close_camera()
                ComThread._connect_socket()
                PiCamera._open_camera()
                PiCamera._open_stream()
            except KeyboardInterrupt:
                break
    finally:
        ComThread._close_conn()
        ComThread._close_socket()
        PiCamera._close_camera()
