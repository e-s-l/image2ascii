#!/usr/bin/python3

###############
# IMAGE DITHER: #
###############

# IMPORTS #
import argparse                         # To process command line arguments.
import os                               # For terminal actions.
from PIL import Image                   # Python Image Library.
import sys                              # To exit the program, etc.
import numpy as np                      # For matrix maths.
from collections import deque           # double-ended queue -  to reduce pop O
from collections import defaultdict     # to initialise empty dict


def open_image(img_file, debug):
    """Use PIL to open image and convert to RGB form."""
    if debug:
        print("open_image")

    # open image file
    try:
        img = Image.open(img_file)
    except IOError as ioe:
        print("Error opening the image file: \n", ioe)
        sys.exit(1)

    # convert image to RGB type
    img = img.convert('RGB')

    return img


def get_closest(pix, channels):
    return np.round(pix * (channels - 1)) / (channels - 1)


def ditherer(img, channels, algorithm):

    # img_dithered = img

    img_array = np.array(img, dtype=float)

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pix = img_array[i, j]
            pix_new = get_closest(pix, channels)
            img_array[i, j] = pix_new
            err = pix - pix_new

            img_array[i, j + 1] = err * 7.0 / 16.0
            img_array[i + 1, j - 1] = err * 3.0 / 16.0
            img_array[i + 1, j] = err * 5.0 / 16.0
            img_array[i + 1, j + 1] = err * 1.0 / 16.0

    return Image.fromarray(img_array)


def runner(args):
    """Main function to run all components."""

    # get input arguments
    img_file = args.image_in
    debug = args.debug

    # open (and preprocess) image file
    img = open_image(img_file, debug)
    # get file name w/o extension
    fileName, fileExtension = os.path.splitext(img_file)
    filename_new = f"{fileName}_dithered.png"

    # get dimensions of original image
    w, h = img.size

    if debug:
        print("Img size (in pix): w, h: ", w, h)

    # get pixels from original image
    img_pix = img.load()

    # later...
    # adjust size to common webpage sizes...
    # ie full-screen or mobile media queries maximals...
    w_new = w  # some common pixel count
    h_new = h  #

    img = img.resize((w_new, h_new), Image.Resampling.LANCZOS)  # Lanczos filter anti-aliasing

    channels = 3  # number of channels per RGB
    algorithm = "FS"        # Floyd-Steinberg
    # would also like to implement: Jarvis-Judice-Ninke (JJN), Stucki, Burkes, Sierra (3 kinds)...

    img_new = ditherer(img, channels, algorithm)





    # done...
    img_new.save(filename_new)


if __name__ == '__main__':
    # PARSE INPUT ARGUMENTS #
    # Initialise argument parser:
    parser = argparse.ArgumentParser(description='Takes an image file and dither it a la error diffusion.')
    # Add arguments:
    parser.add_argument('image_in', type=str, help='Image file to process.')  # Required
    parser.add_argument('--debug', action='store_true', help='Option to enable debug mode.')   # Optional

    # Parse:
    input_args = parser.parse_args()

    # START RUNNING MAIN PROGRAM #
    try:
        if input_args.debug:
            os.system("figlet THE DITHERER")
        runner(input_args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print("Error running: \n", e)
        sys.exit(1)
