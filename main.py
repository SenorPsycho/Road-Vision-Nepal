import cv2 as cv
import numpy as np
import os
import sys

#Create output directory if it doesn't exist
os.makedirs('Output', exist_ok=True)

def hsv_filter(frame):
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # Yellow mask — H 20-30, full saturation, full value
    yellow_lower = np.array([15, 120, 80])
    yellow_upper = np.array([35, 255, 255])
    yellow_mask = cv.inRange(hsv, yellow_lower, yellow_upper)
    
    # White mask — any hue, low saturation, high value
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([179, 50, 255])
    white_mask = cv.inRange(hsv, white_lower, white_upper)
    
    # Combine both masks
    combined_mask = cv.bitwise_or(yellow_mask, white_mask)
    
    # Apply mask to original BGR frame
    result = cv.bitwise_and(frame, frame, mask=combined_mask)
    
    return result


# A average line function to average multiple line segments into one line for left and right lane
def average_line(frame, lines):
    left_lines = []
    right_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (
            (y2 - y1) / (x2 - x1) if x2 != x1 else 0
        )  # Avoid division by zero for vertical lines
        intercept = y1 - slope * x1
        if slope < -0.3:
            left_lines.append((slope, intercept))
        elif slope > 0.3:
            right_lines.append((slope, intercept))
    left_average = np.average(left_lines, axis=0) if left_lines else None
    right_average = np.average(right_lines, axis=0) if right_lines else None
    return left_average, right_average


# A make line function to convert slope and intercept back to pixel coordinates for drawing
def make_line(frame, line):
    if line is None:
        return None
    slope, intercept = line
    if abs(slope) < 0.001:  # guard against near-zero slope
        return None
    y1 = frame.shape[0]
    y2 = int(y1 * 0.75)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return (x1, y1, x2, y2)


# A rescale function to compare normal video to grayscale and others
def rescale_frame(frame, scale=0.75):
    # Resize frame by scale factor
    # Using INTER_AREA for shrinking — averages surrounding
    # pixels for cleaner result than dropping pixels
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    new_dimensions = (width, height)

    return cv.resize(frame, new_dimensions, interpolation=cv.INTER_AREA)


