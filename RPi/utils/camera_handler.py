import logging
import time
import picamera
import picamera.array
import numpy as np

logger = logging.getLogger(__name__)

class piCamHandler():
    def __init__(self, resolution=(608, 608), rotation=180):
        self.buffer = None
        self.camera = None
        self.stream = None
        self.resolution = resolution
        self.rotation = rotation

    def _open_camera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = self.resolution
        self.camera.rotation = self.rotation
        logger.info('Successfully open the camera')
        print('Successfully open the camera')

    def _close_camera(self):
        if self.camera:
            if self.stream:
                self._close_stream()
            self.camera.close()
            logger.info('Successfully close the camera')
            print('Successfully close the camera')
        else:
            logger.info('No camera opened')
            print('No camera opened')

    def _open_stream(self):
        if not self.camera:
            self._open_camera()
        self.stream = picamera.array.PiRGBArray(self.camera)
        logger.info('Successfully open the stream')
        print('Successfully open the stream')

    def _close_stream(self):
        if self.stream:
            self.stream.close()
            logger.info('Successfully close the stream')
            print('Successfully close the stream')
        else:
            logger.info('No stream opened')
            print('No stream opened')

    def shoot(self):
        if not self.camera:
            logger.info('open the camera first')
            print('open the camera first')
            return False
        if not self.stream:
            logger.info('open the stream first')
            print('open the stream first')
            return False
        self.camera.capture(self.stream, 'rgb', use_video_port=True)
        self.buffer = self.stream.array
        self.stream.truncate(0)
        return True
