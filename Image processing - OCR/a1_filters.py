"""
CP467 Assignment 1 - Kumiko Randle, Daniel Berezovski and Amardeep Sarang

=================
     READ ME
=================
First make sure you have python 3 installed.
Then make sure you have cv2 installed for python (pip install opencv-python==4.1.1.26).

run the program as follows:
python a1_filters.py [path to image] [filter]
where filter is one of the following: vertical_line, vertical_sobel, horizontal_line, horizontal_sobel, edge, mean,
gaussian, large_gaussian
"""
import sys
import cv2
import numpy as np

# Detects horizontal lines
horizontal_line_filter = np.array([
    (1, 1, 1),
    (0, 0, 0),
    (-1, -1, -1)
])

# Detects horizontal lines (found on wikipedia)
horizontal_sobel_filter = np.array([
    (1, 2, 1),
    (0, 0, 0),
    (-1, -2, -1)
])

# Detects vertical lines
vertical_line_filter = np.array([
    (1, 0, -1),
    (1, 0, -1),
    (1, 0, -1)
])

# Detects vertical lines (filter found on wikipedia)
vertical_sobel_filter = np.array([
    (1, 0, -1),
    (2, 0, -2),
    (1, 0, -1)
])

# Blurs image by taking average of nearby pixels
mean_filter = np.array([
    (1/9, 1/9, 1/9),
    (1/9, 1/9, 1/9),
    (1/9, 1/9, 1/9)
])

# Blurs image by taking weighted average of nearby pixels
gaussian_filter = np.array([
    (1/16, 1/8, 1/16),
    (1/8, 1/4, 1/8),
    (1/16, 1/8, 1/16)
])

# Blurs image by taking weighted average of nearby pixels
large_gaussian_filter = 1/273.0 * np.array([
    (1, 4, 7, 4, 1),
    (4, 16, 26, 16, 4),
    (7, 26, 41, 26, 7),
    (4, 16, 26, 16, 4),
    (1, 4, 7, 4, 1)
])

# Detects both vertical and horizontal edges (from wikipedia)
edge_filter = np.array([
    (0, 1, 0),
    (1, -4, 1),
    (0, 1, 0)
])

# Dictionary of filter names paired with actual filter
filters = {
    "vertical_line": vertical_line_filter,
    "vertical_sobel": vertical_sobel_filter,
    "horizontal_line": horizontal_line_filter,
    "horizontal_sobel": horizontal_sobel_filter,
    "edge": edge_filter,
    "mean": mean_filter,
    "gaussian": gaussian_filter,
    "large_gaussian": large_gaussian_filter
}


def open_image(path):
    """
    Opens the image at the given path, reading it in as a grayscale image. Then we convert the pixel values (0 to 255)
    to a decimal number (0.0 to 1.0).
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Could not find image at specified path.")
        exit(0)
    return cv2.normalize(img.astype("float"), None, 0.0, 1.0, cv2.NORM_MINMAX)


def fit_image_to_screen(img, max_width=600, max_height=700):
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


def show_img(original, filtered):
    """
    Given two images, display them side by side. The images have pixel values as decimal numbers ranging from 0.0 to
    1.0. The cv2 library automatically converts this back to 0 to 255 pixel values.
    """
    cv2.imshow("original vs filtered image", np.hstack((original, filtered)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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


def apply_filter (img, img_filter, y, x):
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


def main(img_path, filter_name="vertical_line"):
    img = fit_image_to_screen(open_image(img_path))
    selected_filter = filters[filter_name]
    img_size = img.shape
    filter_size = selected_filter.shape
    new_image = np.zeros(img_size) # creates array of zeros equal to dimensions of original image

    # creates padded image to deal applying filter to edge pixels
    # pads image by extending edges, not with zeros
    padded_img = np.pad(img, (filter_size[0] // 2, filter_size[1] // 2), "edge")

    # iterates through each pixel in image and applies a filter centered at that pixel
    for y in range(img_size[0]):
        if y % 10 == 0 or y == img_size[0]-1:
            print("{0:.2f}% done".format((y+1)/img_size[0] * 100))
        for x in range(img_size[1]):
            new_image[y,x] = apply_filter(padded_img, selected_filter, y, x)

    show_img(img, new_image)


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("you must provide an image path!")
        exit(0)
    elif len(sys.argv) == 2:
        print("no filter specified - defaulting to vertical line filter")
        main(sys.argv[1])
    elif sys.argv[2] not in filters:
        print("filter \"" + sys.argv[2] + "\" does not exist. Please pick from the list below:")
        print(repr(filters.keys()))
        exit(0)
    else:
        main(sys.argv[1], sys.argv[2])
