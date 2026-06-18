# RoadVision Nepal Research Log

## Session 2 June 09, Tuesday

### What I learned
- BGR is Blue Green Red color representation of an image
- Grayscale collapses 3 BGR channels into 1 intensity channel
- Grayscale formula: Gray = 0.114*Blue + 0.587*Green + 0.299*Red
- Green has highest weight because human eyes are most sensitive to green
- Color differences survive grayscale conversion at different intensities
- shape[0] = height, shape[1] = width, shape[2] = channels
- HSV cannot convert directly to grayscale mune go HSV > BGR > Gray
- Matplotlib expects RGB, OpenCV uses BGR mune convert before plotting

### What I built
- Stage 2: Grayscale conversion added to main.py
- rescale_frame function for display at 0.5 scale
- practice/color_spaces.py. Explored BGR, HSV, LAB, RGB conversions

### Observations Kanemandu Grayscale
- Road surface maps to low uniform dark gray
- No lane markings means no intensity gradients on road surface
- Dominant bright regions: streetlamps, headlights, sky
- Prediction: Canny will fire on lighting and building edges before any road-relevant features