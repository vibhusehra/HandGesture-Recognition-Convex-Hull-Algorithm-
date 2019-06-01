# Hand Gesture Recognition Using Convex Hull Algorithm

<p>A set of points is defined to be convex if it contains the line segments connecting each pair of its points. In this project we create
a convex hull around the hand using openCV library. After obtaining the Convex Hull, we find the number of fingers by finding out the defects
in that figure.</p>

## Prerequisites


**Libraries Required:**

- numpy 1.13.1
- opencv-contrib-python 4.0.0.21

## Working
1. First we preprocess the image by applying operations like gaussian blur, thresholding. 
2. Next step is to find the contours in the image.
3. The contour with the largest area(our hand) is used in drawing a complex hull.
4. We find the defects in that convex hull. These defects will be considered only if their angle is <=90 degree.
(These defects will help us in finding the number of fingers).
- zero defects = 1
- one defect = 2
- two defects = 3
- three defects = 4
- four defects = 5

## Demo


<img src="https://github.com/vibhusehra/HandGesture-Recognition-Convex-Hull-Algorithm-/blob/master/demo.gif" width="500" height="500" />
