"""
@data:      graphics_service.py
@author:    Leo Ertuna
@versions:  ver 0.0.0 - 05.09.2020 - Leo Ertuna
            ver 1.0.0 - 05.04.2024 - Jannis Mathiuet
@source:    https://github.com/JPLeoRX/opencv-text-deskew/tree/master/python-service/services
@desc: 
    
"""

from typing import Tuple
from PIL import Image as imageMain
from PIL.Image import Image
import tempfile
import pdf2image
import cv2
import numpy as np

# This service contains all OpenCV / PIL / PDF functions that can be reused
class GraphicsService():
    def openImagePil(self, imagePath: str) -> Image:
        return imageMain.open(imagePath)

    def convertPilImageToCvImage(self, pilImage: Image):
        return cv2.cvtColor(np.array(pilImage), cv2.COLOR_RGB2BGR)

    def convertCvImagetToPilImage(self, cvImage) -> Image:
        return imageMain.fromarray(cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB))

    def openImageCv(self, imagePath: str):
        return self.convertPilImageToCvImage(self.openImagePil(imagePath))

    def cvToGrayScale(self, cvImage):
        return cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)

    def cvApplyGaussianBlur(self, cvImage, size: int):
        return cv2.GaussianBlur(cvImage, (size, size), 1)
# *****************************************************************************
# extensions Jannis Mathiuet
# *****************************************************************************
    def cvToBlackWhite(self, cvImage, blurSize: int=1):
        # source: https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
        # 
        gray = self.cvToGrayScale(cvImage)
        blur = self.cvApplyGaussianBlur(gray, blurSize)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = cv2.bitwise_not(thresh)
        # thresh = cv2.adaptiveThreshold(cvImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #                                cv2.THRESH_BINARY, 11, 2)
        return thresh
    
    def cvApplyNoiseRemoval(self, cvImage): 
        kernel = np.ones((1, 1), np.uint8)
        cvImage = cv2.dilate(cvImage, kernel, iterations=1)
        
        kernel = np.ones((1, 1), np.uint8)
        cvImage = cv2.erode(cvImage, kernel, iterations=1)
        
        #reduces Noise
        cvImage = cv2.morphologyEx(cvImage, cv2.MORPH_CLOSE, kernel)
        cvImage = cv2.medianBlur(cvImage, 3) 
        
        # direkte Fuktion von opencv (ausprobieren) 
        # Quelle: https://docs.opencv.org/3.4/d1/d79/group__photo__denoise.html#ga4c6b0031f56ea3f98f768881279ffe93
        # cv2.fastNlMeansDenoising(im_bw, noNoise_image, 11)
        return cvImage
    
    def cvApplyThickerFont(self, cvImage, fsize: int=1):
        # funktioniert besser wenn Bild zuerst invertiert, wenn nicht ist hier Erosion
        cvImage = cv2.bitwise_not(cvImage)
        kernel = np.ones((fsize, fsize), np.uint8) # groesserer Kernel --> groesserer Filter
        cvImage = cv2.dilate(cvImage, kernel, iterations=1) # iterations: Durchlaeufe
        cvImage = cv2.bitwise_not(cvImage)
        # zurueck invertieren
        return cvImage
    
    def cvApplyThinnerFont(self, cvImage, fsize: int=1):
        # funktioniert besser wenn Bild zuerst invertiert, wenn nicht ist hier Dilation
        cvImage = cv2.bitwise_not(cvImage)
        kernel = np.ones((fsize, fsize), np.uint8) # groesserer Kernel --> groesserer Filter
        cvImage = cv2.erode(cvImage, kernel, iterations=1) # iterations: Durchlaeufe
        cvImage = cv2.bitwise_not(cvImage)
        return cvImage
    
    def cvApplyRescalling(self):
        return
# *****************************************************************************  

    # Extracts all contours from the image, and resorts them by area (from largest to smallest)
    def cvExtractContours(self, cvImage):
        contours, hierarchy = cv2.findContours(cvImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        return contours

    # Apply new color to the outer border of the image
    def paintOverBorder(self, cvImage, borderX: int, borderY: int, color: Tuple[int, int, int]):
        newImage = cvImage.copy()
        height, width, channels = newImage.shape
        for y in range(0, height):
            for x in range(0, width):
                if (y <= borderY) or (height - borderY <= y):
                    newImage[y, x] = color
                if (x <= borderX) or (width - borderX <= x):
                    newImage[y, x] = color
        return newImage

    # Rotate the image around its center
    def rotateImage(self, cvImage, angle: float):
        newImage = cvImage.copy()
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage

    # Render one page of a PDF document to image
    def renderPdfDocumentPageToImageFromPath(self, pdfDocPath: str, pageNumber: int, dpi: int) -> str:
        tempFolder = tempfile.gettempdir()
        pageImagePaths = pdf2image.convert_from_path(pdfDocPath, dpi=dpi, output_folder=tempFolder, fmt='png', paths_only=True, thread_count=1, first_page=pageNumber, last_page=pageNumber)
        return pageImagePaths[0]
    
# =============================================================================
#     Deskew
# =============================================================================
    # Deskew image
    def deskew(self, cvImage) -> Tuple:
        angle = self.getSkewAngle(cvImage)
        print(angle)
        return self.rotateImage(cvImage, -1.0 * angle), angle

    # Calculate skew angle of an image
    def getSkewAngle(self, cvImage, debug: bool = False) -> float:
        # Prep image, copy, convert to gray scale, blur, and threshold
        newImage = cvImage.copy()
        gray = GraphicsService().cvToGrayScale(newImage)
        blur = GraphicsService().cvApplyGaussianBlur(gray, 11)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        if debug:
            cv2.imshow('Gray', gray)
            cv2.imshow('Blur', blur)
            cv2.imshow('Thresh', thresh)
            cv2.waitKey()

        # Apply dilate to merge text into meaningful lines/paragraphs.
        # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
        # But use smaller kernel on Y axis to separate between different blocks of text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5)) # TODO: what does this influence?
        dilate = cv2.dilate(thresh, kernel, iterations=11)          # TODO: what does this interations influence? higher Number worse results?
        if debug:
            cv2.imshow('Dilate', dilate)
            cv2.waitKey()

        # Find all contours
        contours = self.cvExtractContours(dilate)
        if debug:
            temp1 = cv2.drawContours(newImage.copy(), contours, -1, (255, 0, 0), 2)
            cv2.imshow('All Contours', temp1)
            cv2.waitKey()

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)
        if debug:
            minAreaRectContour = np.int0(cv2.boxPoints(minAreaRect))
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

