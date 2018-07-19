"""
ITSP 2018
Scribble by Four-Play

Master program which captiures the frame, passes it to the specified model and predicts the written letter

"""
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import pickle
import collection
from keras.models import load_model
import scipy.ndimage as ireader
import PIL 
from PIL import Image
import os
import keras

#Load model
modelname='neilnei.h5'
model=load_model('./Models/'+modelname)
print("Model ready")

#String which collects each character
finalstring=""
pickle.dump(finalstring, open('finalstring.p','wb'))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# Define the BGR values of the LED glow

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

#Store points for each contour
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcamç
if not args.get("video", False):
	vs = VideoStream(src=0).start()

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)
points=[]

# keep looping

#trackingpen indicates is true if a letter is being drawn
trackingpen=False

#Index of letter being tracked
count=0

#Number of strokes in current letter
strokecount=0

#Below parameters are stored in order to detect a space character/new line character
widthX=[]
widthY=[]
maxX=[]
minX=[]
maxY=[]
minY=[]

#Stores boolean values. True if pen is pressed against a surface
detected=[True]*2000

#Keep looping
while True:
	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (1, 1), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		# print(M)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size (calculated by calibrating with size of LED glow)
		if radius > 0.1:
			#Update trackingpen boolean
			trackingpen=True
			detected.append(True)

			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			points.append((x,y))
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		else:
			#Update trackingpen boolean
			trackingpen=False
			detected.append(False)
	else:
		trackingpen=False
		detected.append(False)

	# update the points queue
	pts.appendleft(center)
	
	#Number of frames after which the letter is converted to jpeg. Divide by 30 to get time in seconds. This is the minimum time between two letters
	gap=70

	#check is true if the current keystroke data should be saved to a jpeg
	check = False
	if strokecount<=1:
		for i in range(1,gap):
			if detected[-i]==True:
				check = True
	#No lowercase letter has more than 2 strokes. So as soon as two strokes are detected, stop waiting for more strokes
	elif strokecount>=2:
		for i in range(1,8):
			if detected[-i]==True:
				check = True

	#Once pen is lifted, trackingpen becomes False and a vector of keystroke data for that particular set of strokes is dumped
	if trackingpen==False and len(points) != 0:
		pickle.dump(points, open('../Vectors/boundedVec_'+str(count)+'_'+str(strokecount)+'.p','wb'))
		strokecount+=1
		points=[]

	#Calculate bounding bow paramters in order to detect space and newline. Dumped vectors are read and sent to the model for prediction
	if check==False and strokecount!=0:
		
		#Read and store keystroke data for that particular data. Loop for multiple keystrokes(max=2)
		dispx,dispy,dat=[],[],[]
		for i in range(strokecount):
			dat.append(pickle.load(open('../Vectors/boundedVec_'+str(count)+'_'+str(i)+'.p','rb')))

		#Flip the data laterally since webcam detects it in an inverted orientation
		for i in range(len(dat)):	
			dispx.append([-p[0] for p in dat[i]])
			dispy.append([-p[1] for p in dat[i]])

		#Calculate the max and min (x,y) for the letter. This data is used for space and newline
		maxdx,mindx,maxdy,mindy=dispx[0][0],dispx[0][0],dispy[0][0],dispy[0][0]
		for i in range(len(dat)):
			for j in range(len(dispx[i])):
				if dispx[i][j] > maxdx :
					maxdx=dispx[i][j]
				if mindx >= dispx[i][j] :
					mindx=dispx[i][j]
			for j in range(len(dispy[i])):
				if dispy[i][j]>maxdy:
					maxdy=dispy[i][j]
				if mindy>=dispy[i][j]:
					mindy=dispy[i][j]

		#Store max and min (x,y) values for each letter and use the previous one to detect if a space or new line should be inserted
		maxX.append(maxdx)
		maxY.append(maxdy)
		minX.append(mindx)
		minY.append(mindy)
		widthX.append(maxdx- mindx)
		widthY.append(maxdy-mindy)

		if len(widthX)>=2:
			
			#If difference of previous y values if greater than 0.6*(average y) -> insert newline
			newline=False
			if (minY[-2]-maxY[-1])>(0.6*sum(widthY)/len(widthY)):
				newline=True
				finalstring += '\n'
				# print("New line detected")

			#Similarly, insert space if next letter is at a distance of 1.25*average of previous letter's maximum x coordinate
			if (minX[-1] - maxX[-2])>(1.25*sum(widthX)/len(widthX)) and newline==False:
				finalstring += ' '
				# print("Space detected")

		#Converts vector to jpeg
		collection.ptoj(count,strokecount)
		
		#
		detected.append(True)

		#Add predicted letter to finalstring
		finalstring += collection.predict(count,model)

		#Dump characters detected till-now to a pickle file
		pickle.dump(finalstring, open('finalstring.p','wb'))
		
		#Increment number of letters tracked. Reset stroke count to zero for next letter
		count += 1
		strokecount=0
		

	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()

# close all windows

cv2.destroyAllWindows()