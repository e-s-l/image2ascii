#!/usr/bin/python

#image2ascii.

##################
#based off: 
#https://medium.com/@shubham0473/unleash-your-inner-artist-a-step-by-step-guide-to-converting-images-to-ascii-art-using-java-97860464f19a
#and
#https://github.com/isaksolheim/image-to-ascii/blob/master/image_to_ascii.py
##################

##################
### TO DO:
#   exception handling
#   print to console
# 
##################

#imports:
import sys      #system stuff (to get input arguments)
import os       #operating system stuff (to get file extensions)
from PIL import Image      #'python image library' (for the processing)
import numpy as np          #for the usual


########
debug = False    #print misc. outputs
#
scale = 4     #shrink image size
#
ASCIICHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"  #liight to dark, left to right

############################################################

def preProcessImage(imgFile):
    ###
    # some minor preprocessing
    ###

    #
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

    #convert image to RBG type
    img = img.convert ('RGB')

    return img

############################################################

def img2AsciiConvertor(img, scale):

    #get img dimensions
    W,H = img.size

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

    #woudlnt really want 1 asciichar per pixel, but anyway...

    #####
    f = open("imageAsAscii.txt", "wt")
    #
    output = ""
    for Y in range(0,H):
        for X in range(0,W):
            brightness = BM[X,Y]
            asciiIndex = (int) ((len(ASCIICHARS) - 1) * (brightness / 255.0))
            asciiValue = ASCIICHARS[asciiIndex]
            output+=asciiValue+" "
        output+="\n"
    f.write(output)
    #
    f.close()


############################################################
def main():

    ###
    if len(sys.argv) != 2:
        print("Try: python image2ascii.py <image_file>")
        sys.exit(1)

    #if cli usage is: ./image2ascii.py imagefile.png
    image_file = preProcessImage(sys.argv[1])
    
    #
    img2AsciiConvertor(image_file, scale)


############################################################
#call initialisation function with input arg of image name
if __name__ == "__main__":
    main()
    print(":)")

###