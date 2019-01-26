import cv2
import imutils
import numpy as np
import argparse
import os

from contours import find_screen_contour
from transform import create_edged_image, create_scanned_image


def show_step_1(image: np.ndarray, edged: np.ndarray) -> None:
    print("STEP 1: Edge Detection")
    cv2.imshow("Image", image)
    cv2.imshow("Edged", edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_step_2(image: np.ndarray, screen_contour: np.ndarray) -> None:
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screen_contour], -1, (0, 255, 0), 2)
    cv2.imshow("Outline", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_step_3(original_image: np.ndarray, scanned_image: np.ndarray) -> None:
    print("STEP 3: Apply perspective transform")
    height_to_resize = 650
    cv2.imshow("Original", imutils.resize(original_image, height=height_to_resize))
    cv2.imshow("Scanned", imutils.resize(scanned_image, height=height_to_resize))
    cv2.waitKey(0)


def scan_image(path: str, show_steps=True) -> np.ndarray:
    height = 600
    img = cv2.imread(path)
    image = cv2.copyMakeBorder(img,15,15,15,15,cv2.BORDER_CONSTANT,None,[0,0,0])
    original_image = image.copy()
    height_ratio = image.shape[0] / float(height)
    image = imutils.resize(image, height=height)

    edged = create_edged_image(image)
    if show_steps:
        show_step_1(image, edged)

    screen_contour = find_screen_contour(edged)
    if show_steps:
        show_step_2(image, screen_contour)

    scanned_image = create_scanned_image(original_image, screen_contour.reshape(4, 2) * height_ratio)
    if show_steps:
        show_step_3(original_image, scanned_image)

    result_file_name = "/tmp/result_" + os.path.basename(path) 
    cv2.imwrite(result_file_name, scanned_image)
    return scanned_image


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
                    help = "Path to the image to be scanned")
    args = ap.parse_args()


    scan_image(args.image, False)
