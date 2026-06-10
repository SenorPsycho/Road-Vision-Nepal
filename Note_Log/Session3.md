# RoadVision Nepal Research Log

## Session 3 June 10, Wednesday

### What I learned
- Gaussian blur replaces each pixel with a weighted average of surrounding pixels
- Closer pixels get higher weights, further pixels get lower weights
- Kernel size controls neighbourhood size must be odd to have a clear center pixel
- Standard deviation (sigma) controls steepness of weight drop-off
- Sigma=0 lets OpenCV auto-calculate from kernel size
- Too large a kernel over-blurs and destroys genuine edges along with noise
- Blur is preprocessing it removes high-frequency noise before Canny runs

- Canny edge detection is a multi-step process: gradient computation (Sobel) → non-maximum suppression → double thresholding → hysteresis
- Non-maximum suppression thins edges to single-pixel-wide lines
- Two thresholds: above high = definite edge, below low = discarded, in between = weak edge
- Hysteresis keeps weak edges only if connected to a strong edge creates chains
- Low threshold too low = noise chains connect to strong edges and pull in false edges
- Canny is not failing in Kathmandu the environment has no signal to give it

### What I built
- Stage 3: Gaussian blur added to `main.py` 5x5 kernel, sigma=0
- Stage 4: Canny edge detection added to `main.py` thresholds 50/150
- Ran both pipelines simultaneously on Kathmandu and Highway footage for direct comparison
- Used `CAP_PROP_POS_MSEC` to jump to timestamp 2:35:43 in highway footage for a clean open road section

### Observations Gaussian Blur (Kathmandu)
- Streetlamps and headlights still dominant after blur intensity too strong to suppress
- Road surface unchanged nothing to blur, no gradients exist there
- Power lines noticeably thinner and fainter thin high-frequency features affected most
- Blur is working correctly, the input just has no useful signal to preserve

### Observations Canny (Kathmandu)
- Dense edges on buildings, power lines, utility poles, vehicle outlines
- Road surface completely black with zero edges detected
- Power lines survive not on their own strength but through hysteresis chaining to building edges
- This confirms Session 2 prediction: Canny fires on urban infrastructure before any road-relevant features

### Observations Canny Comparison (Highway vs Kathmandu)
- Highway: two clean diagonal lines in lower frame. Yellow left line and dashed white right line clearly detected
- Highway upper half mostly black with open sky and road producing almost nothing
- Kathmandu: dense edges everywhere except road surface
- Same pipeline, same thresholds, opposite results
- Highway environment produces exactly what the pipeline needs
- Kathmandu environment produces everything except what the pipeline needs

### Key research finding Stage 4
- Canny is not failing. The classical pipeline is working as designed.
- The failure is environmental. No lane markings means no intensity gradients on the road surface means nothing for the algorithm to find.
- This is a fundamental mismatch between pipeline assumptions and environment, not a parameter tuning problem.

### Images saved
- `canny_kathmandu_urban_failure.png` dense building edges, black road surface
- `canny_comparison_kathmandu_vs_highway.png` side by side core visual finding

