# Results of experiments

## Image segmentation
- trying to automatically extract part of receipt with prices is not easy
I took bounding boxes of words and tried to combine them into 2-3 main segments of receipt using
morphological operations on image.
- Simpler approach is to ask user to draw bounding box on prices list (e.g. via mobile app)
- And vertical division line between names and prices can be hardcoded ratio of width,
 because it's constant for given type of receipt
 
 ## Telling Tesseract what it should expect
 - In Tesseract 3.x it was possible to specify `whitelistchars`. That allowed to constrain outputs of OCR to only 
 limited set of chars. There was also `user-patterns` options that allowed to specify expected "words" by regex. 
 However both of these features don't work anymore  (https://github.com/tesseract-ocr/tesseract/issues/403 ,
 https://github.com/tesseract-ocr/tesseract/issues/751 ) with new engine in tesseract 4.0. They should work in old 
 engine (--oem 0), but trying to run it end with error (about lack of traineddata)
 - There is some hope in function `GetBestLSTMSymbolChoices` 
 (https://github.com/sirfz/tesserocr/pull/147/files#diff-8f6d524f7607ce50dc1ba57419e80a5cR2126)
 It returns confidences about posbible symbols. 
 We could add some logic to get values we expect, even they're less probable
  
 
  
 

