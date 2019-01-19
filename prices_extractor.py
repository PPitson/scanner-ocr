import numpy as np
import locale

# needed to avoid crashes
# reference: https://github.com/sirfz/tesserocr/issues/137
locale.setlocale(locale.LC_ALL, 'C')
# For some reason, Pycharm thinks it's invalid import, but it works
import tesserocr
from tesserocr import PyTessBaseAPI, RIL, PSM, iterate_level, OEM

from typing import Tuple
from PIL import Image


def extract_prices_column(receipt_image: np.ndarray, prices_names_region: Tuple[int, int]) -> (Image, Image):
    """

    :param receipt_image: cleaned image, that contains only receipt, without background
    :param prices_names_region: tuple specyfying (start_height, end_height) of region
    where prices and names of products are located(we assume full width of receipt,
    so iti s not passed as argument). start_height - after "PARAGON FISKALNY".
    end_height - before lines summarizing taxes and amount to pay
    """

    # discovered empirically  for Carrefour receipts.
    # Divides names of products from prices.
    division_line_ratio = 0.65

    (start_height, end_height) = prices_names_region
    image = Image.fromarray(receipt_image)
    width_input, height_input = image.size
    prices_names_rectangle = image.crop((0, start_height, width_input, end_height))
    prices_width_start = division_line_ratio * width_input
    prices_names_width, prices_names_height = prices_names_rectangle.size

    # remove noise like receipt border line
    prices_width_end = prices_names_width - 50
    prices_dims = (prices_width_start, 0, prices_width_end, prices_names_height)
    prices_rectangle = prices_names_rectangle.crop(prices_dims)

    names_dims = (0, 0, prices_width_start, prices_names_height)
    names_rectangle = prices_names_rectangle.crop(names_dims)

    return (prices_rectangle, names_rectangle)


def recognize_column(prices_image: Image) -> str:
    with PyTessBaseAPI(psm=PSM.SINGLE_BLOCK) as api:
        api.SetImage(prices_image)
        ocr_result = api.GetUTF8Text()
        return ocr_result
