import cv2
import imutils
import numpy as np


def find_screen_contour(image: np.ndarray) -> np.ndarray:
    """ Returns a rectangle representing object of interest """
    max_contour = get_contour_with_max_area(image)
    screen_contour = get_screen_contour_approximation(max_contour)
    if len(screen_contour) != 4:
        screen_contour = get_minimum_rect(screen_contour)
    return screen_contour


def get_contour_with_max_area(image: np.ndarray) -> np.ndarray:
    contours = find_contours(image.copy())
    return max(contours, key=cv2.contourArea)


def find_contours(image: np.ndarray) -> np.ndarray:
    contours = cv2.findContours(image.copy(), mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
    return contours[0] if imutils.is_cv2() else contours[1]


def get_screen_contour_approximation(contour: np.ndarray) -> np.ndarray:
    contour_perimeter = cv2.arcLength(contour, closed=True)
    epsilon = 0.02 * contour_perimeter  # This is the maximum distance between the original curve and its approximation
    return cv2.approxPolyDP(contour, epsilon, closed=True)


def get_minimum_rect(contour: np.ndarray) -> np.ndarray:
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    return np.int0(box)
