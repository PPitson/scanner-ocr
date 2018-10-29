import cv2
import numpy as np
from imutils import auto_canny
from skimage.filters import threshold_local


def create_edged_image(image: np.ndarray) -> np.ndarray:
    """ Creates images containing wihte edges on black background """
    image = convert_to_grayscale(image)
    image = blur_image(image)
    return auto_canny(image)


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def blur_image(image: np.ndarray) -> np.ndarray:
    return cv2.GaussianBlur(image, ksize=(5, 5), sigmaX=0)


def create_scanned_image(image: np.ndarray, contour_points: np.ndarray) -> np.ndarray:
    top_down_image = obtain_birds_eye_view(image, contour_points)
    return give_black_and_white_paper_effect(top_down_image)


def obtain_birds_eye_view(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    rect = order_points(pts)
    top_left, top_right, bottom_right, bottom_left = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    distance_between_bottom_coordinates = np.linalg.norm(bottom_right - bottom_left)
    distance_between_top_coordinates = np.linalg.norm(top_right - top_left)
    max_width = max(int(distance_between_bottom_coordinates), int(distance_between_top_coordinates))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    distance_between_right_coordinates = np.linalg.norm(top_right - bottom_right)
    distance_between_left_coordinates = np.linalg.norm(top_left - bottom_left)
    max_height = max(int(distance_between_right_coordinates), int(distance_between_left_coordinates))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array(
        [
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ],
        dtype="float32"
    )

    # compute the perspective transform matrix and then apply it
    perspective_transform_matrix = cv2.getPerspectiveTransform(rect, dst)
    return cv2.warpPerspective(image, perspective_transform_matrix, dsize=(max_width, max_height))


def order_points(points: np.ndarray) -> np.ndarray:
    top_left = 0
    top_right = 1
    bottom_right = 2
    bottom_left = 3
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = points.sum(axis=1)
    rect[top_left] = points[np.argmin(s)]
    rect[bottom_right] = points[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(points, axis=1)
    rect[top_right] = points[np.argmin(diff)]
    rect[bottom_left] = points[np.argmax(diff)]

    # rect now has got ordered coordinates
    return rect


def give_black_and_white_paper_effect(image: np.ndarray) -> np.ndarray:
    warped = convert_to_grayscale(image)
    thresholded_warped = threshold_local(warped, block_size=11, method="gaussian", offset=10)
    return (warped > thresholded_warped).astype("uint8") * 255
