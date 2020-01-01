"""
CP467 Assignment 6 training vector generations - Kumiko Randle, Amardeep Sarang and Daniel Berezovski

=================
     READ ME
=================
First make sure you have python 3 installed.
Then make sure you have cv2 installed for python (pip install opencv-python==4.1.1.26).	
requires the training folder to be in the same directory
assumes the path to each tranning image will follow this format: training/digit/id.png example: training/0/2.png

run the program as follows:
python a6.py 

see a6.txt for output
"""
import cv2 as cv
import numpy as np
import sys

def divide(image):
	'''
	divide the image into 3x3 zones
	'''
	rows = image.shape[0]
	cols = image.shape[1]

	zones = list()

	columns = np.array_split(image, 3)

	for column in columns:
		zones.extend(np.array_split(column, 3, axis=1))

	return zones

def get_bw_ratio(zone):
	'''
	gives the ratio of black to white pixels in a 3x3 zone
	'''
	threshold = 127

	black_pixels = 0
	white_pixels = 0

	for i in range(zone.shape[0]):
		for j in range(zone.shape[1]):
			if zone[i][j] > 127:
				black_pixels += 1
			else:
				white_pixels += 1

	if white_pixels == 0:
		white_pixels = 1

	return black_pixels / white_pixels

def generate_feature_vector(zones):
	'''
	generates the feature vector, given a list of 3x3 zones in the image 
	'''
	feature_vector = list()

	for zone in zones:
		feature_vector.append(get_bw_ratio(zone))

	return feature_vector

def run(path):
	image = cv.imread(path)
	
	black_and_white_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	zones = divide(black_and_white_image)

	#print(digit, )
	return generate_feature_vector(zones)
	

def create_path():
	'''
	will create a path to each training image and will call the function to generate the feature vector
	'''
	init_path = "training/"
	f= open("a6.txt","w+")
	for digit in range(10):
		folder_path = init_path+str(digit)+"/"
		
		# not all id number exist, get atleast 100
		i=1
		count = 0
		while count <100:
			
			path = folder_path + str(i) + ".png"
			i=i+1
			count=count+1
		
			try:
				l = run(path)
				s = str(digit) + " " + str(l)+ "\n"
				print(s)
				f.write(s)
				
			except:
				
				count=count-1
				
	f.close()
			
			
create_path()