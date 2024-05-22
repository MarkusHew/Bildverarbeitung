# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:00:16 2024

@author: janni
"""

import cv2
import numpy as np
import imutils # not needed?
try: 
    from src.graphics_service import GraphicsService
except Exception as e:
    print(e)

# only testing
import os

# =============================================================================
# functions
# =============================================================================
class ItemExtraction():    
    def get_tableofitems(self, cvImage, tablenum:int, getcols: bool=False):
        TABLE_NUMBER = tablenum # statring at 0
        
        rows_img = self.get_receipt_row_images(cvImage)
       
        table_img = rows_img[TABLE_NUMBER]
        tablecols_img = self.get_table_col_images(table_img)
# =============================================================================
#         cv2.imshow("TABLE", table_img)
#         cv2.waitKey(0)
# =============================================================================
        cv2.destroyAllWindows()
        return (table_img, tablecols_img)


    def get_receipt_row_images(self, cvImage):
        grs = GraphicsService()
        img_height, img_width = cvImage.shape[:2]
        morph_rect_width  = img_width//2
        morph_rect_height = img_width//40 # width const, but height variable due to amounts of items
        kernel_noise = 3

        
        thresh = self.apply_thresh(cvImage)

        thresh = self.reduce_noise(thresh, kernel_noise)
        test_noiseremove = thresh
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morph_rect_width, morph_rect_height))
        thresh = cv2.dilate(thresh, kernel, iterations=1) 
        
# =============================================================================
#         test_img = grs.cvApplyRescaling(cvImage, 0.3)
#         test_thresh = grs.cvApplyRescaling(thresh, 0.3)
#         test_noiseremove = grs.cvApplyRescaling(test_noiseremove, 0.3)
#         
#         cv2.imshow("test_img", test_img)
#         cv2.imshow("test_thresh", test_thresh)
#         cv2.imshow("test_noiseremove", test_noiseremove)
# =============================================================================
        
        cnts, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # returns tuple with Array of int32
        cnts = imutils.grab_contours((cnts, hierarchy))
        filtered_cnts = self.filter_contours(cnts, img_width, centering=True, filtering=False)
        row_images = self.crop_images(cvImage, filtered_cnts)
        
        return row_images

    def get_table_col_images(self, table_img):
        table_height, table_width = table_img.shape[:2]
        
        table_thresh = self.apply_thresh(table_img)
        table_thresh = self.reduce_noise(table_thresh, 5)
        
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (table_width//31, table_height//2))
        table_thresh = cv2.dilate(table_thresh, kernel, iterations=1)
        # cv2.imshow("table_dilate", table_thresh)
        cnts, hierarchy = cv2.findContours(table_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # returns tuple with Array of int32
        cnts = imutils.grab_contours((cnts, hierarchy))
        
        filtered_cnts = self.filter_contours(cnts, table_width, centering=None, filtering='h')
        
        tablecols_img = self.crop_images(table_img, filtered_cnts)
        return tablecols_img





    # =============================================================================
    # helping functions
    # =============================================================================
    def filter_contours(self, contours, image_width, **kwargs):
    # flags 
        centering = False
        filtering = ""
        
        filtering_types = ['h','w','b'] #h:height, w:width, b:both
        
        # extract kwargs 
        for key, value in kwargs.items():
            if key == 'centering' : 
                if value == True :
                    centering = True
            if key == 'filtering' :
                if value in filtering_types:
                    filtering = value
        # functions
        def check_middle(distance_from_middle):
            nonlocal max_distance_from_middle
            nonlocal centering

            if centering:
                return (distance_from_middle <= max_distance_from_middle)
            return True
        
        def check_height(h):
            nonlocal median_h
            nonlocal filtering
            if filtering in ['h', 'b']:
                return (h >= median_h)
            return True
            
            
        def check_width(w):
            nonlocal median_w
            nonlocal filtering
            if filtering in ['w', 'b']:
                return (w >= median_w)
            return True
           
        # Calculate the middle of the image
        middle_x = image_width // 2

        # Threshold distance from the middle
        max_distance_from_middle = image_width // 5  # Adjust this value as needed
            
            
        median_h, median_w = self.get_median_sizes(contours)
            
        filtered_contours = []
        for contour in contours:
            # Find the bounding rectangle for the contour
            x, y, w, h = cv2.boundingRect(contour)
                
    # =============================================================================
    #             if centering == True:
    # =============================================================================
            # Calculate the center of the bounding rectangle
            contour_center_x = x + (w // 2)

            # Calculate the distance of the contour's center from the middle
            distance_from_middle = abs(contour_center_x - middle_x)
            
            if check_middle(distance_from_middle) and check_height(h) and check_width(w):
                filtered_contours.append(contour) 
        filtered_contours.reverse()
        print("amount of filtered contours: ", len(filtered_contours))
        return filtered_contours
        
    def apply_thresh(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # initialize a rectangular kernel that is ~5x wider than it is tall,
        # then smooth the image using a 3x3 Gaussian blur and then apply a
        # blackhat morpholigical operator to find dark regions on a light background
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (51, 11))
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
        # cv2.imshow("blackhat", blackhat)
        
        # compute the Scharr gradient of the blackhat image and scale the result into the range [0, 255]
        grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        grad = np.absolute(grad)
        (minVal, maxVal) = (np.min(grad), np.max(grad))
        grad = (grad - minVal) / (maxVal - minVal)
        grad = (grad * 255).astype("uint8")

        # apply a closing operation using the rectangular kernel to close gaps in between characters, 
        #apply Otsu's thresholding method, and finally a dilation operation to enlarge foreground regions
        grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, kernel)
        
        
        # cv2.imshow("gradient", grad)
        # thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # cv2.imshow("gradient THRESH", thresh)
        
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # thresh = cv2.bitwise_not(thresh)
        # thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return thresh

    def crop_images(self, cvImage, contours):
        crops = []    
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            crops.append(cvImage[y:y+h, x:x+w])
        if not crops:
            return [cvImage]
        return crops

    def reduce_noise(self, thresh, kernelsize:int=3):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        return opening
        
    def get_median_sizes(self, contours):
        # Lists to store heights and widths of contours
        heights = []
        widths = []
        
        # Iterate through each contour
        for cnt in contours:
            # Extract the bounding rectangle coordinates
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Append height and width to respective lists
            heights.append(h)
            widths.append(w)
        
        # Check if the lists are not empty
        if not heights or not widths:
            return None
        
        # Calculate the median height and width
        median_h = int(np.median(heights))
        median_w = int(np.median(widths))
        
        # Return the median height and width as a tuple
        return  (median_h, median_w)

# =============================================================================
# TESTING
# =============================================================================
def main():
    images_list = ["image.tif", 
                   "CoopRechnung2.jpg", 
                   "03052024_Migros_Jannis.jpg",
                   "(2)120524_Coop_Haag_Chur.tif",
                   "120524_Coop_ChurWest.tif",
                   "120524_Coop_Haag_Chur.tif",
                   "120524_CoopB+H_Chur.tif"]
    args = {
    	"image": images_list[-4],
    	"output": "results.csv",
    	"min_conf": 0,
    	"dist_thresh": 25.0,
    	"min_size": 2,
    }
    current_directory = os.path.join(os.getcwd(), os.pardir)
    print("Aktuelles Verzeichnis:", current_directory)
    Verzeichnis=os.path.join(current_directory,"in", args["image"])
    image = cv2.imread(Verzeichnis)
    
    table, cols = ItemExtraction().get_tableofitems(image, 3)
    
    
    image = GraphicsService.cvApplyRescaling(image, 0.2)
    
    cv2.imshow("image", image)
    cv2.imshow("table", table)
    
    for i in range(0, len(cols)): 
        col = cols[i]
        col = GraphicsService.cvApplyRescaling(col, 0.4)
        cv2.imshow("col_"+str(i), col)
    
    cv2.waitKey()
    return 0

if __name__ == "__main__":
    from graphics_service import GraphicsService
    grs = GraphicsService()
    main()
    
    
    