import cv2 as cv
import time
import random
import RPi.GPIO as gp
import  math
import numpy as np
import os
from PIL import Image, ImageEnhance
import vp
import serial
import struct

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(40, gp.OUT)
gp.setup(38, gp.IN)

def main():
	cam = cv.VideoCapture(0)
	while(not(cam.isOpened())):
		print("Camera0 is disconnected")
		time.sleep(1)
	cam.set(cv.CAP_PROP_FRAME_WIDTH, 3280)
	cam.set(cv.CAP_PROP_FRAME_HEIGHT, 2464)
	cam.set(cv.CAP_PROP_EXPOSURE, -4)
	cam.set(cv.CAP_PROP_AUTO_EXPOSURE, 0.75)
	cam.set(cv.CAP_PROP_FPS,30.0)
	cam1 = cv.VideoCapture(2)
	while(not(cam1.isOpened())):
		print("Camera1 is disconnected")
		time.sleep(1)
	cam1.set(cv.CAP_PROP_FRAME_WIDTH, 3280)
	cam1.set(cv.CAP_PROP_FRAME_HEIGHT, 2464)
	#cam1.set(cv.CAP_PROP_AUTO_EXPOSURE,1)
	cam1.set(cv.CAP_PROP_EXPOSURE,-4)
	cam1.set(cv.CAP_PROP_AUTO_EXPOSURE,0.75)
	cam1.set(cv.CAP_PROP_FPS,30.0)
	#cam2 = cv.VideoCapture(4)
	#cam2.set(cv.CAP_PROP_FRAME_WIDTH, 3280)
	#cam2.set(cv.CAP_PROP_FRAME_HEIGHT, 2464)
	#cam3 = cv.VideoCapture(6)
	#cam3.set(cv.CAP_PROP_FRAME_WIDTH, 3280)
	#cam3.set(cv.CAP_PROP_FRAME_HEIGHT, 2464)
	imu = gp.input(38)
	start_time = time.time()
	end_time = time.time()
	token = random.randint(0, 65536)
	buzzer = True
	i=0
        while not gp.input(38):
                time.sleep(0.1)
                gp.output(40, buzzer)
                buzzer = not(buzzer)
	#while (True):
        while gp.input(38) and (end_time - start_time) < (60*30):
                #if (i%5==0):
                gp.output(40,buzzer)
                buzzer = not(buzzer)
                end_time = time.time()
                print((end_time-start_time)*1000)
                ret, image = cam.read()
                ret1,image1 = cam1.read()
                #ret2,image2 = cam2.read()
                #ret3,image3 = cam3.read()
                end_time = time.time()
                print((end_time-start_time)*1000)
                cv.imwrite("/home/pi/final_pics/cam0-%d-%d.jpg" % (token,i),image)
                i+=1
                cv.imwrite("/home/pi/final_pics/cam1-%d-%d.jpg" % (token,i),image1)
                i+=1
                #cv2.imwrite("/home/pi/cam2-%d-%d.jpg" % (token,i),image2)
                #
                #cv2.imwrite("/home/pi/cam3-%d-%d.jpg" % (token,i),image3)
                #i+=1
        cam.release()
        cam1.release()
        #cam2.release()
        #cam3.release()
	#gp.output(40,False)

        result = vp.vision_processing()
        print(result)
        #result = [1462, 0, 0, 522]

        while not gp.input(38):
                time.sleep(0.1)
        ser = serial.Serial('/dev/ttyS0')
        # arduino expects results in the order (green, orange, blue), while VP provides (orange, lavendar, blue, green)
        ser.write(struct.pack('<III', result[3], result[0], result[2]))


#ret = vp.vision_processing()

if __name__ == "__main__":
	main()
