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
import random
from collections import deque   # doubled ended queue -  to reduce pop O
from collections import defaultdict #


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


def luminance(pix_rgb):
    """Given a set of rgb values of a pixel, calculate brightness."""

    r, g, b = pix_rgb
    return 0.299*r + 0.587*g + 0.114*b    # luminance formula


def bfs_search(matrix, start, tol, visited):
    """Breadth first search algorithm."""

    w, h = matrix.shape
    queue = deque([start])
    init = matrix[start]
    group = []

    while queue:
        x, y = queue.popleft()

        if not visited[x, y]:

            visited[x, y] = True
            group.append((x, y))

            for i in range(max(0, x-1), min(w, x+2)):
                for j in range(max(0, y-1), min(h, y+2)):
                    if not visited[i, j] and abs(matrix[i, j] - init) <= tol:
                        queue.append((i, j))

    return group


def find_shapes(matrix):
    """Use the bfs pathfinder to get subsets of similar brightness."""

    print("find_shapes")
    # initialise shapes and bfs stuff
    w, h = matrix.shape
    shapes = []     # list
    visited = np.zeros((w, h), dtype=bool)
    tol = 20

    # find shapes...
    for x in range(w):
        for y in range(h):
            if not visited[x, y]:
                shape = bfs_search(matrix, (x, y), tol, visited)
                shapes.append(shape)

    return shapes


def quick_sort(pixels):
    """Recursive quick sort algorithm for Nx1 array of pixs"""

    if not pixels:
        return pixels
    elif len(pixels) <= 1:
        return pixels
    else:
        pivot = pixels[0]
        # recursion...
        lower = quick_sort([pix for pix in pixels[1:] if (luminance(pix) < luminance(pivot))])
        higher = quick_sort([pix for pix in pixels[1:] if (luminance(pix) >= luminance(pivot))])
        return lower + [pivot] + higher

###


###

def runner(command_line_args):
    """Main function to run all components."""

    # get input arguments
    image_file = command_line_args.image_in
    debug = command_line_args.d

    # open (and preprocess) image file
    image = open_image(image_file)

    file_name, file_extension = os.path.splitext(image_file)

    # get dimensions of original image
    w, h = image.size

    # get pixels from original image
    img_pixs = image.load()

    # initialise new image
    new_image = Image.new('RGB', (w, h))

    # initialise brightness martix
    bm = np.zeros((w, h))

    # fill out the brightness matrix
    for x in range(w):
        for y in range(h):

            p = (x, y)
            pix = img_pixs[p]
            bm[x, y] = luminance(pix)

    # based on the brightness, find shapes/areas of similar brightness
    shapes = find_shapes(bm)

    ###

    for shape in shapes:

        rows = defaultdict(list)

        for x, y in shape:
            rows[y].append((x, y))

        rows = dict(rows)


        all_pixels = []
        all_sorted = []


        for y, coords in rows.items():


            all_pixels.append([])

            for x, y in coords:

                 all_pixels.append(img_pixs[(x, y)])

            sorted_pixels = quick_sort(all_pixels)

            for i, (x, y) in enumerate(coords):
                new_image.putpixel((x, y), sorted_pixels[i])

           # all_sorted.append(quick_sort(all_pixels[y]))

           # for i in range(len(coords)):
           #     p = coords[i]
           #     new_image.putpixel(p, all_sorted[y][i])

    ###

    # save end product
    new_image.save("%s_deranged.png" % file_name)
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
        os.system("figlet THE DERANGER")
        #runner(args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print("Error running: \n", e)
        sys.exit(1)
