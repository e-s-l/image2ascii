#!/usr/bin/python

####################################
# MAKE MP4 FROM PIXEL SORTED IMAGES:
####################################

# IMPORTS #
import argparse                 # To process command line arguments.
import os                       # to get file name and extension
import imageio.v2 as imageio    # to make the .mp4 file
import subprocess               # recommended over os for system calls  #but really should import other file...

# parse image arguments
parser = argparse.ArgumentParser(description='Takes an image file and deranges it a la pixel sorting, then creates a '
                                             'mp4 by combing all the outputs of the pixel sort program.')
parser.add_argument('image_in', type=str, help='Image file to process.')
args = parser.parse_args()

# get image info.
image_file = args.image_in
file_name, file_extension = os.path.splitext(image_file)

# parameters for loops
tol_max = 200
tol_step = 10
tolerances = []
filenames = []

# start loop, run pixel sort with increasing tolerances
for t in range(0, tol_max, tol_step):

    print(f't = {t}')
    subprocess.call(f'python3 pixel_sort.py {image_file} --tolerance {t}', shell=True)
    filenames.append(f'{file_name}_deranged_t{t}.png')


# combine these images into a mp4
writer = imageio.get_writer(f'{file_name}_deranged.mp4', fps=10)

for filename in filenames:
    writer.append_data(imageio.imread(filename))

writer.close()

# fin
