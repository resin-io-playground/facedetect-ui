import cv2
import sys
import os
import threading

pipeFile = "/data/faces"
faces = []
lock = threading.Lock()

def toInt(s):
    return int(s)

def parseFace(face):
    return map(toInt, face.split(','))

def pipeReader():
    while True:
        with open(pipeFile) as openPipe:
            for line in openPipe:
                print(line)
                f = map(parseFace, line.split(';'))
                lock.acquire()
                faces = f
                lock.release()

def getFacesFromPipe():
    lock.acquire()
    f = faces
    lock.release()
    return f

t = threading.Thread(target=pipeReader)
t.start()

video_capture = cv2.VideoCapture('/usr/src/FaceDetect/video.sdp')
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", 1280, 720)          
#cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    faces = getFacesFromPipe()

    # Display the resulting frame
    if ret and len(frame) > 0:
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
