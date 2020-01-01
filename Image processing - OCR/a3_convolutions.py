import cv2 as cv
import numpy as np
import sys

# applies 3x3 mean convoluion to pixel defined by its row and column
# returns the pixel's new value
def apply_mean_filter_to_pixel(image, row, col):
	rows = image.shape[0]
	cols = image.shape[1]

	start_row = row - 1 if row > 0 else 0
	end_row = row + 1 if row < rows - 1 else rows - 1

	start_col = col - 1 if col > 0 else 0
	end_col = col + 1 if col < cols - 1 else cols - 1

	new_value_r = 0
	new_value_g = 0
	new_value_b = 0

	for i in range(start_row, end_row + 1):
		for j in range(start_col, end_col + 1):
			new_value_r += image[i][j][0]
			new_value_g += image[i][j][1]
			new_value_b += image[i][j][2]

	return np.array([new_value_r / 9, new_value_g / 9, new_value_b / 9])

# applies either a row or column mean filter to the pixel at the specifed location in the image
# returns new pixel value
def apply_separate_filter_to_pixel(image, row, col, filter):
	rows = image.shape[0]
	cols = image.shape[1]

	new_value_r = 0
	new_value_g = 0
	new_value_b = 0

	if filter == 'row':
		start_col = col - 1 if col > 0 else 0
		end_col = col + 1 if col < cols - 1 else cols - 1

		for i in range(start_col, end_col + 1):
			new_value_r += image[row][i][0]
			new_value_g += image[row][i][1]
			new_value_b += image[row][i][2]
	elif filter == 'col':
		start_row = row - 1 if row > 0 else 0
		end_row = row + 1 if row < rows - 1 else rows - 1

		for i in range(start_row, end_row + 1):
			new_value_r += image[i][col][0]
			new_value_g += image[i][col][1]
			new_value_b += image[i][col][2]

	return np.array([new_value_r / 3, new_value_g / 3, new_value_b / 3])

# uses apply_mean_filter_to_pixel for each pixel to smooth the entire image
# returns smoothed image
def apply_mean_filter(path):
	image = cv.imread(path)

	rows = image.shape[0]
	cols = image.shape[1]

	for row in range(rows):
		for col in range(cols):
			image[row][col] = apply_mean_filter_to_pixel(image, row, col)

	return image

# uses apply_separate_filter_to_pixel to first apply a row filter, and then a column filter to the entire image
# returns new image
def apply_separate_filters(path):
	image = cv.imread(path)
	
	rows = image.shape[0]
	cols = image.shape[1]

	for row in range(rows):
		for col in range(cols):
			image[row][col] = apply_separate_filter_to_pixel(image, row, col, 'row')

	for row in range(rows):
		for col in range(cols):
			image[row][col] = apply_separate_filter_to_pixel(image, row, col, 'col')

	return image

# runs both types of smoothing, and displays new images side by side for comparison
def main(path):
	mean_filter_image = apply_mean_filter(path)
	separate_fiters_image = apply_separate_filters(path)

	horizontal_stack = np.hstack((cv.imread(path), mean_filter_image, separate_fiters_image))

	cv.imshow('original vs mean vs separate', horizontal_stack)
	cv.waitKey(0)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('you must provide an image path!')
		exit(0)
	elif len(sys.argv) == 2:
		main(sys.argv[1])