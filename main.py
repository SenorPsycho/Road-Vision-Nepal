import cv2 as cv

#Opening the kathmamdu video -Unstructured Case

Kathmandu_Video = cv.VideoCapture('videos/Nepal/Kathmandu.mp4')

while True:
    isTrue, frame = Kathmandu_Video.read()
    
    #If no frame returned, exit loop
    if not isTrue:
        break
    
    cv.imshow('Video_Display',frame)
    
    #Using "d" to exit the video manually before video ends
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
    
    
#Release file handling and free memory     
Kathmandu_Video.release()
cv.destroyAllWindows()