"""
@data:      image_enhancing.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 01.04.2024 - Jannis Mathiuet
@desc: 
    Image enhancing functions like denoising or skewing
    
"""
from typing import Tuple
import cv2
import numpy

# Calculate skew angle of an image
def getSkewAngle(cvImage, debug: bool = False):
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    if debug:
        cv2.imshow('Gray', gray)
        cv2.imshow('Blur', blur)
        cv2.imshow('Thresh', thresh)
        cv2.waitKey()
    
    
    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=5)
    
    if debug:
        cv2.imshow('Dilate', dilate)
        cv2.waitKey()

    # Find all contours
    contours = 
    if debug:
        temp1 = cv2.drawContours(newImage.copy(), contours, -1, (255, 0, 0), 2)
        cv2.imshow('All Contours', temp1)
        cv2.waitKey()

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    minAreaRect = cv2.minAreaRect(largestContour)
    if debug:
        minAreaRectContour = numpy.int0(cv2.boxPoints(minAreaRect))
        temp2 = cv2.drawContours(newImage.copy(), [minAreaRectContour], -1, (255, 0, 0), 2)
        cv2.imshow('Largest Contour', temp2)
        cv2.waitKey()

    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
        return -1.0 * angle
    elif angle > 45:
        angle = 90 - angle
        return angle
    return -1.0 * angle

    # As your page gets more complex you might want to look into more advanced angle calculations
    #
    # Maybe use the average angle of all contours.
    # allContourAngles = [cv2.minAreaRect(c)[-1] for c in contours]
    # angle = sum(allContourAngles) / len(allContourAngles)
    #
    # Maybe take the angle of the middle contour.
    # middleContour = contours[len(contours) // 2]
    # angle = cv2.minAreaRect(middleContour)[-1]
    #
    # Maybe average angle between largest, smallest and middle contours.
    # largestContour = contours[0]
    # middleContour = contours[len(contours) // 2]
    # smallestContour = contours[-1]
    # angle = sum([cv2.minAreaRect(largestContour)[-1], cv2.minAreaRect(middleContour)[-1], cv2.minAreaRect(smallestContour)[-1]]) / 3
    #
    # Experiment and find out what works best for your case.
    
    
    
# Rotate the image around its center
def rotateImage(self, cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage