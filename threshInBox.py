import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

x = 100
y = 100
w = 200
h = 200

while True:
	ret,frame = cap.read()

	#roi = img[y:y+h,x:x+h]
	cv2.rectangle(frame,(y,x), (y+h,x+w), (0,255,0), 2)

	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	roi = frame[y:y+h,x:x+w]

	#gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)

	#img[y:y+h,x:x+w] = gray
	blur = cv2.GaussianBlur(roi,(5,5),0)

	hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv,np.array([2,0,0]),np.array([20,255,255]))

	kernel = np.ones((5,5))
	dilation = cv2.dilate(mask,kernel,iterations = 1)
	erosion = cv2.erode(dilation,kernel,iterations = 1)

	filtered = cv2.GaussianBlur(erosion,(3,3),0)
	ret,thresh = cv2.threshold(filtered,127,255,0)

	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	#finding contour with max area
	contour = max(contours,key=lambda x: cv2.contourArea(x),default=0)

	#bounding box
	#x,y,w,h = cv2.boundingRect(contour)
	#cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),0)

	

	#convex hull
	hull = cv2.convexHull(contour)

	drawing = np.zeros(roi.shape,np.uint8)
	cv2.drawContours(drawing,[contour],-1,(0,255,0),0)
	cv2.drawContours(drawing,[hull],-1,(0,0,255),0)
	
	cv2.imshow("drawing",drawing)

	hull = cv2.convexHull(contour,returnPoints = False)
	defects = cv2.convexityDefects(contour,hull)

	#finding defects and displaying them on the images
	

	#ret,thresh1 = cv2.threshold(blur,180,255,cv2.THRESH_BINARY)

	#thresh1 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11, 2)
	#blur = cv2.GaussianBlur(gray,(5,5),0)
	#ret3,thresh1 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	#cv2.imshow('hull',hll)
	#cv2.imshow('contours',contour)
	cv2.imshow("img",roi)
	#cv2.imshow('img3',erosion)
	#cv2.imshow('contour',dilation-erosion)



	k = cv2.waitKey(30) & 0xff #exit if Esc is pressed
	if k == 27:
		break

cap.release() #release the webcam
cv2.destroyAllWindows() #destroy the window