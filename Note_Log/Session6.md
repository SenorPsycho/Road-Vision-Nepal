## Session 6 June 14, Saturday

### What I learned

**Line averaging core idea**
- Hough returns many short segments per frame for what should be two lane lines
- Averaging groups all segments into left lane and right lane based on slope direction
- Negative slope = left lane, positive slope = right lane (because y increases downward in OpenCV)
- Lines with slope between -0.3 and 0.3 are nearly horizontal noise, discarded
- All slopes and intercepts per side get averaged into one representative slope and intercept
- np.average() with axis=0 averages columns separately slopes together, intercepts together

**Slope and intercept**
- Slope = (y2 - y1) / (x2 - x1) steepness of the line
- Intercept = y1 - slope * x1 where the line crosses the y-axis
- Together they describe any line as y = mx + b

**Converting slope and intercept to pixel coordinates**
- cv.line needs two points, not slope and intercept
- Fix y1 at frame bottom (height) and y2 at 60% of height (near horizon)
- Solve for x using x = (y - intercept) / slope
- int() wraps the result because pixel coordinates must be whole numbers
- Returns tuple (x1, y1, x2, y2) immutable, coordinates shouldn't change after creation

**None handling**
- average_line returns None for a side if no lines of that slope direction were found
- make_line returns None early if passed None
- Every drawing block checks is not None before unpacking and drawing
- Defensive programming pipeline must not crash on empty frames

**Two failure modes identified**
- Signal discontinuity marking exists but isn't always visible (dashed white highway line flickering)
- Signal absence nothing consistent to track at all (Kathmandu lines jumping every frame)
- These are different problems one is fixable with temporal smoothing, one is not

### What I built
- Stage 7: average_line() function groups Hough segments by slope, averages into one line per side
- Stage 7: make_line() function converts averaged slope and intercept to drawable pixel coordinates
- Replaced raw Hough drawing loops with averaged single lines per side
- Both videos running simultaneously, each drawing up to two averaged green lines per frame

### Observations Averaged Lines (Highway)
- Two clean lines converging toward vanishing point on the horizon
- Left line tracks yellow lane marking consistently
- Right line tracks white dashed marking but flickers on frames between dashes
- Lines cross near horizon geometrically correct perspective behavior
- Pipeline producing stable, meaningful output on structured road

### Observations Averaged Lines (Kathmandu)
- Two lines drawn but tracking building edges and vehicle outlines, not lane markings
- Lines jump to different angles and positions every few frames no consistent anchor
- Lines cross in middle of frame, not at a road vanishing point
- Pipeline outputs confident-looking result that is completely wrong
- Instability confirms no consistent signal exists for the averaging to converge on

### Key research finding Stage 7
The completed classical pipeline reveals its most important failure characteristic:
it does not fail silently on Kathmandu footage.
It draws lines every frame with apparent confidence.
But those lines track building edges, vehicle outlines, and road boundaries
not lane markings, because none exist.
A system relying on this output would not know it was wrong.
This is more dangerous than returning nothing.
Signal absence produces confidently incorrect output, not null output.

### Images saved
- averaged_lines_comparison_1.png both lanes detected on highway, Kathmandu lines tracking buildings
- averaged_lines_comparison_2.png highway left lane clean, Kathmandu single line crossing frame diagonally

### Next steps
- Stage 8: Output video writer save processed video to file
- Begin failure analysis documentation
- Consider simple adaptations to test against baseline