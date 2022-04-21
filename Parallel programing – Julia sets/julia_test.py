'''
requires opencv
make sure you have cv2 installed for python (pip install opencv)
used pseudo code from: https://en.wikipedia.org/wiki/Julia_set#Pseudocode_for_normal_Julia_sets
'''
import cv2
import numpy as np
import cmath
def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image

def scale_value(old_value, old_max, old_min, new_max, new_min):
  return ( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
  
def main():
    '''
    ---------------------
    Changeable parameters
    --------- -----------
    '''
    #==============================
    width, height = 1000, 1000
    R = 4#escape radius

    cx, cy = 0.360284,0.100376
    #==============================


    #colors
    white = (255, 255, 255)
    black = (0,0,0)

    image = create_blank(width, height, rgb_color=white)
    total_work= width*height
    work_done=0
    for i in range(height):
        for j in range(width):
            ycord = height-1-i#filp y cord 
            #put 0,0 at center
            y = ycord - height/2
            x = j - width/2


            #scale coordinates to be between -R and R
            zx = scale_value(x,width/2, -1*width/2, R, -1*R)
            zy = scale_value(y, height/2, -1*height/2, R, -1*R)

            
            iteration = 0
            max_iteration = 50

            #do all ops using complex number
            while zx * zx + zy * zy < R**2  and iteration < max_iteration:
                xtemp = zx * zx - zy * zy
                zy = 2 * zx * zy + cy
                zx = xtemp + cx

                iteration = iteration + 1
                
                
            #color pixel
            if iteration == max_iteration:
                image[i][j] = black

            
            work_done = work_done + 1
        
        #print % complete
        per=work_done/total_work
        print("{:.2%}".format(per))
     
    #save image to file   
    cv2.imwrite('test.jpg', image)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
main()