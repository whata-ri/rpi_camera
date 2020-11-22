import logging
from io import BytesIO
import numpy as np
import time
import socket

from utils import piCamHandler, communicationThread

logger = logging.getLogger(__name__)

if __name__=='__main__':
    ComThread = communicationThread(host='192.168.0.47', port=49152)
    PiCamera = piCamHandler(resolution=(608, 608), rotation=0)

    ComThread._open_socket()
    ComThread._connect_socket()
    PiCamera._open_camera()
    PiCamera._open_stream()

    out = BytesIO()
    try:
        while True:
            try:
                PiCamera.shoot()
                np.save(out, PiCamera.buffer)
                binary = out.getvalue()
                ComThread.send(binary)
                time.sleep(0.1)
            except socket.error:
                ComThread._close_conn()
                ComThread._connect_socket()
            except KeyboardInterrupt:
                break
    finally:
        ComThread._close_conn()
        ComThread._close_socket()
        PiCamera._close_camera()
