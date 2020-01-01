"""
CP467 Assignment 8 - Kumiko Randle, Daniel Berezovski and Amardeep Sarang

=================
     READ ME
=================
First make sure you have python 3 installed.
Then make sure you have cv2 installed for python (pip install opencv-python==4.1.1.26)
and numpy scipy (python -m pip install --user numpy scipy)

run the program as follows:
python a8_glow.py [path to image]
"""
import sys

import cv2
import math
import numpy as np
import scipy.stats as st

edge_filter = np.array([
    (0, 1, 0),
    (1, -4, 1),
    (0, 1, 0)
])

box_filter = np.arange(49).reshape(7, 7)

# Blurs image by taking weighted average of nearby pixels
large_gaussian_filter = 1/273.0 * np.array([
    (1, 4, 7, 4, 1),
    (4, 16, 26, 16, 4),
    (7, 26, 41, 26, 7),
    (4, 16, 26, 16, 4),
    (1, 4, 7, 4, 1)
])


def generate_gaussian(size, sigma):
    """
    Generates gaussian filter
    :param size: size of matrix
    :param sigma:
    :return:
    """
    x = np.linspace(-sigma, sigma, size+1)
    one_dim_kernel = np.diff(st.norm.cdf(x))
    two_dim_kernel = np.outer(one_dim_kernel, one_dim_kernel)
    return two_dim_kernel/two_dim_kernel.sum()


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


def convert_to_bw(img, threshold):
    """
    Converts all pixels in an image to black (0) or white (255)
    :param img: 2d array of pixel values representing an image
    :param threshold: value between 0.0 and 1.0, all pixels > threshold become 1.0, all less become 0.0.
    :return: 2d array of pixels containing only 0 or 255
    """
    bw_img = np.where(img >= threshold, 1.0, 0.0)

    return bw_img


def display_image(img):
    """
    Displays an image
    :param img: 2d array of pixel values representing an image
    :return: None
    """
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_regions(img):
    """
    Finds all connected regions of black pixels in an image
    :param img: 2d array of pixel values representing an image
    :return: tuples of number of black pixels in region and mean pixel location
    """
    padding_offset = 1
    id = -1
    id_map = {}
    segmented_img = np.pad(img, (padding_offset, padding_offset), "constant", constant_values=(1.0, 1.0))

    for y in range (padding_offset, img.shape[0] + padding_offset):
        for x in range (padding_offset, img.shape[1] + padding_offset):
            if segmented_img[y, x] == 0.0: # pixel is black
                # give pixel an id
                segmented_img[y, x] = id

                # add pixel to id_map
                id_map[id] = [(y, x)]

                # merge with all neighbours previously visited
                center_id = segmented_img[y, x]
                neighbour_locations = [(y-1, x), (y, x-1), (y-1, x-1)]
                neighbour_ids = [segmented_img[pos] for pos in neighbour_locations]

                for (neighbour_location, neighbour_id) in zip(neighbour_locations, neighbour_ids):
                    merge_neighbour(center_id, neighbour_id, neighbour_location, segmented_img, id_map)

                # decrement id by 1
                id -= 1

    return id_map


def merge_neighbour(center_id, neighbour_id, neighbour_location, segmented_img, id_map):
    """
    Merges lists of neighbouring pixels if they are connected
    """
    # Only have to merge if ids are not the same
    if center_id != neighbour_id:
        # make neighbour same id as center
        segmented_img[neighbour_location] = center_id

        # make all pixels with neighbour id same as center id
        if neighbour_id in id_map:
            for pos in id_map[neighbour_id]:
                segmented_img[pos] = center_id
            id_map[center_id] += id_map[neighbour_id]
            del id_map[neighbour_id]


def extract_section(img, y, x, filter_size):
    """
    Given an x and y coordinate of an image, selects the pixels of a section which is centered at x, y and has width and
    height equal to filter_size
    """
    x_min = x - filter_size[0]//2
    x_max = x + filter_size[0]//2 + 1
    y_min = y - filter_size[1]//2
    y_max = y + filter_size[1]//2 + 1
    return img[y_min:y_max, x_min:x_max]


def apply_filter_to_pixel (img, img_filter, y, x):
    """
    Given an x and y coordinate of an image, extracts a section equal to the filter size centered at x, y and applies
    filter to section. This is done by taking the product of each element in the filter with its corresponding element
    in the section and then summing over all products.
    """
    filter_size = img_filter.shape
    img_section = extract_section(img, y + filter_size[0]//2, x + filter_size[1]//2, filter_size)
    filtered_section = img_section * img_filter
    new_pixel = filtered_section.sum()

    return new_pixel


def apply_filter(img, filter):
    """
    Applies filter to an image
    """
    img_size = img.shape
    filter_size = filter.shape
    new_image = np.zeros(img_size)  # creates array of zeros equal to dimensions of original image

    # creates padded image to deal applying filter to edge pixels
    # pads image by extending edges, not with zeros
    padded_img = np.pad(img, (filter_size[0] // 2, filter_size[1] // 2), "edge")

    print("Applying filters...")

    # iterates through each pixel in image and applies a filter centered at that pixel
    for y in range(img_size[0]):
        for x in range(img_size[1]):
            new_image[y, x] = apply_filter_to_pixel(padded_img, filter, y, x)

    return new_image


def glow(img, colour):
    """
    Adds a glowing effect to an image in given colour
    """
    colour_img = convert_to_colour(img)
    inverted_img = (1 - colour_img) * 100
    return ((100 - inverted_img ) * colour + inverted_img)/100


def convert_to_colour(img):
    """
    Converts an image to colour
    """
    return np.stack((img,) * 3, axis=-1)


def overlay_images(original_img, glow_img):
    """
    Overlays glow image on original image to create glow effect
    """
    orig_colour_img = convert_to_colour(original_img)
    return np.where(orig_colour_img==1, glow_img, orig_colour_img)


def rescale_image(img, scale):
    """
    Rescales image in both axes based on scale.
    """
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)
    rescaled = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return rescaled


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


def main(path):
    img = fit_image_to_screen(open_image(path))
    bw_img = convert_to_bw(img, threshold=0.5)

    outlines = apply_filter(bw_img, edge_filter)
    temp1 = np.where(outlines > 0, 1.0, 0.0)
    thickened_outlines = apply_filter(temp1, box_filter)
    temp2 = np.where(thickened_outlines > 0, 1.0, 0.0)
    blurred_outlines = apply_filter(temp2, generate_gaussian(size=9, sigma=0.1))
    glowing_outlines = glow(blurred_outlines, np.array([238/255, 238/255, 175/255]))

    final_img = overlay_images(bw_img, glowing_outlines)

    # Display glowing outlines
    display_image(final_img)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("you must provide an image path!")
        exit(0)
    else:
        main(sys.argv[1])