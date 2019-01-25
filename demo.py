import re

from prices_extractor import extract_prices_column, recognize_column
from scanner import scan_image

PATH = "Paragony-test/IMG_20181112_194547.jpg"
PRICES_PATTERN = re.compile(r"(?<==)\s([\d\.\,]+)")


def get_price(price_text: str) -> float:
    price_match = re.search(PRICES_PATTERN, price_text)
    if price_match is None:
        return 0.0
    return float(price_match.group().replace(",", "."))


scanned_image = scan_image(PATH, show_steps=False)

# selected manaully by some kind of gui
prices_names_region = (720, 2400)
prices_image, names_image = extract_prices_column(scanned_image, prices_names_region)
prices_text = recognize_column(prices_image)
names_text = recognize_column(names_image)

prices = [price_text for price_text in prices_text.split("\n") if price_text][1:]  # [1:] to remove noisy header
products = [product for product in names_text.split("\n") if product][1:]

width = 30
total_sum = 0
for product_name, price_text in zip(products, prices):
    price = get_price(price_text)
    print(f"{product_name:{width}}{price}")
    # print(product_name, price)
    total_sum += price

print("Sum:", round(total_sum, 2))
