# RoadVision Nepal Research Log

## Session 4 June 11, Thursday

### What I learned

**NumPy basics**
- Images are grids of numbers stored as NumPy arrays grayscale is 2D, color is 3D
- Every OpenCV frame is a NumPy array under the hood
- np.zeros_like(image) creates a black array with the exact same shape and data type as the input image
- shape[0] = height, shape[1] = width (already knew this but confirmed in context of masks)

**Masking**
- A mask is a black image with a white shape drawn on it
- White regions = keep, black regions = discard
- cv.fillPoly() fills a polygon with a color on a given image
- Polygon points must be a NumPy array

**Bitwise AND**
- Operates per pixel both pixels must be white (255) for the result to be white
- 255 AND 255 = 255 (edge survives)
- 255 AND 0 = 0 (edge removed)
- Used to combine Canny output with mask only edges inside the white polygon survive

**ROI shape reasoning**
- Road occupies a triangle in dashcam perspective wide at bottom, narrow at horizon
- Rectangle would include buildings and parked vehicles on the sides
- Triangle cuts to only the road ahead region

### What I built
- Stage 5: region_of_interest() function added to main.py
- Triangle defined with three points: bottom-left (0, 1080), bottom-right (1920, 1080), apex (960, 540)
- Applied to Canny output for both Kathmandu and Highway footage
- Both videos running simultaneously for direct comparison
- Highway timestamp set to 2:35:43 open road section with clear lane markings, minimal urban clutter

### Observations ROI (Highway)
- Two clean diagonal lines visible inside triangle yellow left line and dashed white right line
- Lines converge toward apex as expected from perspective
- Some vegetation edges on left side but lane lines clearly dominant
- ROI successfully isolates the road region the pipeline needs

### Observations ROI (Kathmandu)
- Buildings and vehicles survived inside the lower triangle urban scene extends into road region
- Road surface at bottom shows only a faint horizontal boundary line, not a lane marking
- No diagonal lane lines anywhere inside the triangle
- Road surface area inside triangle is empty no edges

### Key research finding Stage 5
ROI masking confirms the failure is not noise. Sky, power lines, and upper-frame
clutter are all eliminated. Even with perfect isolation of the road region,
there are no lane edges inside the triangle on Kathmandu footage.
The absence of markings means no edges exist where the pipeline looks for them.
This is not a fixable parameter it is a structural mismatch between
the pipeline's assumptions and the environment.

