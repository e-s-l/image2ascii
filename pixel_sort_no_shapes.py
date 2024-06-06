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


def get_brightness(pix_rgb):
    """Given a set of rgb values of a pixel, calculate brightness."""
   # print("get_brightness")
    r, g, b = pix_rgb
    return 0.299*r + 0.587*g + 0.114*b    # luminance formula


def bfs_search(matrix, start, tol, visited):
    """Breadth first search algorithm."""
    print("bfs_search")

    w, h = matrix.shape
    queue = [start]
    init = matrix[start]
    group = []

    while queue:
        x, y = queue.pop(0)

        if not visited[x, y]:

            visited[x, y] = True
            group.append((x, y))

            for i in range(max(0, x-1), min(w, x+2)):
                for j in range(max(0, y-1), min(h, y+2)):
                    if not visited[i, j] and abs(matrix[i, j] - init) <= tol:
                        queue.append((i, j))

    return group


def quick_sort(pixels):
    """Recursive quick sort algorithm for Nx1 array of pixs"""

    if not pixels:
        return pixels
    else:
        pivot = pixels[0]
        # recursion...
        lower = quick_sort([pix for pix in pixels[1:] if (get_brightness(pix) < get_brightness(pivot))])
        higher = quick_sort([pix for pix in pixels[1:] if (get_brightness(pix) >= get_brightness(pivot))])
        return lower + [pivot] + higher



def find_shapes(matrix):
    """Use the bfs pathfinder to get subsets of similar brightness."""

    print("find_shapes")
    # initialise shapes and bfs stuff
    w, h = matrix.shape
    shapes = []
    visited = np.zeros((w, h), dtype=bool)
    tol = 10

    # find shapes...
    for x in range(w):
        for y in range(h):
            if not visited[x, y]:
                shape = bfs_search(matrix, (x, y), tol, visited)
                shapes.append(shape)

    return shapes


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
    # img_pix = image.load()
    img = image.convert('RGB')


    # initialise new image
    new_image = Image.new('RGB', (img_w, img_h))



    # initialise a brightness numpy matrix
    bm = np.zeros((img_w, img_h))
   # bavm = bm



    for x in range(img_w):
        for y in range(img_h):

            p = (x,y)
            img_pix = img.getpixel(p)
            rgb = img_pix

            # 1: flip colors...
            new_pix = (255-rgb[0], 255-rgb[1], 255-rgb[2])

            img.putpixel(p, new_pix)
            # 2: get brightness...
             bm[x, y] = get_brightness(new_pix)





    shapes = find_shapes(bm)

    shape_num = 0

    for shape in shapes:

        if debug:
            shape_num += 1
            print(shape_num)

        for x, y in shape:
            # average the brightness over the shape
            # b_av = np.mean([bm[x, y] for x, y in shape])
            bavm[x, y] = bm[x, y]*random.uniform(0, shape_num)

    '''

    for x in range(img_w):
        for y in range(img_h):
            # make new image
            p = (x, y)
            pix = int(bavm[x, y])
            new_pix = (random.randint(0, pix), random.randint(0, pix), random.randint(0, pix))
            new_image.putpixel(p, new_pix)

    '''

    # quick sort all image pixels
    # 1. create array of all pixels:

    all_pixels =[]

    for x in range(img_w):
        all_pixels.append([])
        for y in range(img_h):
            p = (x,y)
            img_pix = img.getpixel(p)
            all_pixels[x].append(img_pix)

    # 2. sort pixels
    all_sorted = []

    for x in range(img_w):
        all_sorted.append(quick_sort(all_pixels[x]))

    # 3. save pixels
    for x in range(img_w):
        for y in range(img_h):
            p = (x, y)
            new_image.putpixel(p, all_sorted[x][y])



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
        os.system("figlet THE DERANGER")
        #runner(args)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print("Error running: \n", e)
        sys.exit(1)
