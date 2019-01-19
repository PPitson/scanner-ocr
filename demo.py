from scanner import scan_image

from prices_extractor import extract_prices_column, recognize_column

path = "Paragony-test/IMG_20181112_194547.jpg"

scanned_image = scan_image(path, show_steps=False)

# selected manaully by some kind of gui
prices_names_region = (720, 2400)
prices_image, names_image = extract_prices_column(scanned_image, prices_names_region)
prices_text = recognize_column(prices_image)
names_text = recognize_column(names_image)

# todo
# prepare some simple gui to select prices_names_region (described in `def prices_names_region`)
# extract prices from prices_text. Sth like pattern `\d+,\d\d`  that is present after `=` sign
# match prices with names
# display prices and names as table
