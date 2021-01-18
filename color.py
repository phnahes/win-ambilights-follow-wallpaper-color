#
# Dependencies
# numpy   1.19.3
# Pillow  8.1.0
# scipy   1.6.0
#
# Useful informations:
# https://stackoverflow.com/a/3244061/6644766
# https://stackoverflow.com/a/29643643/6644766

from PIL import Image
from PIL import ImageColor
from __future__ import print_function
import binascii
import numpy as np
import re
import scipy
import scipy.cluster
import scipy.misc
import serial
import struct

WALLPAPER_DIR = r'C:\Users\Paulo'
COMPLETE_DIR = WALLPAPER_DIR + '\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper' # For Windows 10
#COMPLETE_DIR = WALLPAPER_DIR + '\AppData\Roaming\Microsoft\Windows\Themes\TranscodedWallpaper' # For Windows 7

NUM_CLUSTERS = 5

SERIAL_BAUDRATE = "9600" 
SERIAL_PORT     = "COM8" 

def send_to_board(value):
    port = SERIAL_PORT
    baud_rate = SERIAL_BAUDRATE

    com = serial.Serial()
    com.port = port
    com.baudrate = baud_rate
    com.timeout = 0.1
    com.writeTimeout = 0
    com.setDTR(False)
    com.open()
    com.write(bytes(value + '\n', encoding="ascii"))
    com.close()

def detect_color():
    print('reading image')
    im = Image.open(COMPLETE_DIR)
    im = im.resize((150, 150))      # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')

    print('most frequent is %s (#%s)' % (peak, colour))
    rgb_color = str(ImageColor.getcolor('#' + colour, "RGB"))
    rgb_color = rgb_color.replace(",", " ").replace("(", "").replace(")", "")

    print("Setting color: " + rgb_color)
    return(rgb_color)


send_to_board(detect_color())

