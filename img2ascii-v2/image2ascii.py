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

#######################
# control parameters:
debug = True   # print misc. outputs
printToConsole = False
printToFile = False
scale = int(20)     # scale factor to shrink image size
ASCIICHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"  # light to dark, left to right

############################################################

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


def bfs_search(matrix, start, tolerance):

    w, h = matrix.shape
    queue = [start]
    b_init = matrix[start]
    group = []
    visited = []

    while queue:
        x, y = queue.pop(0)
        visited.append((x, y))
        group.append((x, y))

        for i in range(max(0, x-1), min(w, x+2)):
            for j in range(max(0, y-1), min(h, y+2)):
                if (i, j) not in visited:
                    if abs(matrix[i, j] - b_init) <= tolerance:
                        queue.append((i, j))

    return group, visited


def find_shapes(matrix, tolerance):
    # BFS pathfinder to get subsets of similar brightness

    w, h = matrix.shape
    shapes = []
    visited = []

    for x in range(w):
        for y in range(h):
            if (x, y) not in visited:
                shape, newly_visited = bfs_search(matrix, (x, y), tolerance)
                shapes.append(shape)
                visited.extend(newly_visited)

    return shapes


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
            pixelRGB = img.getpixel(pos)    # get RGB
            R, G, B = pixelRGB
            # Calculate Brightness
            brightness = sum([R, G, B])/3
            # note: could (should?!) use luminance formula
            BM[X, Y] = brightness

    #
    if debug:
        print(BM)

    ######################

    shapes = find_shapes(BM, tolerance=10)
    print(len(shapes))

    sys.exit(1)


    #initialise
    ascii_matrix = np.full((w, h), ' ', dtype=str)

    # convert brightness into ascii
    for shape in shapes:
        b_av = np.mean([bm[x, y] for x, y in group])
        ascii_index = int((len(ASCIICHARS) - 1)*(b_av/255.0))
        ascii_value = ASCIICHARS[ascii_index]
        for x, y in group:
            ascii_matrix[x, y] = ascii_value

    #######################
    # print or save             #add option to print-save shape at a time
    output = ""
    for Y in range(H):
        for X in range(W):
            output += ascii_matrix[X, Y]
        output += "\n"
    #
    if debug:
        print(printToFile)
        print(printToConsole)

    #######################
    if printToFile:
        #####
        f = open("imageAsAscii.txt", "wt")
        f.write(output)
        f.close()
        if debug:
            print('printed to file')
    
    if printToConsole:
        ###
        print(output)
  
     
############################################################
def main():

    global printToConsole
    global printToFile

    # print to file or console:
    print("Would u like to print to file [1] or the console [2]?")
    while True:
        user_in = input().strip().lower()
        if user_in == "1" or user_in == "file":
            printToFile = True
            if debug:
                print("printing to file...")
            break
            ###
        elif user_in == "2" or user_in == "console":
            printToConsole = True
            if debug:
                print("printing to console...")
            break
            ###
        else:
            print("Please enter 1 or 2, or 'file' or 'console'...")

    # if cli usage is: ./image2ascii.py imagefile.png
    image_file = preprocess_image(sys.argv[1])

    #######################
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
