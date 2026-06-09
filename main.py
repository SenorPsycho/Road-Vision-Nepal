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

while True:
    isTrue, frame = Kathmandu_Video.read()
    
    #If no frame returned, exit loop
    if not isTrue:
        break
    
    # Convert to grayscale — collapses 3 BGR channels into 1 intensity channel
    # Canny needs single channel input to detect intensity gradients cleanly
    grayscale_video = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('Video_Display',rescale_frame(frame,scale = 0.5))
    cv.imshow('Grayscale Video',rescale_frame(grayscale_video,scale = 0.5))
    
    #Using "d" to exit the video manually before video ends
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
    
    
#Release file handling and free memory     
Kathmandu_Video.release()
cv.destroyAllWindows()