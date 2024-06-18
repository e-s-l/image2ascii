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

    # dy, dx, fraction

    FS_diffusion_matrix = [
        (0, 1, 7.0 / 16.0),
        (1, -1, 3.0 / 16.0),
        (1, 0, 5.0 / 16.0),
        (1, 1, 1.0 / 16.0)
    ]

    Atkinson_diffusion_matrix = [
        (0, 1, 1.0 / 8.0),
        (0, 2, 1.0 / 8.0),
        (1, -1, 1.0 / 8.0),
        (1, 0, 1.0 / 8.0),
        (1, 1, 1.0 / 8.0),
        (2, 0, 1.0 / 8.0)
    ]

    Burkes_diffusion_matrix = [
        (0, 1, 8.0 / 32.0),
        (0, 2, 4.0 / 32.0),
        (1, -2, 2.0 / 32.0),
        (1, -1, 4.0 / 32.0),
        (1, 0, 8.0 / 32.0),
        (1, 1, 4.0 / 32.0),
        (1, 2, 2.0 / 32.0)
    ]

    Sierra_lite_diffusion_matrix = [
        (0, 1, 2.0 / 4.0),
        (1, -1, 1.0 / 4.0),
        (1, 0, 1.0 / 4.0)
    ]

    diffusion_matrices = {"FS": FS_diffusion_matrix, "Sl": Sierra_lite_diffusion_matrix,
                         "At": Atkinson_diffusion_matrix, "Bu": Burkes_diffusion_matrix}

    diffusion_matrix = diffusion_matrices.get(algorithm)

    img_array = np.array(img, dtype=float)
    h, w = img_array.shape[:2]

    for i in range(h):
        for j in range(w):
            pix = img_array[i, j] / 255
            pix_new = get_closest(pix, channels)
            img_array[i, j] = pix_new
            err = pix - pix_new

            for dy, dx, fraction in diffusion_matrix:
                y, x = i + dy, j + dx
                if 0 <= y < h and 0 <= x < w:
                    img_array[y, x] += err * fraction

    return Image.fromarray((255 * img_array).astype(np.uint8))


def runner(args):
    """Main function to run all components."""

    channels = 6  # number of channels per RGB
    algorithm = "At"  # "FS", "At", "Sl", "Bu"

    # get input arguments
    img_file = args.image_in
    debug = args.debug

    # open (and preprocess) image file
    img = open_image(img_file, debug)

    # get & make filenames
    fileName, fileExtension = os.path.splitext(img_file)
    filename_new = f"{fileName}_dithered_{algorithm}.png"

    # get dimensions of original image
    w, h = img.size

    # get pixels from original image
    img_pix = img.load()

    # adjust image size
    ar = w / h
    w_new, h_new = 1920, round(1920 / ar)
    img = img.resize((w_new, h_new), Image.Resampling.LANCZOS)  # Lanczos filter anti-aliasing

    # apply dithering
    img_new = ditherer(img, channels, algorithm)

    # done...
    img_new.save(filename_new.format(channels))


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
    runner(input_args)
    sys.exit(0)

    try:
        if input_args.debug:
            os.system("figlet THE DITHERER")
        runner(input_args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print("Error running: \n", e)
        sys.exit(1)
