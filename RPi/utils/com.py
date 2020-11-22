import threading
import logging
import socket
import struct

logger = logging.getLogger('picamera.com')

class communicationThread(threading.Thread):
    def __init__(self, host: str, port: int=49152):
        """Com handler between PC and RPI

        Args:
            host (str): IP address of RPI
            port (int, optional): Port number of RPI. Defaults to 49152.
        """
        self._host = host
        self._port = port
        self._socket = None
        self._conn = None

    def _open_socket(self):
        if self._socket:
            logger.info('socket already exists')
            return False
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self._host, self._port))
            logger.info('bind socket to host and port')
            return True

    def _connect_socket(self):
        if self._conn:
            logger.info('connection already exists')
            return False
        else:
            logger.info('connecting to client...')
            self._socket.listen()
            self._conn, addr = self._socket.accept()
            logger.info('connected to the device: address({})'.format(addr))
            return True

    def _close_socket(self):
        if self._socket:
            if self._conn:
                self._conn.close()
            self._socket.close()
            self._socket = None
            self._conn = None
            logger.info('socket closed')
            return True
        else:
            logger.info('socket does not exist')
            return False

    def _close_conn(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.info('connection closed')
            return True
        else:
            logger.info('connection does not exist')
            return False

    def send(self, data):
        if self._conn:
            msg = struct.pack('>I', len(data)) + data
            self._conn.sendall(msg)
        else:
            logger.warn('No connection to host computer!')

    def run(self):
        self._open_socket()
        self._connect_socket()
        while True:
            try:
                #Todo self._conn.send(# camera data)
                pass
            except socket.error:
                self._close_conn()
                self._connect_socket()
                logger.info('reopen connection')
            except KeyboardInterrupt:
                break