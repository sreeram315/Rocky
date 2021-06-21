import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
import requests
import base64
import json

from utils import *
from constants import *


def extract_reg_number(image_name):
	try:
		img = cv2.imread(image_name,cv2.IMREAD_COLOR)

		img = cv2.resize(img, (620,480) )

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
		gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
		edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

		# find contours in the edged image, keep only the largest
		# ones, and initialize our screen contour
		cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
		screenCnt = None

		# loop over our contours
		for c in cnts:
		 # approximate the contour
		 peri = cv2.arcLength(c, True)
		 approx = cv2.approxPolyDP(c, 0.018 * peri, True)
		 
		 # if our approximated contour has four points, then
		 # we can assume that we have found our screen
		 if len(approx) == 4:
		  screenCnt = approx
		  break

		if screenCnt is None:
		 detected = 0
		 print ("No contour detected")
		else:
		 detected = 1

		if detected == 1:
		 cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

		# Masking the part other than the number plate
		mask = np.zeros(gray.shape,np.uint8)
		new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
		new_image = cv2.bitwise_and(img,img,mask=mask)

		# Now crop
		(x, y) = np.where(mask == 255)
		(topx, topy) = (np.min(x), np.min(y))
		(bottomx, bottomy) = (np.max(x), np.max(y))
		Cropped = gray[topx:bottomx+1, topy:bottomy+1]

		#Read the number plate
		text = pytesseract.image_to_string(Cropped, config='--psm 6')
		text = remove_chars_from_string(text, UNWANTED_CHARS)
		reg_number = text.replace(' ', '')
		reg_number = (((requests.post(url='https://www.de-vis-software.ro/platebber.aspx',headers={"Authorization": 'Basic %s' %  base64.b64encode(b"sreerammaram2@gmail.com:sreerAM31@").decode("ascii"),"Content-Type": "application/json","Accept": "application/json"},data=json.dumps({"base64ImageString": '%s' % base64.b64encode((open(image_name, "rb")).read()).decode("ascii"),"languageCode": "auto","plate_output": "no"}))).json())[0]['plate_text'].split('|')[0]).strip()
		reg_number = remove_chars_from_string(reg_number, UNWANTED_CHARS)
		print("Detected Number is:",reg_number)
	except:
		reg_number = (((requests.post(url='https://www.de-vis-software.ro/platebber.aspx',headers={"Authorization": 'Basic %s' %  base64.b64encode(b"sreerammaram2@gmail.com:sreerAM31@").decode("ascii"),"Content-Type": "application/json","Accept": "application/json"},data=json.dumps({"base64ImageString": '%s' % base64.b64encode((open(image_name, "rb")).read()).decode("ascii"),"languageCode": "auto","plate_output": "no"}))).json())[0]['plate_text'].split('|')[0]).strip()
		reg_number = remove_chars_from_string(reg_number, UNWANTED_CHARS)
		print("Detected Number is:",reg_number)
	return str(reg_number)
