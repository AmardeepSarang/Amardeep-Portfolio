import cv2 as cv
import numpy as np
import sys

# splits image into 9 zones, and returns zones as a list of numpy arrays
def divide(image):
	rows = image.shape[0]
	cols = image.shape[1]

	zones = list()

	columns = np.array_split(image, 3)

	for column in columns:
		zones.extend(np.array_split(column, 3, axis=1))

	return zones

# returns the ratio of black pixels to white pixels in any given zone based on a brightness threshold of 127
def get_bw_ratio(zone):
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

# produces a feature vector from the black:white pixel ratios from each zone in the image
def generate_feature_vector(zones):
	feature_vector = list()

	for zone in zones:
		feature_vector.append(get_bw_ratio(zone))

	return np.array(feature_vector)

# prints feature vector of specified image
def main(path):
	image = cv.imread(path)

	black_and_white_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

	zones = divide(black_and_white_image)

	print(generate_feature_vector(zones))

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('you must provide an image path!')
		exit(0)
	elif len(sys.argv) == 2:
		main(sys.argv[1])