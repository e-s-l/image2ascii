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
#   
##################

#imports:
import sys      #system stuff (to get input arguments)
import os       #operating system stuff (to get file extensions)

try:
    from pillow import Image      #'python image library' (for the processing)
except ModuleNotFoundError as mne:
    try:
        from PIL import Image
    except  ModuleNotFoundError as mne:
        print("required packages unavailable:", mne)
        sys.exit(1)
            
import numpy as np          #for the usual


########
debug = False   #print misc. outputs
###
#control parameters:
global printToConsole
global printToFile
printToFile = False
printToConsole = False
#
scale = int(5)     #scale factor to shrink image size
#
ASCIICHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"  #light to dark, left to right

############################################################

def preProcessImage(imgFile):
    #######################
    # some minor preprocessing
    ###
    fileName, fileExtension = os.path.splitext(imgFile)

    if (debug):
        print(fileName+'\n', fileExtension)
    
    #######################
    #open image file
    try:
        img = Image.open(imgFile)       
    except IOError as e:
        print("Error opening the image file:", e)
        print("Are u sure this is an image file? Better start again...")
        sys.exit(1)
    
    #######################
    #Resize the image according to the output:
    W,H = img.size
    if (printToConsole):
        #get console size
        console_width = os.get_terminal_size().columns
        aspect_ratio = W / H
        new_height = int(console_width / aspect_ratio)
        #resize
        img = img.resize((console_width, new_height)) 
    ###
    if (printToFile):
        img = img.resize((W//scale, H//scale))

    #######################
    #convert image to RBG type
    img = img.convert('RGB')

    return img

############################################################

def img2AsciiConvertor(img):

    #get img (new) dimensions (again)
    W,H = img.size

    #######################
    #convert image into brightness matrix (averaged rgb values for each pixel)

    #initialise (dark) matrix
    BM = np.zeros((W, H))

    for X in range(0,W):
        for Y in range(0,H):
            #Get RGB
            pixelRGB = img.getpixel((X,Y))
            R,G,B = pixelRGB 
            #Calculate Brightness
            brightness = sum([R,G,B])/3
            #note: could (should?!) use luminance formula
            BM[X, Y]= brightness 
    #
    if debug:
        print(BM)

    #######################
    #convert brightness into ascii
    #woudlnt really want 1 asciichar per pixel, but anyway...
    #######################
    output = ""
    for Y in range(0,H):
        for X in range(0,W):
            brightness = BM[X,Y]
            asciiIndex = (int) ((len(ASCIICHARS) - 1) * (brightness / 255.0))
            asciiValue = ASCIICHARS[asciiIndex]
            output+=asciiValue
        output+="\n"
    #
    if (debug):
        print(printToFile)
        print(printToConsole)

    #######################
    if (printToFile):
        #####
        f = open("imageAsAscii.txt", "wt")
        f.write(output)
        f.close()
        if (debug):
            print('printed to file')
    
    if (printToConsole):
        ###
        print(output)
  
     
############################################################
def main():

    global printToConsole
    global printToFile

    ###
    if len(sys.argv) != 2:
        print("Try: python image2ascii.py <image_file>")
        sys.exit(1)

    #print to file or console:
    print("Would u like to print to file [1] or the konsole [2]?")
    while(True):
        user_in = input().strip().lower()
        if user_in == "1" or user_in == "file":
            printToFile = True
            if (debug):
                print("printing to file...")
            break
            ###
        elif user_in == "2" or user_in == "console":
            printToConsole = True
            if (debug):
                print("printing to console...")
            break
            ###
        else:
            print("Please enter 1 or 2, or file or console...")

    #if cli usage is: ./image2ascii.py imagefile.png
    image_file = preProcessImage(sys.argv[1])

    #######################
    #call the runner
    img2AsciiConvertor(image_file)

############################################################
#call initialisation function with input arg of image name
if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        print("\nexiting...")
        sys.exit(0)
    except Exception as e:
        print("There is an error:", e)
        sys.exit(1)
    print(":)")

###
