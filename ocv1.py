# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import RPi.GPIO as GPIO
from time import sleep
flag = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(37,GPIO.OUT)





 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
 
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
	# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=300)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
##	mask = cv2.erode(mask, None, iterations=2)
##	mask = cv2.dilate(mask, None, iterations=2)
 
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)                        
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		X = int(M["m10"] / M["m00"])
		if X<170 and X>130:
			flag=0
		elif X>170:
			flag = 1
		elif X<130:
			flag =-1
		print(X)
		
 




	if flag ==0:
##		D2A = GPIO.PWM(16,100)
		GPIO.output(15,GPIO.HIGH)
		GPIO.output(16,GPIO.HIGH)                
		GPIO.output(35,GPIO.HIGH)
		GPIO.output(37,GPIO.LOW)
		GPIO.output(22,GPIO.LOW)
		GPIO.output(18,GPIO.HIGH)
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(13,GPIO.LOW)
##		D3A = GPIO.PWM(15,100)
##		D2A.start(85)
##		D3A.start(53)
##	elif flag==-1:


##		A = GPIO.PWM(16,100)
##		GPIO.output(22,GPIO.LOW)		GPIO.output(18,GPIO.HIGH)
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(13,GPIO.LOW)
##		A2 = GPIO.PWM(15,100)
##		A.start(0)
##		A2.start(60)
	elif flag==1:
##		c2 = GPIO.PWM(16,100)
		GPIO.output(22,GPIO.LOW)
		GPIO.output(18,GPIO.HIGH)
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(13,GPIO.LOW)
##		c3 = GPIO.PWM(15,100)
##		c2.start(60)
##		c3.start(0)

	else:

		D2A = GPIO.PWM(16,100)
		GPIO.output(22,GPIO.LOW)
		GPIO.output(18,GPIO.LOW)
		GPIO.output(11,GPIO.LOW)
		GPIO.output(13,GPIO.LOW)
		GPIO.output(18,GPIO.LOW)
		GPIO.output(16,GPIO.LOW)
		D3A = GPIO.PWM(15,100)
		D2A.stop()
		D3A.stop()
		
		
		
		
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
print(frame.shape)
##D2A.stop()
##D3A.stop()
##c2.stop()
##c3.stop()
##A2.stop()
##A.stop()
GPIO.cleanup()
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
