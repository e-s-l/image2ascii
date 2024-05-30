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
#   fix saving shapes to file
#
##################

# imports:
import sys                  # system stuff (to get input arguments)
import os                   # operating system stuff (to get file extensions)
from PIL import Image       # Python Image Library
import numpy as np          # for the usual

###################
# control parameters:
debug = False   # print misc. outputs
printToConsole = False
printToFile = False
bfs_grouping = False

##################

scale = int(20)
tolerance = 50

##################
# The character array to map brightness to:
ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
WOW_SNR = "123456789ABCDEFGHIJKLMNOPQRSTU"
# light to dark, left to right
char_map = WOW_SNR
##################

print_shapes = True
save_shapes = False

##################

use_luminance_form = True


############################################################
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


############################################################
def get_brightness(r, g, b):
    # Given a set of rgb values of a pixel, calculate brightness
    # brightness = sum([r, g, b])/3             # simple average
    brightness = 0.299*r + 0.587*g + 0.114*b    # luminance formula
    return brightness


############################################################
def bfs_search(matrix, start, tol):
    # breadth first seach algorithm

    w, h = matrix.shape
    queue = [start]

    b_init = matrix[start]
    group = []
    visited = np.zeros((w, h), dtype=bool)

    while queue:
        x, y = queue.pop(0)

        if not visited[x, y]:

            visited[x, y] = True
            group.append((x, y))

            for i in range(max(0, x-1), min(w, x+2)):
                for j in range(max(0, y-1), min(h, y+2)):
                    if not visited[i, j] and abs(matrix[i, j] - b_init) <= tol:
                        queue.append((i, j))

    return group, visited


############################################################
def find_shapes(matrix, tol):
    # BFS pathfinder to get subsets of similar brightness

    w, h = matrix.shape
    shapes = []
    visited = np.zeros((w, h), dtype=bool)

    for x in range(w):
        for y in range(h):
            if not visited[x, y]:
                shape, newly_visited = bfs_search(matrix, (x, y), tol)
                shapes.append(shape)
                visited = visited | newly_visited

    return shapes


############################################################
def get_output(matrix):
    # for printing the character matrix as plain text

    W, H = matrix.shape
    output = ""
    for Y in range(H):
        for X in range(W):
            output += matrix[X, Y]
        output += "\n"

    return output


############################################################
def print_output_to_console(matrix):

    output = get_output(matrix)
    print(output)


############################################################
def save_output_to_file(matrix, file):

    output = get_output(matrix)
    f = open(file, "wt")
    f.write(output)
    f.close()


############################################################
def img2ascii_convertor(img):

    #######################

    # convert image into brightness matrix (averaged rgb values for each pixel)
    # get img (new) dimensions (again)
    W, H = img.size
    # initialise (dark) matrix
    BM = np.zeros((W, H))

    for X in range(W):
        for Y in range(H):
            pos = (X, Y)                    # get position
            pixel_rgb = img.getpixel(pos)    # get RGB
            r, g, b = pixel_rgb
            BM[X, Y] = get_brightness(r, g, b)
    #
    if debug:
        print("BM")
        print(BM)

    ######################

    # initialise (empty) matrix
    char_matrix = np.full((W, H), ' ', dtype=str)

    if bfs_grouping:
        if debug:
            print("finding shapes")

        shapes = find_shapes(BM, tolerance)
        shape_num = 0
        if debug:
            print("num of shapes =", len(shapes))
        for shape in shapes:
            # initialise (empty) matrix
            shape_matrix = np.full((W, H), ' ', dtype=str)
            shape_num += 1
            #
            for x, y in shape:
                # find character for average brightness of the group:
                b_av = np.mean([BM[x, y] for x, y in shape])
                shape_matrix[x, y] = get_char_from_b(b_av)
                # add to the culminative total matrix:
                char_matrix[x, y] = shape_matrix[x, y]

            if printToFile and save_shapes:
                save_output_to_file(shape_matrix, "./shapes/shape_%i.txt" % shape_num)
            elif printToConsole and print_shapes:
                print_output_to_console(shape_matrix)


    else:   # no BFS shape finder...
        for Y in range(H):
            for X in range(W):
                char_matrix[X, Y] = get_char_from_b(BM[X, Y])

    ###
    if printToFile:
        save_output_to_file(char_matrix, "imageAsAscii.txt")
    elif printToConsole:
        print_output_to_console(char_matrix)

############################################################
def get_char_from_b(brightness):
    # convert brightness into ascii:
    index = int((len(char_map) - 1) * (brightness / 255.0))
    return char_map[index]


############################################################
def process_user_input():

    #
    global printToConsole
    global printToFile
    global bfs_grouping
    global char_map

    # confirm require image file supplied
    if len(sys.argv) != 2:
        print("Try: python image2ascii.py <image_file>")
        sys.exit(1)

    # ask for options:
    # print to file or console...
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
    opts_in_bfs = {"1", "bfs", ""}
    opts_in_no_bfs = {"2", "no"}
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

    # which character map to use:
    opts_in_ascii = {"1", "ascii", ""}
    opts_in_snr = {"2", "snr"}
    print("Would u like to map to ascii characters [1] or snr values [2]?")
    while True:
        user_in = input().strip().lower()
        if user_in in opts_in_ascii or user_in in opts_in_snr:
            if user_in in opts_in_ascii:
                char_map = ASCII_CHARS
            else:
                char_map = WOW_SNR
            if debug:
                print("mapping to ", "ascii" if user_in in opts_in_ascii else "snr")
            break
            ###
        else:
            print("Please enter 1 or 2, or 'ascii' or 'snr'...")


############################################################
def main():

    process_user_input()
    #######################
    # if cli usage is: ./image2ascii.py imagefile.png
    image_file = preprocess_image(sys.argv[1])
    # call the runner
    img2ascii_convertor(image_file)

############################################################


# call initialisation function with input arg of image name
if __name__ == "__main__":
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
