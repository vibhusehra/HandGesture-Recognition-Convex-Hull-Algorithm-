import cv2
import numpy as np
import math

def imageFiltering(frame):

	roi = frame[y:y+h,x:x+w]

	blur = cv2.GaussianBlur(roi,(5,5),0)

	hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv,np.array([2,50,50]),np.array([20,255,255]))

	kernel = np.ones((5,5))

	filtered = cv2.GaussianBlur(mask,(3,3),0)
	ret,thresh = cv2.threshold(filtered,127,255,0)
	thesh = cv2.GaussianBlur(thresh,(5,5),0)

	contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


	return roi,thresh,contours


cap = cv2.VideoCapture(0)

x = 100
y = 100
w = 200
h = 200

while True:
	ret,frame = cap.read()

	cv2.rectangle(frame,(y,x), (y+h,x+w), (0,255,0), 2)

	#gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	
	

	roi,thresh,contours = imageFiltering(frame)
	

	

	drawing = np.zeros(roi.shape,np.uint8)
	try:
		#finding contour with max area
		contour = max(contours,key=lambda x: cv2.contourArea(x),default=0)



		#convex hull
		hull = cv2.convexHull(contour)

		
		cv2.drawContours(drawing,[contour],-1,(0,255,0),0)
		cv2.drawContours(drawing,[hull],-1,(0,0,255),0)
		
		

		hull = cv2.convexHull(contour,returnPoints = False)
		defects = cv2.convexityDefects(contour,hull)

		count_defects = 0 

		#finding defects and displaying them on the image
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(contour[s][0])
			end = tuple(contour[e][0])
			far = tuple(contour[f][0])
			#cv2.line(drawing,start,end,[0,255,0],2)
			#cv2.circle(drawing,far,5,[0,0,255],-1)

			a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
			b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
			c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
			angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

			if angle <= 90:
				count_defects += 1
				cv2.circle(drawing,far,5,[0,0,255],-1)

			cv2.line(drawing,start,end,[0,255,0],2)

		if count_defects == 0:
			cv2.putText(frame, "ONE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
		elif count_defects == 1:
			cv2.putText(frame, "TWO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		elif count_defects == 2:
			cv2.putText(frame, "THREE", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		elif count_defects == 3:
			cv2.putText(frame, "FOUR", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		elif count_defects == 4:
			cv2.putText(frame, "FIVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
		else:
			pass

	except:
		pass
	cv2.imshow("thresh",thresh)
	cv2.imshow("drawing",drawing)
	cv2.imshow("img",frame)



	k = cv2.waitKey(30) & 0xff #exit if Esc is pressed
	if k == 27:
		break

cap.release() #release the webcam
cv2.destroyAllWindows() #destroy the window