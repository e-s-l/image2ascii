#!/usr/bin/python

#image2ascii.

#based off: 
#https://medium.com/@shubham0473/unleash-your-inner-artist-a-step-by-step-guide-to-converting-images-to-ascii-art-using-java-97860464f19a
#and
#https://github.com/isaksolheim/image-to-ascii/blob/master/image_to_ascii.py

#imports:
import sys      #system stuff (to get input arguments)
import os       #operating system stuff (to get file extensions)
from PIL import Image      #'python image library' (for the processing)
import numpy as np          #for the usual


########

debug = True

############################################################

def img2AsciiConvertor(imgFile, scale):


    ###
    #exception handling for bad files
    #ideally will be able to take any image file type.

    fileName, fileExtension = os.path.splitext(imgFile)

    if (debug):
        print(fileName+'\n', fileExtension)

    ############################################################
    #pre-process the image file
    #open image file
    img = Image.open(imgFile)

    #resize image (and save and open new)
    W,H = img.size
    img.resize((W//scale, H//scale)).save(fileName+".resized%s" % fileExtension)
    
    #open the resized image
    img = Image.open(fileName+".resized%s" % fileExtension)
    W,H = img.size

    #convert image to RBG type
    img = img.convert ('RGB')


    ############################################################
    #convert image into brightness matrix (averaged rgb values for each pixel)


    #initialise (dark) matrix
    BM = np.zeros((W,H))

    for X in range(0,W):
        for Y in range(0,H):
            #Get RGB
            pixelRGB = img.getpixel((X,Y))
            R,G,B = pixelRGB 
            #Calculate Brightness
            brightness = sum([R,G,B])/3
            #note: could (should?!) use luminance formula
            BM[X,Y]= brightness
    
    #
    if debug:
        print(BM)

    ############################################################
    #convert brightness into ascii
    # from light to dark: `^\”,:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$   #67 != 26 lower case + 10 numerals + 33 special characters?

    #woudlnt really want 1 asciichar per pixel, but anyway...




    ##################

    ASCIICHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    #####

    f = open("imageAsAscii.txt", "wt")


    for Y in range(0,H):
        for X in range(0,W):
            brightness = BM[X,Y]
            asciiIndex = (int) ((len(ASCIICHARS) - 1) * (brightness / 255.0))
            asciiValue = ASCIICHARS[asciiIndex]
            f.write(asciiValue+" ")

        f.write('\n')

    #
    f.close()


############################################################
#call initialisation function with input arg of image name
if __name__ == "__main__":

    #if cli usage is: ./image2ascii.py imagefile.png
    scriptName = sys.argv[0]
    imgFile = sys.argv[1]
    #
    scaling = 3

    #main function (take an OO approach later)
    img2AsciiConvertor(imgFile, scaling)

    
