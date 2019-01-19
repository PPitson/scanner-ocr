import locale

# needed to avoid crashes
# reference: https://github.com/sirfz/tesserocr/issues/137
locale.setlocale(locale.LC_ALL, 'C')
# For some reason, Pycharm thinks it's invalid import, but it works
import tesserocr
from tesserocr import PyTessBaseAPI, RIL, PSM, iterate_level, OEM

from PIL import Image, ImageDraw

path = "Paragony-test/IMG_20181112_194547.jpg"
from scanner import scan_image

scanned_image = scan_image(path, show_steps=False)
# recolored = cv2.cvtColor(scanned_image, cv2.COLOR_GRAY2RGB)
# plt.imshow(recolored)

image = Image.fromarray(scanned_image)
width_input, height_input = image.size

# selected by client in mobile app, or detected by some heuristic
(start_height, end_height) = (720, 2400)
prices_names_rectangle = image.crop((0, start_height, width_input, end_height))

# discovered empirically  for Carrefour receipts.
# Divides names of products from prices.
DIVISION_LINE_RATIO = 0.6
prices_width_start = DIVISION_LINE_RATIO * width_input
prices_names_height, prices_names_width = prices_names_rectangle.size

prices_dims = (prices_width_start, 0, prices_names_width + 50, prices_names_height)
prices_rectangle = prices_names_rectangle.crop(prices_dims)


# prices_rectangle.show()

def draw_box(tesseract_box, color, thickness, img):
    coordinates = tesseract_box[1]
    # left upper corner
    pt1 = (int(coordinates['x']), int(coordinates['y']))
    # right bottom corner
    pt2 = (pt1[0] + int(coordinates['w']), pt1[1] + int(coordinates['h']))
    draw = ImageDraw.Draw(img)
    print(pt1)
    print(pt2)
    print()
    draw.rectangle(xy=[pt1, pt2], fill=None, outline=color, width=thickness)


# when trying to set oem= 0 (or OEM.TESSERACT_ONLY) this error appears:
# RuntimeError: Failed to init API, possibly an invalid tessdata path: /usr/share/tessdata/

with PyTessBaseAPI(psm=PSM.SINGLE_BLOCK, lang='eng') as api:
    api.SetImage(prices_rectangle)
    api.SetVariable("save_blob_choices", "T")
    api.SetVariable("lstm_choice_mode", "2")  # i don't know yet which number is correct
    # remember to add few pixels more to bounding box - it improves results
    api.SetRectangle(115 - 5, 194 - 5, 628 - 115 + 5, 272 - 194 + 5)
    word_boxes = api.GetComponentImages(RIL.WORD, True)
    line_boxes = api.GetComponentImages(RIL.TEXTLINE, True)
    symbol_boxes = api.GetComponentImages(RIL.SYMBOL, True)
    api.Recognize()
    ocrResult = api.GetUTF8Text()
    print(api.GetBestLSTMSymbolChoices())
    print(ocrResult)

    ri = api.GetIterator()
    level = RIL.SYMBOL
    for r in iterate_level(ri, level):
        symbol = r.GetUTF8Text(level)  # r == ri
        conf = r.Confidence(level)
        if symbol:
            print('symbol {}, conf: {}'.format(symbol, conf), end=' ')
        indent = False
        ci = r.GetChoiceIterator()
        for idx, c in enumerate(ci):
            if idx > 0:
                print(f"hurra: {idx}")
            if indent:
                print('\t\t ', end=' ')
            print('\t- ', end=' ')
            choice = c.GetUTF8Text()  # c == ci
            print('{} conf: {}'.format(choice, c.Confidence()))
            indent = True
        print('---------------------------------------------')

rgb_prices = prices_rectangle.convert("RGB")
rgb_prices.save('aaaa.png')

# for b in line_boxes:
#    line_boxes draw_box(b, "green", 5, rgb_prices)

for n, b in enumerate(line_boxes):
    if n == 3:
        draw_box(b, "green", 5, rgb_prices)

# for b in word_boxes:
#         draw_box(b, "red", 3, rgb_prices)

# for b in symbol_boxes:
#     draw_box(b, "blue", 1, rgb_prices)

# rgb_prices.show()

# with pytessbaseapi() as api:
#     api.setimagefile('/usr/src/tesseract/testing/phototest.tif')
#     api.setvariable("save_blob_choices", "t")
#     api.setrectangle(37, 228, 548, 31)
#     api.recognize()
#
#     ri = api.getiterator()
#     level = ril.symbol
#     for r in iterate_level(ri, level):
#         symbol = r.getutf8text(level)  # r == ri
#         conf = r.confidence(level)
#         if symbol:
#             print()
#             u'symbol {}, conf: {}'.format(symbol, conf),
#         indent = false
#         ci = r.getchoiceiterator()
#         for c in ci:
#             if indent:
#                 print
#                 '\t\t ',
#             print
#             '\t- ',
#             choice = c.getutf8text()  # c == ci
#             print
#             u'{} conf: {}'.format(choice, c.confidence())
#             indent = true
#         print()
# printprint        '---------------------------------------------'