# Region of Interest (ROI) function for noise removal (Road widens at bottom, narrows toward horizon)
def region_of_interest(frame):
    height = frame.shape[0]
    width = frame.shape[1]

    # Look at upper half of frame only
    upper_half = frame[0:height // 2, :]
    
    # Sum edge pixels across each row
    row_sums = np.sum(upper_half, axis=1)
    
    # Find rows with significant edge activity
    significant_rows = np.where(row_sums > 500)[0]

    # Use lowest significant row as apex, fallback to height//2
    if len(significant_rows) > 0:
        apex_y = int(significant_rows[-1])
    else:
        apex_y = height // 2

    triangle = np.array([
        [
            (0, height),
            (width, height),
            (width // 2, apex_y)
        ]
    ])

    mask = np.zeros_like(frame)
    cv.fillPoly(mask, triangle, 255)
    return cv.bitwise_and(frame, mask)


# Opening the kathmamdu video -Unstructured Case
# Point to note, define functions before video capture


Kathmandu_Video = cv.VideoCapture("videos/Nepal/Kathmandu.mp4")
Highway_video = cv.VideoCapture("videos/international/highway.mp4")

# Check if videos opened successfully, if not, print error and exit
if not Kathmandu_Video.isOpened():
    print("Error: Could not open Kathmandu video")
    sys.exit(1)

if not Highway_video.isOpened():
    print("Error: Could not open Highway video")
    sys.exit(1)

# FPS retrieval for both videos, to ensure they are processed at correct speed and to check if they are same or different
fps_kathmandu = Kathmandu_Video.get(cv.CAP_PROP_FPS)
fps_highway = Highway_video.get(cv.CAP_PROP_FPS)

# Temporary line to find frame dimensions
# print('Kathmandu resolution:', Kathmandu_Video.get(cv.CAP_PROP_FRAME_WIDTH), 'x', Kathmandu_Video.get(cv.CAP_PROP_FRAME_HEIGHT))
# print('Highway resolution:', Highway_video.get(cv.CAP_PROP_FRAME_WIDTH), 'x', Highway_video.get(cv.CAP_PROP_FRAME_HEIGHT))

# 2:35:43 = (2*3600 + 35*60 + 43) * 1000 = 9343000 ms
Highway_video.set(cv.CAP_PROP_POS_MSEC, 9343000)
# This timestamp chosen to see clean highway roads with less urban factors.

# Define output video writers for both videos, using same dimensions and fps as input videos
fourcc = cv.VideoWriter_fourcc(*"mp4v")

# Frame dimensions retrieval for both videos, to ensure they are processed correctly
frame_width = int(Kathmandu_Video.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(Kathmandu_Video.get(cv.CAP_PROP_FRAME_HEIGHT))
frame_width2 = int(Highway_video.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height2 = int(Highway_video.get(cv.CAP_PROP_FRAME_HEIGHT))

# Output video writer initialization for both videos, to save the processed videos with detected lane lines
output_kathmandu = cv.VideoWriter(
    "Output/output_kathmandu.mp4", fourcc, fps_kathmandu, (frame_width, frame_height)
)
output_highway = cv.VideoWriter(
    "Output/output_highway.mp4", fourcc, fps_highway, (frame_width2, frame_height2)
)


while True:
    isTrue, frame = Kathmandu_Video.read()
    isTrue2, frame2 = Highway_video.read()

    # Frame checker
    if not isTrue or not isTrue2:
        break

    # Frame copy for drawing lines later without affecting original frame
    # frame_copy is kathmandu video, frame2_copy is highway video
    frame_copy = frame.copy()
    frame2_copy = frame2.copy()
    
    # Apply HSV filter to isolate lane colors (yellow and white) for both videos, to enhance lane line detection by reducing noise from irrelevant colors
    hsv_kathmandu = hsv_filter(frame)
    hsv_highway = hsv_filter(frame2)

    # Convert to grayscale — collapses 3 BGR channels into 1 intensity channel
    # Canny needs single channel input to detect intensity gradients cleanly
    grayscale_video_kathmandu = cv.cvtColor(hsv_kathmandu, cv.COLOR_BGR2GRAY)
    grayscale_video_highway = cv.cvtColor(hsv_highway, cv.COLOR_BGR2GRAY)

    ## Apply Gaussian blur to grayscale frame
    # Removes high-frequency noise before edge detection
    # 5x5 kernel — mild blur, preserves genuine edges
    # Sigma=0 lets OpenCV auto-calculate from kernel size
    gaussian_blur_video_kathmandu = cv.GaussianBlur(
        grayscale_video_kathmandu, (5, 5), 0
    )
    gaussian_blur_video_highway = cv.GaussianBlur(grayscale_video_highway, (5, 5), 0)

    # Canny edge detection on blurred frame
    canny_video_kathmandu = cv.Canny(gaussian_blur_video_kathmandu, 50, 150)
    canny_video_highway = cv.Canny(gaussian_blur_video_highway, 50, 150)

    # Apply region of interest mask to Canny output
    ROI_video_kathmandu = region_of_interest(canny_video_kathmandu)
    ROI_video_highway = region_of_interest(canny_video_highway)

    # Apply Hough Transform to find lines in the masked Canny output
    Hough_video_kathmandu = cv.HoughLinesP(
        ROI_video_kathmandu,
        2,
        np.pi / 180,
        threshold=100,
        minLineLength=40,
        maxLineGap=5,
    )
    if Hough_video_kathmandu is not None:
        Averaged_Kathmandu = average_line(frame, Hough_video_kathmandu)
    else:
        Averaged_Kathmandu = (None, None)

    Hough_video_highway = cv.HoughLinesP(
        ROI_video_highway, 2, np.pi / 180, threshold=100, minLineLength=40, maxLineGap=5
    )
    if Hough_video_highway is not None:
        Averaged_Highway = average_line(frame2, Hough_video_highway)
    else:
        Averaged_Highway = (None, None)

    left_avg_kathmandu, right_avg_kathmandu = Averaged_Kathmandu
    left_line_kathmandu = make_line(frame, left_avg_kathmandu)
    right_line_kathmandu = make_line(frame, right_avg_kathmandu)

    left_avg_highway, right_avg_highway = Averaged_Highway
    # print("Left avg highway:", left_avg_highway)
    # print("Right avg highway:", right_avg_highway)
    left_line_highway = make_line(frame2, left_avg_highway)
    right_line_highway = make_line(frame2, right_avg_highway)

    if left_line_kathmandu is not None:
        x1, y1, x2, y2 = left_line_kathmandu
        cv.line(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 5)

    if right_line_kathmandu is not None:
        x1, y1, x2, y2 = right_line_kathmandu
        cv.line(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 5)

    if left_line_highway is not None:
        x1, y1, x2, y2 = left_line_highway
        cv.line(frame2_copy, (x1, y1), (x2, y2), (0, 255, 0), 5)

    if right_line_highway is not None:
        x1, y1, x2, y2 = right_line_highway
        cv.line(frame2_copy, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # Loop through detected lines and draw them on the copied frame

    # First loop for kathmandu video (with none check for lines, because if no lines detected, it will throw an error)
    # if Hough_video_kathmandu is not None:
    #     for line in Hough_video_kathmandu:
    #         x1, y1, x2, y2 = line[0]
    #         cv.line(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # # Second loop for highway video (Same logic with none check for lines)
    # if Hough_video_highway is not None:
    #     for line in Hough_video_highway:
    #         x1, y1, x2, y2 = line[0]
    #         cv.line(frame2_copy, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # All imshow calls
    # cv.imshow('Video_Display',rescale_frame(frame,scale = 0.5))
    # cv.imshow('Grayscale Video',rescale_frame(grayscale_video,scale = 0.5))
    # cv.imshow('Gaussian Blur',rescale_frame(gaussian_blur_video,scale = 0.5))
    # cv.imshow('Canny Video Kathmandu',rescale_frame(canny_video_kathmandu,scale = 0.5))
    # cv.imshow('Canny Video Highway', rescale_frame(canny_video_highway, scale = 0.5))
    # cv.imshow('ROI masked video Kathmandu',rescale_frame(ROI_video_kathmandu,scale = 0.5))
    # cv.imshow('ROI masked video highway',rescale_frame(ROI_video_highway,scale = 0.5))
    # cv.imshow("Hough Lines Video Kathmandu", rescale_frame(frame_copy, scale=0.5))
    # cv.imshow("Hough Lines Video Highway", rescale_frame(frame2_copy, scale=0.5))
    # cv.imshow("hsv filtered video kathmandu", rescale_frame(hsv_kathmandu, scale=0.5))
    # cv.imshow("hsv filtered video highway", rescale_frame(hsv_highway, scale=0.5))

    cv.imshow("averaged lines on highway", rescale_frame(frame2_copy, scale=0.5))
    cv.imshow("averaged lines on kathmandu", rescale_frame(frame_copy, scale=0.5))

    # Write the processed frames with detected lane lines to output videos
    output_kathmandu.write(frame_copy)
    output_highway.write(frame2_copy)

    # Using "d" to exit the video manually before video ends
    if cv.waitKey(20) & 0xFF == ord("d"):
        break


# Release file handling and free memory
Kathmandu_Video.release()
Highway_video.release()
output_kathmandu.release()
output_highway.release()
cv.destroyAllWindows()