## Session 5 June 13, Friday

### What I learned

**Hough Line Transform core idea**
- After Canny you have white pixels on a black image individual dots with no context
- Hough's job is to figure out which dots belong to the same line
- Every white pixel votes for all lines that could pass through it
- Lines that receive many votes from many pixels are real lines
- Lines with few votes are noise and get discarded
- This is called voting a democracy of pixels

**HoughLines vs HoughLinesP**
- HoughLines returns infinite lines stretching across the entire frame not useful for lane detection
- HoughLinesP is probabilistic returns actual line segments with start and end points (x1, y1, x2, y2)
- HoughLinesP is the standard for lane detection pipelines

**HoughLinesP parameters**
- rho=2 precision of distance voting grid, 2 pixels is standard
- theta=np.pi/180 1 degree angle precision, always use this
- threshold=100 minimum votes needed for a line to be returned, higher is stricter
- minLineLength=40 segments shorter than this get discarded, removes noise
- maxLineGap=5 gaps smaller than this between aligned segments get bridged, helps with dashed lines
- Dashed lines need lower threshold and minLineLength than solid lines each dash is short with fewer votes

**cv.line**
- Draws a line segment on an image between two points
- Parameters: image, pt1 (x1,y1), pt2 (x2,y2), color (BGR tuple), thickness
- Draw on a copy of the frame, not the original preserves original for comparison
- HoughLinesP output is wrapped in an extra array use line[0] to unwrap to x1,y1,x2,y2

**None check**
- HoughLinesP returns None if no lines detected
- Always check if result is not None before looping crashes otherwise
- On Kathmandu frames this check fires frequently

### What I built
- Stage 6: HoughLinesP applied to both ROI outputs
- Separate loops for Kathmandu and Highway with None checks
- Lines drawn in green on frame copies, not original frames
- Both videos running simultaneously for direct comparison

### Observations Hough Lines (Highway)
- Yellow left lane line detected cleanly long diagonal green segment following it precisely
- White dashed right lane partially detected shorter segments, gaps between dashes not fully bridged
- Some false detections on vegetation and distant vehicles inside ROI
- Pipeline working correctly on structured road environment

### Observations Hough Lines (Kathmandu)
- Dashboard edge detected as horizontal green line at bottom car hood boundary, not a lane
- Few random short segments from building edges and vehicles inside ROI triangle
- No consistent diagonal lane lines anywhere
- Road surface produces no detections confirms all previous stage findings

### Key research finding Stage 6
Hough Line Transform completes the failure picture.
On highway, the pipeline returns clean lane line segments.
On Kathmandu, it returns dashboard edges and random noise fragments.
The absence of lane markings propagates through every stage
no gradients at Canny, no edges at ROI, no lines at Hough.
The pipeline cannot invent signal that was never there.
