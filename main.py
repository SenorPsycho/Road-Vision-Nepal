import cv2 as cv

#A rescale function to compare normal video to grayscale and others
def rescale_frame(frame,scale=0.75):
    # Resize frame by scale factor
    # Using INTER_AREA for shrinking — averages surrounding 
    # pixels for cleaner result than dropping pixels
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    
    new_dimensions = (width,height)
    
    return cv.resize(frame,new_dimensions,interpolation=cv.INTER_AREA)


#Opening the kathmamdu video -Unstructured Case
#Point to note, define functions before video capture
Kathmandu_Video = cv.VideoCapture('videos/Nepal/Kathmandu.mp4')
Highway_video = cv.VideoCapture('videos/international/highway.mp4')
# 2:35:43 = (2*3600 + 35*60 + 43) * 1000 = 9343000 ms
Highway_video.set(cv.CAP_PROP_POS_MSEC, 9343000)


while True:
    isTrue, frame = Kathmandu_Video.read()
    isTrue2, frame2 = Highway_video.read()
    
    #If no frame returned, exit loop
    if not isTrue or not isTrue2:
        break
    
    # Convert to grayscale — collapses 3 BGR channels into 1 intensity channel
    # Canny needs single channel input to detect intensity gradients cleanly
    grayscale_video_kathmandu = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    grayscale_video_highway = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    
    ## Apply Gaussian blur to grayscale frame
    # Removes high-frequency noise before edge detection
    # 5x5 kernel — mild blur, preserves genuine edges
    # Sigma=0 lets OpenCV auto-calculate from kernel size
    gaussian_blur_video_kathmandu = cv.GaussianBlur(grayscale_video_kathmandu, (5,5), 0)
    gaussian_blur_video_highway = cv.GaussianBlur(grayscale_video_highway,(5,5),0)
    
    
    #Canny edge detection on blurred frame
    canny_video_kathmandu = cv.Canny(gaussian_blur_video_kathmandu, 50, 150)
    canny_video_highway = cv.Canny(gaussian_blur_video_highway, 50, 150)
    
    #All imshow calls
    # cv.imshow('Video_Display',rescale_frame(frame,scale = 0.5))
    # cv.imshow('Grayscale Video',rescale_frame(grayscale_video,scale = 0.5))
    # cv.imshow('Gaussian Blur',rescale_frame(gaussian_blur_video,scale = 0.5))
    cv.imshow('Canny Video Kathmandu',rescale_frame(canny_video_kathmandu,scale = 0.5))
    cv.imshow('Canny Video Highway', rescale_frame(canny_video_highway, scale = 0.5))
    
    
    #Using "d" to exit the video manually before video ends
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
    
    
#Release file handling and free memory     
Kathmandu_Video.release()
cv.destroyAllWindows()