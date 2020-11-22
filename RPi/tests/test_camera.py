import picamera
import picamera.array

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

with picamera.PiCamera() as camera:

    camera.resolution = (600, 600)
    camera.rotation = 180
    camera.start_preview()
    time.sleep(2)

    with picamera.array.PiRGBArray(camera) as stream:
        start_time = time.time()
        camera.capture(stream, 'rgb', use_video_port=True)
        elapsed = time.time() - start_time
        print(elapsed)
        plt.figure()
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.imshow(stream.array)
        plt.savefig('test.png')
        print('finished output image')
