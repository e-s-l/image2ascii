#!/usr/bin/python

###############
# PIXEL SORT: #
###############

# IMPORTS #
import argparse         # To process command line arguments.
import os               # For terminal actions.
from PIL import Image   # Python Image Library.
import sys              # To exit the program, etc.
import numpy as np      # For matrix maths.


# FUNCTIONS #

def open_image(image_file):
    """Use PIL to open image and convert to RGB form."""
    print("open_image")

    # open image file
    try:
        img = Image.open(image_file)
    except IOError as ioe:
        print("Error opening the image file: \n", ioe)
        sys.exit(1)

    # convert image to RBG type
    img = img.convert('RGB')

    return img


def runner(command_line_args):
    """Main function to run all components."""
    print("runner")

    # get input arguments
    image_file = command_line_args.image_in
    debug = command_line_args.d

    # open (and preprocess) image file
    image = open_image(image_file)
    # get dimensions of original image
    img_w, img_h = image.size
    # get pixels from original image
    img_pix = image.load()
    # initialise new image
    new_image = Image.new('RGB', (img_w, img_h))

    # 1: flip colors...
    for x in range(img_w):
        for y in range(img_h):
            p = (x, y)
            rgb = img_pix[p]
            new_image.putpixel(p, (255-rgb[0], 255-rgb[1], 255-rgb[1]))

    # save end product
    new_image.save("deranged_image.png")
    # close original image file
    image.close()
    #
    print(":)")


if __name__ == '__main__':

    ###
    # PARSE INPUT ARGUMENTS #
    # Initialise argument parser:
    parser = argparse.ArgumentParser(description='Takes an image file and deranges it a la pixel sorting.')

    # Add arguments:
    parser.add_argument('image_in', type=str, help='Image file to process.')  # Required
    parser.add_argument('--d', action='store_true', help='Option to enable debug mode.')   # Optional

    # Parse:
    args = parser.parse_args()

    ###
    # START RUNNING MAIN PROGRAM #
    runner(args)

    try:
        os.system("figlet -f future THE DERANGER")
        # runner(args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print("Error running: \n", e)
        sys.exit(1)
