"""
CP467 Assignment 2 - Kumiko Randle, Daniel Berezovski and Amardeep Sarang

=================
     READ ME
=================
First make sure you have python 3 installed.
Then make sure you have cv2 installed for python (pip install opencv-python==4.1.1.26).

run the program as follows:
python a2_connected_regions.py [path to image]
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


def draw_text(img, text, location):
    """
    Draws text on an image
    :param img: 2d array of pixel values representing an image
    :param text: string to be drawn on image
    :param location: pixel location where text will be drawn
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    fontColor = (0, 0, 255)
    lineType = 1

    cv2.putText(img, text,
                location,
                font,
                fontScale,
                fontColor,
                lineType)


def find_mean_location(id_map):
    """
    Finds mean location in an array of pixels
    """
    region_size_and_mean = []
    for key in id_map:
        mean_location = (0, 0)
        pixels = id_map[key]
        for (py, px) in pixels:
            mean_location = (mean_location[0] + px, mean_location[1] + py)
        mean_location = (mean_location[0] // len(pixels), mean_location[1] // len(pixels))
        region_size_and_mean.append((len(pixels), mean_location))

    return region_size_and_mean


def main(path):
    img = fit_image_to_screen(open_image(path))
    bw_img = convert_to_bw(img)

    regions = find_mean_location(find_regions(bw_img))
    bw_img = (bw_img * 255).astype('uint8')
    bw_img = cv2.cvtColor(bw_img, cv2.COLOR_GRAY2RGB)

    print("Total regions: " + str(len(regions)))

    for i in range(len(regions)):
        size, location = regions[i]
        print("Region " + str(i + 1) + ": " + str(size))
        draw_text(bw_img, str(i+1) + ": " + str(size), location)

    display_image(bw_img)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("you must provide an image path!")
        exit(0)
    else:
        main(sys.argv[1])