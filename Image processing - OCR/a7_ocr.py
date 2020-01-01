"""
CP467 Assignment 7 OCR - Kumiko Randle, Amardeep Sarang and Daniel Berezovski

=================
     READ ME
=================
First make sure you have python 3 installed.
Then make sure you have cv2 installed for python (pip install opencv-python==4.1.1.26).
Do not try to scale symbol up to a point were its edge will be off the image, in this case it won't show

run the program as follows:
python a7.py [path to image] [path to vector file ] [scale value x] [scale value y] [k]

"""
import sys
import cv2
import numpy as np
import math
from _operator import itemgetter
from random import randint,choice



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

def convert_to_wb(img):
    """
    Converts all pixels in an image to black (0) or white (255)
    :param img: 2d array of pixel values representing an image
    :return: 2d array of pixels containing only 0 or 255
    """
    bw_img = np.where(img >= 0.5, 0.0, 1.0)

    return bw_img



def display_image(img):
    """
    Given an image, display it. The images have pixel values as decimal numbers ranging from 0.0 to
    1.0. The cv2 library automatically converts this back to 0 to 255 pixel values.
    """
    cv2.imshow("Prediction", img)
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
    _, im_th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(255-im_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #get bounding rectengle
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
    bounding_box_cord=[]#gives the cords for each bounding box
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
            #check for out of boud, don't print an image if it will be out bounds of original image
            print("Symbol {} falls of the image, please chose a smaller scaling factor!".format(i))
        else:
            output_img[y1:y2, x1:x2] = num_im #put into new image at same spot
            bounding_box_cord.append((x1,x2,y1,y2))
    return output_img, bounding_box_cord

def divide(image):
    rows = image.shape[0]
    cols = image.shape[1]

    zones = list()

    columns = np.array_split(image, 3)

    for column in columns:
        zones.extend(np.array_split(column, 3, axis=1))

    return zones

def get_bw_ratio(zone):
    threshold = 0.5

    black_pixels = 0
    white_pixels = 0

    for i in range(zone.shape[0]):
        for j in range(zone.shape[1]):
            if zone[i][j] > threshold:
                black_pixels += 1
            else:
                white_pixels += 1

    if white_pixels == 0:
        white_pixels = 1

    return black_pixels / white_pixels

def generate_feature_vector(zones):
    feature_vector = list()

    for zone in zones:
        feature_vector.append(get_bw_ratio(zone))

    return np.array(feature_vector)

def get_feature_vector(path):
    '''
    Gets stored feature vectors of symbols from a file
    '''
    f = open(path, "r")
    if f is None:
        print("Could not find feature vector file at specified path.")
        exit(0)
    feature_vector=[]
    for line in f:
        num = int(line[0])#extract digit class
        
        vec = line[4:len(line)-2].split(",")
    
        #convert to float
        new_vec=[]
        for i in vec:
            new_vec.append(float(i))
        new_vec = normalize(new_vec)
        new_vec.append(num)
        #print(new_vec)
        feature_vector.append(new_vec)
    
    return feature_vector
def normalize(vec):
    v_max = max(vec)
    v_min = min(vec)
    new_vec=[]

    for i in vec:
        new_vec.append((i - v_min)/(v_max-v_min))
    return new_vec

def euclidean_distance(a,b,length):
    '''
    calculates euclidean distance
    '''
    dist=0
    for i in range(length-1):
        dist+=pow(a[i]-b[i], 2)
        
        
    return math.sqrt(dist)

def k_nn_prediction(prediction_subject,trainng_set,k):
    '''
    returns prediction for prediction subject
    prediction_subject - single row of test set
    trainng_set - entire traing set
    k - number of neighbors that vote
    '''
    dist_and_outcomes=[]
    
    
    #record distance and out come for each row of training set
    for train_row in trainng_set:
        dist_and_outcomes.append([euclidean_distance(prediction_subject, train_row,len(prediction_subject)),train_row[len(train_row)-1]])
    
    #sort by distance
    dist_and_outcomes=sorted(dist_and_outcomes, key=itemgetter(0))
    
    #get first k votes
    votes=[]
    for i in range(k):
        votes.append(dist_and_outcomes[i][1])
    
    return vote_count(votes)

def vote_count(votes):
    '''
    count votes and returns most voted
    '''
    counts=[0,0,0,0,0,0,0,0,0,0]
    key=[0,1,2,3,4,5,6,7,8,9]
    for v in votes:
        counts[int(v)-1]+=1
    max_i=0;
    max_v=counts[0]
    for i in range(len(counts)):
        if counts[i]>max_v:
            max_i=i
            max_v=counts[i]
    
    tie_votes=[]
    for i in range(len(counts)):
        if max_v==counts[i]:
            tie_votes.append(i)
    
    if len(tie_votes)==1:
        #no tie
        i=tie_votes[0]
        result=key[i]
    else:
        #tie, break at random
        i=choice(tie_votes)
    result=key[i]
    return result

def draw_text(img, text, location):
    """

    :param img:
    :param text:
    :param location:
    :return:
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.8
    fontColor = (0, 0, 255)
    lineType = 1

    cv2.putText(img, text,
                location,
                font,
                fontScale,
                fontColor,
                lineType)

def main(path,vec_file, x_scale, y_scale,k):
    img = fit_image_to_screen(open_image(path))
    bw_img = convert_to_bw(img)
    bw_img = (bw_img * 255).astype('uint8')
    #scale images
    scale_img, bounding_box=scale_symbol(bw_img, x_scale, y_scale)

    feat_vecs=get_feature_vector(vec_file)#get stored feature vectors
    
    scale_img_rgb = cv2.cvtColor(scale_img,cv2.COLOR_GRAY2RGB)#for  color text
    
    for cord_set in bounding_box:
        #extract each symbol
        x1, x2, y1, y2 = cord_set
        symbol = scale_img[y1:y2, x1:x2]

        
        #We are normally working with black digits and white background. 
        #get_bw_ratio function was made for white digits and black background. 
        #So this if function to switch black digits and white background to white digits and black background.
        black_and_white_image = convert_to_wb(symbol)

        #get ratio vectors for cerrent symbol in image
        zones = divide(black_and_white_image)
        current_feat_vec=generate_feature_vector(zones)
        
        #get predicted class of image.
        # when k-nn is set to k = 1 it is just calculating simply euclidean distance
        # can be set k > 1 with more data
        prediction_num=k_nn_prediction(current_feat_vec,feat_vecs,k)

        #overlay prediction on image
        draw_text(scale_img_rgb,str(prediction_num),(x1,y2))

    display_image(scale_img_rgb)

        



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Not enough arguments, using default")
        main("digits.jpg","a6.txt",9,9,3)
    else:
        
        main(sys.argv[1],sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
