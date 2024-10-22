"""
@data:      graphics_service.py
@author:    Leo Ertuna
@versions:  ver 0.0.0 - 05.09.2020 - Leo Ertuna
            ver 1.0.0 - 05.04.2024 - Jannis Mathiuet
            ver 2.0.0 - 20.05.2024 - Jannis Mathiuet (final version)
@source:    https://github.com/JPLeoRX/opencv-text-deskew/tree/master/python-service/services
            (for some of the code)
@desc: 
    multiple functions for image processing
    some are currently not used
    
"""

from typing import List, Tuple
import cv2
import numpy as np
import matplotlib.pyplot as plt
# from src.file_handling import FileHandling

# This service contains all OpenCV and display functions that can be reused
class GraphicsService():
    
    def imgPreperationUser(self, cvImage):
        user_satisfied = False
        previous_img = [cvImage.copy()]
        while(not user_satisfied):
            print("aktueller Stand: ", len(previous_img))
            current_img = previous_img[-1]
            show_img = self.cvApplyRescaling(current_img, 0.2)
            cv2.imshow("q: abbrechen, w:weiter, c:zuscheiden, f: 180deg drehen, r:zurueck", show_img)
            
            key = cv2.waitKey(0)
            if key == ord('c'):
                new_img = self.cropManual(current_img)
                previous_img.append(new_img)
                
            if key == ord('f'): 
                new_img = cv2.rotate(current_img, cv2.ROTATE_180)
                previous_img.append(new_img)
                
            if key == ord('r'): 
                if len(previous_img) != 1:
                    del previous_img[-1]
                    
            if key == ord('w') or key == 13:
                user_satisfied = True
                
            if key == ord('q') or key == 27:
                cv2.destroyAllWindows()
                return cvImage, False
            
        cv2.destroyAllWindows()
        img = previous_img[-1]
        del previous_img
        return img, True
    
    
    
    def displayImage(self, path:str):
        if type(path) is not str:
            try: 
                cv2.imshow("img", path)
            except:
                print("not image or path")
        else: 
            dpi = 80
            im_data = plt.imread(path)
            height, width = im_data.shape[:2]
            
            # What size does the figure need to be in inches to fit the image?
            figsize = width / float(dpi), height / float(dpi)
            
            # Create a figure of the right size with one axes that takes up the full figure
            fig = plt.figure(figsize=figsize)
            ax = fig.add_axes([0, 0, 1, 1])
            
            # Hide spines, ticks, etc.
            ax.axis('off')
            
            # Display the image.
            ax.imshow(im_data, cmap='gray')
            plt.show()
            
        return None
    
    
    
    def cropManual(self, cvImage):
        image = cvImage.copy()  
        # Skalieren des Bildes für die Auswahl
        scale = 0.2 # Skalierungsfaktor, kann nach Bedarf angepasst werden
        small_image = cv2.resize(image, None, fx=scale, fy=scale)
        
        # Select a region of interest (ROI)
        img_name = "Select ROI and press Enter to confirm"
        roi = cv2.selectROI(img_name, small_image)
        cv2.destroyAllWindows()
        # cv2.destroyWindow(img_name)
        x, y, w, h = roi
        
        #Auf Originalbild umrechnen
        x = int(x / scale)
        y = int(y / scale)
        w = int(w / scale)
        h = int(h / scale)
        
        # Bild ausschneiden
        cropped_img = cvImage[y:y+h, x:x+w]
        cropped_img = self.cvRemoveBorders(cropped_img)
        rotate = self.deskew(cropped_img)    #Bild nach Zeile ausrichten

        return rotate
    
    
    
    def fill_contour2border(self, cvImage, contour, white: bool):
        # Create a mask with the same dimensions as the image
        mask = np.zeros_like(cvImage)

        # Fill the largest contour on the mask
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)

        # Invert the mask to fill the area outside the contour
        inverted_mask = cv2.bitwise_not(mask)

        # Fill the area between the largest contour and the image border
        cvImage[inverted_mask == 255] = white*255
        newImage = cv2.drawContours(cvImage, [contour], -1, white*(255, 255, 255), thickness=cv2.FILLED)
        return newImage
    
    
    
    def cvToGrayScale(self, cvImage): 
        if (len(cvImage.shape) != 3): 
            print("Grayscale is not applicable")
            return cvImage
        return cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)



    def cvApplyGaussianBlur(self, cvImage, size: int):
        if type(size) is not int:
            size = 1
            print("Error! Please use int for size")
        if size <= 0:
            size = 1
        if not(size % 2):
            size += 1
        return cv2.GaussianBlur(cvImage, (size, size), 1)



    def cvToBlackWhite(self, cvImage, blurSize: int=1): # returns white image with black highlights (e.g.text)
        # source: https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
        gray = self.cvToGrayScale(cvImage)
        blur = self.cvApplyGaussianBlur(gray, blurSize)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = cv2.bitwise_not(thresh)
        return thresh
    
    def cvApplyNoiseRemoval(self, cvImage): 
        kernel = np.ones((1, 1), np.uint8)
        cvImage = cv2.dilate(cvImage, kernel, iterations=1)
        
        kernel = np.ones((1, 1), np.uint8)
        cvImage = cv2.erode(cvImage, kernel, iterations=1)
        
        #reduces Noise
        cvImage = cv2.morphologyEx(cvImage, cv2.MORPH_CLOSE, kernel)
        cvImage = cv2.medianBlur(cvImage, 3) 
        
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
    
    def cvApplyRescaling(self, cvImage, scale: float=1.0):        
        rescaledImage = cvImage
        if (scale < 1.0) : 
            rescaledImage = cv2.resize(cvImage, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if (scale > 1.0) : 
            rescaledImage = cv2.resize(cvImage, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        return rescaledImage
    
    def cvRemoveBorders(self, cvImage): 
        # Don't use for PDF!
        # Don't use for automated task
        binary = self.cvToBlackWhite(cvImage, 11)
        contours = self.cvExtractContours(binary)
        largestContour = contours[0]
        x, y, w, h = cv2.boundingRect(largestContour)
        
        # print(cv2.boundingRect(largestContour))
        # crop = cvImage
        crop = cvImage[y:y+h, x:x+w]
        return crop
    

    # Extracts all contours from the image, and resorts them by area (from largest to smallest)
    def cvExtractContours(self, img_binary):
        DEBUG = False
        
        # img = self.cvToBlackWhite(cvImage, 101)
        # binary_inv = cv2.bitwise_not(binary)
        if DEBUG:
            # resc_binary = self.cvApplyRescaling(binary, 0.2)
            # resc_binary_inv = self.cvApplyRescaling(binary_inv, 0.2)
            cv2.imshow("binary", img_binary)
            # cv2.imshow("inverted", resc_binary_inv)
        
        # cv2.imshow("test", binary)
        contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        return contours

    # Apply new color to the outer border of the image
    def paintOverBorder(self, cvImage, borderX: int, borderY: int, color: Tuple[int, int, int], linewidth: int):
        newImage = cvImage.copy()
        height, width = newImage.shape[:2]
        height -= (1+linewidth)
        width -= (1+linewidth)
        
        isGray = False
        if len(newImage.shape) == 2:
            newImage = cv2.cvtColor(newImage, cv2.COLOR_GRAY2BGR)
            isGray = True
        cv2.rectangle(newImage, (0,0), (width, height), color, linewidth)

        # for y in range(0, height):
        #     for x in range(0, width):
        #         if (y <= borderY) or (height - borderY <= y):
        #             newImage[y, x] = color
        #         if (x <= borderX) or (width - borderX <= x):
        #             newImage[y, x] = color
        if isGray:
            newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        return newImage

    # Rotate the image around its center
    def rotateImage(self, cvImage, angle: float):
        newImage = cvImage.copy()
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage

# =============================================================================
#     Deskew
# =============================================================================
    # Deskew image
    def deskew(self, cvImage) -> Tuple:
        h_img, w_img = cvImage.shape[:2]
        if (h_img < w_img):
            cvImage = cv2.rotate(cvImage, cv2.ROTATE_90_CLOCKWISE)
        skewangle = self.getSkewAngle(cvImage, False)
        # print(angle)
        # return self.rotateImage(cvImage, -1.0 * angle), angle
        return self.rotateImage(cvImage, -1.0 * skewangle)

    # Calculate skew angle of an image
    def getSkewAngle(self, cvImage, debug: bool = False) -> float:
        # Prep image, copy, convert to gray scale, blur, and threshold
        newImage = cvImage.copy()
        if debug:  
            temp = self.cvApplyRescaling(newImage, 0.2)
            cv2.imshow('Input', temp)
        # gray = GraphicsService().cvToGrayScale(newImage)
        # blur = GraphicsService().cvApplyGaussianBlur(gray, 11)
        # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        thresh = self.cvToBlackWhite(newImage, 101)
        if debug:
            
            # cv2.imshow('Gray', gray)
            # cv2.imshow('Blur', blur)
            temp0 = self.cvApplyRescaling(thresh, 0.2)
            cv2.imshow('Thresh', temp0)
            pass

        # Apply dilate to merge text into meaningful lines/paragraphs.
        # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
        # But use smaller kernel on Y axis to separate between different blocks of text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 6)) 
        dilate = cv2.dilate(thresh, kernel, iterations=3)
        
        dilate = thresh
        if debug:
            pass
            #cv2.imshow('Dilate', dilate)

        # Find all contours
        contours = self.cvExtractContours(dilate)
        if debug:
            temp1 = cv2.drawContours(newImage.copy(), contours, -1, (255, 0, 0), 2)
            temp1 = self.cvApplyRescaling(temp1, 0.2)
            cv2.imshow('All Contours', temp1)

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)
        print(minAreaRect)
        if debug:
            minAreaRectContour = np.int0(cv2.boxPoints(minAreaRect))
            temp2 = cv2.drawContours(newImage.copy(), [minAreaRectContour], -1, (255, 0, 0), 2)
            temp2 = self.cvApplyRescaling(temp2, 0.2)
            cv2.imshow('Largest Contour', temp2)
            
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
