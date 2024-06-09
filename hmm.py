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

    # convert image to RGB type
    img = img.convert('RGB')

    return img

def get_brightness(pix_rgb):
    """Given a set of rgb values of a pixel, calculate brightness."""
    print("get_brightness")
    r, g, b = pix_rgb
    return 0.299*r + 0.587*g + 0.114*b    # luminance formula

def bfs_search(matrix, start, tol, visited):
    """Breadth first search algorithm."""
    print("bfs_search")

    h, w = matrix.shape
    queue = [start]
    init = matrix[start]
    group = []

    while queue:
        x, y = queue.pop(0)

        if not visited[x, y]:
            visited[x, y] = True
            group.append((x, y))

            for i in range(max(0, x-1), min(h, x+2)):
                for j in range(max(0, y-1), min(w, y+2)):
                    if not visited[i, j] and abs(matrix[i, j] - init) <= tol:
                        queue.append((i, j))

    return group

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

    # initialise a brightness numpy matrix
    bm = np.zeros((img_h, img_w))

    # initialise shapes and bfs stuff
    shapes = []
    visited = np.zeros((img_h, img_w), dtype=bool)
    tol = 1

    for x in range(img_w):
        for y in range(img_h):
            p = (x, y)
            rgb = img_pix[p]

            # 1: flip colors...
            new_pix = (255-rgb[0], 255-rgb[1], 255-rgb[2])

            # 2: get brightness...
            bm[y, x] = get_brightness(new_pix)

            # find shapes...
            if not visited[y, x]:
                shape = bfs_search(bm, (y, x), tol, visited)
                shapes.append(shape)

    shape_num = 0

    for shape in shapes:
        if debug:
            shape_num += 1
            print(shape_num)

        for y, x in shape:
            b_av = np.mean([bm[yi, xi] for yi, xi in shape])

            # make new image
            p = (x, y)
            new_pix = (int(b_av), int(b_av), int(b_av))
            new_image.putpixel(p, new_pix)

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
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print("Error running: \n", e)
        sys.exit(1)