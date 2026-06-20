# RoadVision Nepal

An evaluation of classical lane detection on Nepali road environments.

## Research Question

Does classical computer vision lane detection work on Nepali roads? Where does it fail, why does it fail technically, and what would a system designed for this environment actually need?

## Motivation

Classical lane detection pipelines are built on assumptions that hold in structured road environments — painted lane markings, even lighting, clean asphalt. These assumptions are rarely questioned because they hold reliably in the datasets and environments where these systems are developed and tested.

Nepali roads, particularly urban roads in Kathmandu, violate most of these assumptions. This project investigates what happens when a standard classical pipeline encounters that environment, characterizing specific failure mechanisms rather than simply demonstrating failure.

## Methodology

A full 8-stage classical lane detection pipeline was implemented in Python using OpenCV:

1. Video input
2. Grayscale conversion
3. Gaussian blur
4. Canny edge detection
5. Region of interest masking
6. Hough Line Transform
7. Line averaging and stabilization
8. Output video writer

The pipeline was tested on two videos representing contrasting environments:

- **Highway footage** — a structured US highway with clear lane markings, used as a baseline to confirm the pipeline functions correctly under standard assumptions
- **Kathmandu footage** — urban roads from Kathmandu to Dharke, recorded at dusk, with no consistent lane markings, dense surrounding structures, and mixed lighting

Two adaptations were then applied and evaluated:

- **HSV color filtering** — isolating yellow and white lane-colored pixels before edge detection to reduce false gradients
- **Adaptive ROI** — dynamically estimating the apex of the region of interest based on per-frame edge density rather than a fixed position

## Key Findings

Two distinct failure modes were identified:

**Signal Discontinuity** — present on highway footage where dashed lane markings cause intermittent detection between dash gaps. The signal exists but is interrupted. This failure is recoverable through temporal smoothing.

**Signal Absence** — present throughout the Kathmandu footage. No lane markings exist on the road surface, so no intensity gradient is available for any stage to detect. Neither HSV filtering nor adaptive ROI improved this outcome, confirming that the bottleneck is the absence of the signal the pipeline is designed to detect, not a tuning problem.

The pipeline does not fail gracefully under signal absence. It produces confident-looking output by latching onto building edges, dashboard boundaries, and noise fragments — making it more dangerous than a system that produces no output at all.

## Output Samples

![Highway detection](images/highway_output.png)
![Kathmandu detection](images/kathmandu_output.png)

## Documentation

Full failure analysis including stage-by-stage breakdown, assumption mapping, and adaptation experiment results is in [`FAILURE_ANALYSIS.md`](FAILURE_ANALYSIS.md).

## Stack

Python, OpenCV, NumPy

## Future Direction

The primary limitation is the absence of reliable lane markings. Future work may investigate road-boundary-based approaches that identify drivable surface without relying on painted markings, or semantic segmentation methods that do not assume structured road environments.
