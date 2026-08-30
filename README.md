# Kathmandu Lane Detection Failure Analysis

A systematic evaluation of a classical (Canny/Hough) lane detection pipeline on unmarked, unstructured urban roads in Kathmandu, Nepal, benchmarked against structured US highway footage.

## Research question

Why does classical lane detection fail on roads without painted lane markings? Is it a tuning problem, or a fundamental breakdown of the pipeline's assumptions?

## Key finding

The failure is **signal absence, not signal degradation**. Every stage of the pipeline, from grayscale conversion and Gaussian blur through Canny edge detection, ROI masking, Hough transform, and line averaging, depends on intensity gradients created by painted lane markings. When no markings exist, there is no gradient for any stage to recover. No amount of threshold tuning, ROI adjustment, or filtering can create signal that was never present.

More importantly, the pipeline does not fail safely. Instead of reporting no detection, it produces confident, stable-looking lane lines by latching onto irrelevant structure such as building edges, dashboard boundaries, and power lines that happened to pass slope filtering. A system that draws no lines signals lost tracking. A system that draws wrong lines with confidence does not.

Full stage-by-stage analysis, including two adaptation experiments (HSV color filtering, adaptive ROI), is documented in [FAILURE_ANALYSIS.md](FAILURE_ANALYSIS.md).

## Method

An 8-stage classical pipeline (grayscale, blur, Canny edge detection, ROI masking, Hough line transform, slope-based line averaging) was run in parallel on two video sources:

- **Highway footage**: US highway, clear painted lane markings, even daytime lighting
- **Kathmandu footage**: unmarked urban road, dusk lighting, mixed traffic, no lane markings

Running identical code on both isolates *environmental* causes of failure from *algorithmic* ones.

## Adaptation experiments

Two targeted modifications were tested to see whether they could recover lane signal on the Kathmandu footage:

1. **HSV color filtering**: filtering for yellow/white marking colors before edge detection. This correctly produced near-zero output on Kathmandu footage, since no markings exist to detect, confirming the bottleneck is signal absence rather than color space.
2. **Adaptive ROI**: dynamically estimating the region-of-interest apex per frame instead of using a fixed triangle. No meaningful change was observed on either dataset, showing ROI placement was never the bottleneck.

Both experiments reinforce the core conclusion that this is not a parameter-tuning problem.

## Repository structure

```
Classical_Pipeline_Output/       # Processed output videos (highway, Kathmandu)
Comparision_Images_Of_Pipeline/  # Stage-by-stage visual comparisons
Session_Log/                     # Development session logs (chronological)
FAILURE_ANALYSIS.md              # Full technical failure analysis
main.py                          # Pipeline implementation
```

## Status

This study is complete. No further iteration is planned on the classical pipeline itself. The findings here motivate a separate, ongoing deep-learning segmentation project, particularly the conclusion that unmarked roads require a fundamentally different detection approach such as semantic segmentation, road-boundary detection, or sensor fusion rather than edge/line detection.

## Stack

Python, OpenCV, NumPy
