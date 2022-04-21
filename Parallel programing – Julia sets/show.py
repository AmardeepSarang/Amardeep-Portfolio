'''
requires opencv
make sure you have cv2 installed for python (pip install opencv)
used pseudo code from: https://en.wikipedia.org/wiki/Julia_set#Pseudocode_for_normal_Julia_sets
'''
'''
import cv2
import numpy as np
import cmath
import System.Drawing as sd

def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

def main():
'''
   # ---------------------
   # Changeable parameters
#--------- -----------
'''
    #==============================
    width, height = 5000, 5000
    max_iteration = 50
    white =(255,255,255)
    image = create_blank(width, height, rgb_color=white)
    total_work= width*height
    work_done=0
    b = sd.Bitmap(width,height)
    f=open("julia_out.txt","r")
    for line in f:
        line_param = line.strip().split()
        
        i=int(line_param[0])
        j=int(line_param[1])
        itera=int(line_param[2])
        if itera==max_iteration:
            col=sd.Color.Black
        else:
            col=sd.Color.White
        bm.setPixel(i,j,col)
    bm.Save(PathWrite,sd.Imaging.ImageFormat.Bmp)
     
main()
'''
from PIL import Image

img = Image.new( 'RGB', (10000,10000), "black") # Create a new black image
pixels = img.load() # Create the pixel map
for i in range(img.size[0]):    # For every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # Set the colour accordingly

img.show()