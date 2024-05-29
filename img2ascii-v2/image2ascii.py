#!/usr/bin/python

# image2ascii.

##################
# based off:
# https://medium.com/@shubham0473/unleash-your-inner-artist-a-step-by-step-guide-to-converting-images-to-ascii-art-using-java-97860464f19a
# and
# https://github.com/isaksolheim/image-to-ascii/blob/master/image_to_ascii.py
# and
# https://www.youtube.com/watch?v=wUQbchYY80U
##################

##################
# TO DO:
#   exception handling
#   add a search algorithm to group areas
#   use luminance formula
##################

# imports:
import sys                  # system stuff (to get input arguments)
import os                   # operating system stuff (to get file extensions)
from PIL import Image       # Python Image Library
import numpy as np          # for the usual

###################
# control parameters:
debug = True   # print misc. outputs
printToConsole = False
printToFile = False
bfs_grouping = False
print_shapes = True
scale = int(100)     # scale factor to shrink image size
tolerance = 200
ASCIICHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"  # light to dark, left to right

##################


def preprocess_image(img_file):
    # some minor preprocessing

    img = None  # initialise
    fileName, fileExtension = os.path.splitext(img_file)

    if debug:
        print(fileName+'\n', fileExtension)
    ##################

    # open image file
    try:
        img = Image.open(img_file)
    except IOError as ioe:
        print("Error opening the image file: \n", ioe)
        print("Are u sure this is an image file? Better start again...")
        sys.exit(1)
    
    ##################
    # Resize the image according to the output:
    W, H = img.size
    if debug:
        print('W, H =', (W, H))

    if printToConsole:
        # get console size
        console_width = os.get_terminal_size().columns
        aspect_ratio = W/H
        new_height = int(console_width/aspect_ratio)
        # resize
        img = img.resize((console_width, new_height)) 
    ###
    if printToFile:
        img = img.resize((W//scale, H//scale))

    #######################
    # convert image to RBG type
    img = img.convert('RGB')

    return img


def get_brightness(r, g, b):
    # Given a set of rgb values of a pixel, calculate brightness
    # brightness = sum([r, g, b])/3             # simple average
    brightness = 0.299*r + 0.587*g + 0.114*b    # luminance formula
    return brightness


def bfs_search(matrix, start, tol):

    w, h = matrix.shape
    queue = [start]
    b_init = matrix[start]
    group = set()
    visited = set()

    while queue:
        x, y = queue.pop(0)
        visited.add((x, y))
        group.add((x, y))

        for i in range(max(0, x-1), min(w, x+2)):
            for j in range(max(0, y-1), min(h, y+2)):
                if (i, j) not in visited and abs(matrix[i, j] - b_init) <= tol:
                    queue.append((i, j))

    return group, visited


def find_shapes(matrix, tol):
    # BFS pathfinder to get subsets of similar brightness

    w, h = matrix.shape
    shapes = []
    visited = set()

    for x in range(w):
        for y in range(h):
            if (x, y) not in visited:
                shape, newly_visited = bfs_search(matrix, (x, y), tol)
                shapes.append(shape)
                visited.update(newly_visited)

    return shapes


def save_output(matrix, file):
    # print or save
    W, H = matrix.shape
    output = ""
    for Y in range(H):
        for X in range(W):
            output += matrix[X, Y]
        output += "\n"
    #
    if debug:
        print(printToFile)
        print(printToConsole)

    #######################
    if printToFile:  # make this a function so can call on shapes
        #####
        f = open(file, "wt")
        f.write(output)
        f.close()
        if debug:
            print('printed to file')

    if printToConsole:
        ###
        print(output)


def img2ascii_convertor(img):

    # get img (new) dimensions (again)
    W, H = img.size

    #######################
    # convert image into brightness matrix (averaged rgb values for each pixel)

    # initialise (dark) matrix
    BM = np.zeros((W, H))

    for X in range(0, W):
        for Y in range(0, H):
            pos = (X, Y)                    # get position
            pixelrgb = img.getpixel(pos)    # get RGB
            r, g, b = pixelrgb
            BM[X, Y] = get_brightness(r, g, b)

    #
    if debug:
        print(BM)

    ######################

    # initialise (empty) matrix
    ascii_matrix = np.full((W, H), ' ', dtype=str)

    # convert brightness into ascii
    if bfs_grouping:
        shapes = find_shapes(BM, tolerance)
        shape_num = 0
        if debug:
            print("num of shapes =", len(shapes))
        for shape in shapes:
            shape_num += 1
            b_av = np.mean([BM[x, y] for x, y in shape])
            ascii_index = int((len(ASCIICHARS) - 1)*(b_av/255.0))
            ascii_value = ASCIICHARS[ascii_index]
            for x, y in shape:
                ascii_matrix[x, y] = ascii_value
            if print_shapes:
                save_output(ascii_matrix, "shape_%i.txt" % shape_num)
    else:
        for Y in range(H):
            for X in range(W):
                brightness = BM[X, Y]
                asciiIndex = int((len(ASCIICHARS) - 1) * (brightness / 255.0))
                ascii_matrix[X, Y] = ASCIICHARS[asciiIndex]

    #######################
    save_output(ascii_matrix, "imageAsAscii.txt")


############################################################
def main():

    global printToConsole
    global printToFile
    global bfs_grouping

    # print to file or console:
    opts_in_file = {"1", "file"}
    opts_in_console = {"2", "console", ""}
    print("Would u like to print to file [1] or the console [2]?")
    while True:
        user_in = input().strip().lower()
        if user_in in opts_in_file or user_in in opts_in_console:
            printToFile = user_in in opts_in_file
            printToConsole = user_in in opts_in_console
            if debug:
                print("printing to", "file..." if printToFile else "console...")
            break
            ###
        else:
            print("Please enter 1 or 2, or 'file' or 'console'...")

    # use BFS to find shapes or not:
    opts_in_bfs = {"1", "bfs"}
    opts_in_no_bfs = {"2", "no", ""}
    print("Would u like to use BFS shape grouping [1] or not [2]?")
    while True:
        user_in = input().strip().lower()
        if user_in in opts_in_bfs or user_in in opts_in_no_bfs:
            bfs_grouping = user_in in opts_in_bfs
            if debug:
                print("bfs grouping", "applied" if bfs_grouping else "not applied")
            break
            ###
        else:
            print("Please enter 1 or 2, or 'bfs' or 'no'...")

    #######################
    # if cli usage is: ./image2ascii.py imagefile.png
    image_file = preprocess_image(sys.argv[1])
    # call the runner
    img2ascii_convertor(image_file)

############################################################


# call initialisation function with input arg of image name
if __name__ == "__main__":

    ###
    if len(sys.argv) != 2:
        print("Try: python image2ascii.py <image_file>")
        sys.exit(1)

    try:
        main()
    except KeyboardInterrupt:
        print("\nexiting...")
        sys.exit(0)
    except Exception as e:
        print("There is an error: \n", e)
        sys.exit(1)
    print(":)")

###
