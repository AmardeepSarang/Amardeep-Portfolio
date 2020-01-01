"""
CP467 Assignment 4 - Kumiko Randle, Amardeep Sarang and Daniel Berezovski

=================
     READ ME
=================
First make sure you have python 3 installed.
Then make sure you have cv2 installed for python (pip install opencv-python==4.1.1.26).
Do not try to scale symbol up to a point were its edge will be off the image, in this case it won't show
Can work with multiple symbols in 1 image

run the program as follows:
python a4.py [path to image] [x scaling dimension] [y scaling dimension]

"""
import sys
import cv2
import numpy as np


def open_image(path):
    """
    Opens the image at the given path, reading it in as a grayscale image. Then we convert the pixel values (0 to 255)
    to a decimal number (0.0 to 1.0).
    :param path: path to image location
    :return: 2d array of pixel values (0.0 to 1.0)
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Could not find image at specified path.")
        exit(0)
    return cv2.normalize(img.astype("float"), None, 0.0, 1.0, cv2.NORM_MINMAX)


def convert_to_bw(img):
    """
    Converts all pixels in an image to black (0) or white (255)
    :param img: 2d array of pixel values representing an image
    :return: 2d array of pixels containing only 0 or 255
    """
    bw_img = np.where(img >= 0.5, 1.0, 0.0)

    return bw_img


def display_image(original, filtered):
    """
    Given two images, display them side by side. The images have pixel values as decimal numbers ranging from 0.0 to
    1.0. The cv2 library automatically converts this back to 0 to 255 pixel values.
    """
    cv2.imshow("original vs filtered image", np.hstack((original, filtered)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def fit_image_to_screen(img, max_width=900, max_height=600):
    """
    Rescales an image in both axes to fit within the dimensions of most monitors.
    """
    img_height = img.shape[0]
    if img_height > max_height:
        scale = max_height / img_height
        img = rescale_image(img, scale)

    img_width = img.shape[1]
    if img_width > max_width:
        scale = max_width / img_height
        img = rescale_image(img, scale)

    return img


def rescale_image(img, scale):
    """
    Rescales image in both axes based on scale.
    """
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)
    rescaled = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return rescaled


def scale_symbol(img, x_scale_dem, y_scale_dem):
    """
    Rescales each symbol in image according the x and y dimensions given
    Code from stackoverflow user Howard GENG used as template
    https://stackoverflow.com/questions/53489267/how-to-scale-down-symbols-in-an-image-using-open-cv
    """
    _, im_th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(255-im_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #get bounding rectangle
    num_imgs=[]
    num_points=[]
    
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        num_img=img[y:y+h, x:x+w]
        size=num_img.shape
        if(size[0]>3 and size[1]>3):# avoids noise pixels
            num_imgs.append(img[y:y+h, x:x+w])
            num_points.append((x, y))
            
        
    # resize images and put it back
    output_img = np.ones_like(img) * 255

   #scale down each symbol
    for (i, num_im) in enumerate(num_imgs):
    
        num_im = cv2.resize(num_im, (x_scale_dem,y_scale_dem), interpolation=cv2.INTER_AREA)
        (img_h, img_w) = num_im.shape[:2]
        #get place to insert in new image
        btm_x, btm_y = num_points[i]
        x1 = btm_x 
        y1 = btm_y
        x2 = x1 + img_w
        y2 = y1 + img_h

        if(output_img[y1:y2, x1:x2].shape != num_im.shape):
            #check for out of bound, don't print an image if it will be out bounds of original image
            print("Symbol {} falls of the image, please chose a smaller scaling factor!".format(i))
        else:
            output_img[y1:y2, x1:x2] = num_im #put into new image at same spot

    return output_img

def main(path, x_scale, y_scale):
    img = fit_image_to_screen(open_image(path))
    bw_img = convert_to_bw(img)
    bw_img = (bw_img * 255).astype('uint8')

    output_img=scale_symbol(bw_img, x_scale, y_scale)
    display_image(bw_img,output_img)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough arguments, using default")
        main("digits.jpg",9,9)
    else:
        main(sys.argv[1], int(sys.argv[2]),int(sys.argv[3]))