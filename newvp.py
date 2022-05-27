#---------------Dependencies---------------#
#OpenCV, numpy, matplotlib, Pillow
import cv2 as cv
from cv2 import COLOR_HSV2BGR
from cv2 import COLOR_BGR2HSV
from cv2 import COLOR_RGB2BGR
from cv2 import waitKey
import numpy as np
import os
from PIL import Image, ImageEnhance

def vision_processing():

    #Current best upper: 15, 255, 255
    #Current best lower: 3, 50, 50

    #----------------Constants------------------#
    #Used for color recognition (orange)
    #Current best upper: 15, 255, 255
    #Current best lower: 3, 50, 50
    FUSC_MIN = np.array([155, 100, 50],np.uint8)
    FUSC_MAX = np.array([165, 255, 120],np.uint8)

    #Test Orange
    ORANGE_MIN = np.array([3, 150, 50],np.uint8)
    ORANGE_MAX = np.array([15, 255, 100],np.uint8)

    #HSV range: H(0-180), S(0-255), V(0-255)
    LAV_MIN = np.array([122, 120, 100],np.uint8)
    LAV_MAX = np.array([133, 255, 255],np.uint8)

    #Blue bounds
    BLUE_MIN = np.array([100, 100, 100],np.uint8)
    BLUE_MAX = np.array([112, 255, 255],np.uint8)

    #Yellow bounds
    YELLOW_MIN = np.array([20, 80, 80],np.uint8)
    YELLOW_MAX = np.array([30, 255, 255],np.uint8)

    ORANGE_SUM = 1
    LAV_SUM = 1
    BLUE_SUM = 1
    YELLOW_SUM = 1
    FUSC_SUM = 1

    HIGHEST_AVG = 1

    iterations = 0

    #define kernel size  
    kernel = np.ones((7,7),np.uint8)

    #Used for determining how much orange color should be seen (max)
    buffer = 50
    #xborder, yborder - how many pixels will be cropped off each side of the image
    xborder, yborder = 500, 600
    #Brightness, contrast adjustment values
    brightness, contrast = 127, 127
    #Image directories

    #########       DIRECTORY GOES HERE ZAK        ###############
    dir1 = "/home/pi/final_pics"
    ##############################################################

    #These two are used for storing the picture that has the highest amount of orange pixels
    numHighestPixels = 0
    dirHighestPixels = "null"

    #Going to come back to this. This will sort the files by ascending order
    list1 = os.listdir(dir1)
    #list1 = [int(x) for x in list1]
    #list1.sort()

    #cv.namedWindow("Current", cv.WINDOW_NORMAL)

    for images in sorted(os.listdir(dir1)):

        #image = cv.imread("New/" + images)

        #This block will check if the file is corrupt

        print("Processing file: " + str(images))

        try:
            PilImg = Image.open(str(dir1 + "/" + images)).convert("HSV")
            PilImg = PilImg.crop((int(xborder), int(yborder), int(PilImg.width - xborder), int(PilImg.height - yborder)))
            #converter = ImageEnhance.Color(PilImg)
            #PilImg = converter.enhance(1.3)
            PilImg.verify() # verify that it is, in fact an image
        except (IOError, SyntaxError) as e:
            print('Bad file:', images) # print out the names of corrupt files
            continue

        #Convert the cropped image to BGR (RGB)
        PilImg = PilImg.convert("RGB")
        finalImg = np.array(PilImg)
        finalImg = cv.cvtColor(finalImg, COLOR_RGB2BGR)

        image = finalImg

        image = cv.cvtColor(image, COLOR_BGR2HSV)

        #Make all orange pixels white and all other pixels black
        mask1 = cv.inRange(image, ORANGE_MIN, ORANGE_MAX)
        mask2 = cv.inRange(image, LAV_MIN, LAV_MAX)
        mask3 = cv.inRange(image, BLUE_MIN, BLUE_MAX)
        mask4 = cv.inRange(image, YELLOW_MIN, YELLOW_MAX)
        #mask5 = cv.inRange(image, FUSC_MIN, FUSC_MAX)

        if np.sum(mask4 == 255) > (np.sum(mask1 == 255) + np.sum(mask2 == 255) + (np.sum(mask3 == 255))):
            combinedMask1 = cv.bitwise_or(mask2, mask1)
            combinedMask2 = cv.bitwise_or(combinedMask1, mask3)
            combinedMaskFinal = cv.bitwise_or(combinedMask1, combinedMask2)

        else:
            combinedMask1 = cv.bitwise_or(mask2, mask1)
            combinedMask2 = cv.bitwise_or(mask3, mask4)
            #combinedMask3 = cv.bitwise_or(combinedMask2, mask5)
            combinedMaskFinal = cv.bitwise_or(combinedMask1, combinedMask2)

        #Remove extra noise from the combined masks
        combinedMaskFinal = cv.morphologyEx(combinedMaskFinal, cv.MORPH_CLOSE, kernel)
        combinedMaskFinal = cv.morphologyEx(combinedMaskFinal, cv.MORPH_OPEN, kernel)

        target = cv.bitwise_and(image,image, mask=combinedMaskFinal)

        image = cv.cvtColor(image, COLOR_HSV2BGR)

        #Find countours and draw rectangle around the tent
        contours, hierarchy = cv.findContours(combinedMaskFinal.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2:]
        stencil = np.zeros(image.shape).astype(image.dtype)
        color = [255, 255, 255]
        cv.fillPoly(stencil, contours, color)

        if len(contours) != 0:
            mask1 = cv.drawContours(mask1, contours, -1, (0, 0, 255), 3)
            mask2 = cv.drawContours(mask2, contours, -1, (0, 0, 255), 3)
            mask3 = cv.drawContours(mask3, contours, -1, (0, 0, 255), 3)
            mask4 = cv.drawContours(mask4, contours, -1, (0, 0, 255), 3)
            #mask5 = cv.drawContours(mask5, contours, -1, (0, 0, 255), 3)


            target1 = cv.bitwise_and(image,image, mask=mask1)
            target2 = cv.bitwise_and(image,image, mask=mask2)
            target3 = cv.bitwise_and(image,image, mask=mask3)
            target4 = cv.bitwise_and(image,image, mask=mask4)
            #target5 = cv.bitwise_and(image,image, mask=mask5)

            c = max(contours, key = cv.contourArea)
            x,y,w,h = cv.boundingRect(c)
            cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

            result1 = cv.bitwise_and(target1, stencil)
            result2 = cv.bitwise_and(target2, stencil)
            result3 = cv.bitwise_and(target3, stencil)
            result4 = cv.bitwise_and(target4, stencil)
            #result5 = cv.bitwise_and(target5, stencil)

            ORANGE_SUM = ORANGE_SUM + np.sum(result1 != 0)
            LAV_SUM = LAV_SUM + np.sum(result2 != 0)
            BLUE_SUM = BLUE_SUM + np.sum(result3 != 0) 
            YELLOW_SUM = YELLOW_SUM + np.sum(result4 != 0)
            #FUSC_SUM = FUSC_SUM + np.sum(result5 != 0)



            iterations += 1
        

    if iterations < 1:
        iterations = 1

    if ((BLUE_SUM / iterations) > 4000):
        BLUE_SUM = 0

    if ((YELLOW_SUM / iterations) > 4000):
        YELLOW_SUM = 0


    #print("Orange Average: " + str(ORANGE_SUM / iterations))
    #print("Lavender Average: " + str(LAV_SUM / iterations))
    #print("Blue Average: " + str(BLUE_SUM / iterations))
    #print("Yellow Average: " + str(YELLOW_SUM / iterations))
    #print("Fuschia Average: " + str(FUSC_SUM / iterations))


    ret = [(ORANGE_SUM / iterations), (LAV_SUM / iterations), (BLUE_SUM / iterations), (YELLOW_SUM / iterations)]
    return ret

if __name__ == '__main__':
        print(vision_processing())
