# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:00:16 2024

@author: janni
"""
import cv2
import numpy as np
import imutils

# only testing
import os
from graphics_service import GraphicsService
grs = GraphicsService()

def filter_contours(contours, image_width, **kwargs):
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
        
        
    median_h, median_w = get_median_sizes(contours)
        
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
        # Check if the contour is within the threshold distance from the middle
        # if distance_from_middle <= max_distance_from_middle:
        #     if (h >= median_h) and (w >= median_w):
        #         filtered_contours.append(contour) 
        
        if check_middle(distance_from_middle) and check_height(h) and check_width(w):
            filtered_contours.append(contour) 
    filtered_contours.reverse()
    print("amount of filtered contours: ", len(filtered_contours))
    return filtered_contours
    
def apply_thresh(image):
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
    
    
    
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # thresh = cv2.bitwise_not(thresh)
    # thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh


def get_tableofitems(cvImage):
    TABLE_NUMBER = 3 # statring at 0
    
    img_height, img_width = cvImage.shape[:2]
    morph_rect_width  = int(img_width/2)
    # morph_rect_width = int(1)
    morph_rect_height = int(img_height/100)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morph_rect_width, morph_rect_height))
    
    thresh = apply_thresh(cvImage)
    dilate = cv2.dilate(thresh, kernel, iterations=1) 
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # dilate = cv2.erode(dilate, kernel, iterations=3)
    # cv2.imshow("dilate", dilate)
    # cnts, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # returns tuple with Array of int32
    cnts = imutils.grab_contours((cnts, hierarchy))
    
    # print(cnts, key=cv2.contourArea)
    filtered_cnts = filter_contours(cnts, img_width, centering=True, filtering='w')
    
# =============================================================================
#     for i in range(0, len(filtered_cnts)):
#         cnt = filtered_cnts[i]
#         (x, y, w, h) = cv2.boundingRect(cnt)
#         crop = cvImage[y:y+h, x:x+w]
#         cv2.imshow("img_"+str(i), crop)
# =============================================================================
    
    cnt = filtered_cnts[TABLE_NUMBER]
    (x, y, w, h) = cv2.boundingRect(cnt)
    table_img = cvImage[y:y+h, x:x+w]
    
    table_img_h, table_img_w = table_img.shape[:2]
    
    
    thresh_table = apply_thresh(table_img)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    erode_table = cv2.erode(thresh_table, kernel, iterations=1)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (table_img_w//41, table_img_h))
    dilate_table = cv2.dilate(erode_table, kernel, iterations=1)

    
    cv2.imshow("table", table_img)
    cv2.imshow("dilate table", dilate_table)
    cnts, hierarchy = cv2.findContours(dilate_table.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # returns tuple with Array of int32
    cnts = imutils.grab_contours((cnts, hierarchy))
    
    # cv2.drawContours(table_img, cnts, -1, (0,255,200), 3)
    # print(cnts, key=cv2.contourArea)
    filtered_cnts = filter_contours(cnts, table_img_w, centering=None, filtering=None)
    # table_titels = ["Artikel", "Menge", "Preis", "Aktion", "Total"]
    print(table_img.shape[:2])
    cols_of_table = []
    for i in range(0, len(filtered_cnts)):
        cnt = filtered_cnts[i]
        (x, y, w, h) = cv2.boundingRect(cnt)
        crop = table_img[:, x:x+w]
        
        print(crop.shape[:2])
        cv2.imshow("img_"+str(i), crop)
        
        cols_of_table.append(crop)


# =============================================================================
#     for i in range(0, len(filtered_cnts)):
#         cnt = filtered_cnts[i]
#         x, y, w, h = cv2.boundingRect()
#         table = cvImage[y:y + h, x:x + w]
#         cv2.imshow(str(i), table)
#     
# =============================================================================
    return dilate
    
def get_median_sizes(contours):
    heights = []
    widths = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        heights.append(h)
        widths.append(w)
    if not heights or not widths:
        return None
    median_h = int(np.median(heights))
    median_w = int(np.median(heights))
    return  (median_h, median_w)

# =============================================================================
# TESTING
# =============================================================================
def main():
    images_list = ["image.tif", "CoopRechnung2.jpg", "03052024_Migros_Jannis.jpg",
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
    # itex = ItenExtraction()
    
    dilate = get_tableofitems(image)
    
    
    image = grs.cvApplyRescaling(image, 0.2)
    dilate = grs.cvApplyRescaling(dilate, 0.2)
    
    cv2.imshow("image", image)
    cv2.imshow("dilate", dilate)
    cv2.waitKey()
    return 0

if __name__ == "__main__":
    main()
    
    
    


































# =============================================================================
# class ItenExtraction():
# # =============================================================================
# #     def __init__(self, no_table_contour=5):
# #         self.no_table_contour = int(no_table_contour)
# #         
# #         
# #         return None
# # =============================================================================
#     
#     def filter_contours(self, contours, image_width, **kwargs):
#         # flags 
#         centering = False
#         filtering = ""
#         
#         filtering_types = ['h','w','b'] #h:height, w:width, b:both
#         
#         # extract kwargs 
#         for key, value in kwargs.items():
#             if key == 'centering' : 
#                 if value == True :
#                     centering = True
#             if key == 'filtering' :
#                 if value in filtering_types:
#                     filtering = value
#         # functions
#         def check_middle(distance_from_middle):
#             nonlocal max_distance_from_middle
#             return (distance_from_middle <= max_distance_from_middle)
#         
#         def check_height(h):
#             nonlocal median_h
#             return (h >= median_h)
#         
#         def check_width(w):
#             nonlocal median_w
#             return (w >= median_w)
#        
#         # Calculate the middle of the image
#         middle_x = image_width // 2
# 
#         # Threshold distance from the middle
#         max_distance_from_middle = image_width // 4  # Adjust this value as needed
#         
#         
#         median_h, median_w = self.get_median_sizes(contours)
#         
#         filtered_contours = []
# 
#         for contour in contours:
#             # Find the bounding rectangle for the contour
#             x, y, w, h = cv2.boundingRect(contour)
#             
# # =============================================================================
# #             if centering == True:
# # =============================================================================
#             # Calculate the center of the bounding rectangle
#             contour_center_x = x + (w // 2)
# 
#             # Calculate the distance of the contour's center from the middle
#             distance_from_middle = abs(contour_center_x - middle_x)
#             
# 
#             # Check if the contour is within the threshold distance from the middle
#             if distance_from_middle <= max_distance_from_middle:
#                 if (h >= median_h) and (w >= median_w):
#                     filtered_contours.append(contour) 
#         filtered_contours.reverse()
#         return filtered_contours
#     
# def apply_thresh(self, image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 
#     # initialize a rectangular kernel that is ~5x wider than it is tall,
#     # then smooth the image using a 3x3 Gaussian blur and then apply a
#     # blackhat morpholigical operator to find dark regions on a light background
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (51, 11))
#     gray = cv2.GaussianBlur(gray, (3, 3), 0)
#     blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
#     # cv2.imshow("blackhat", blackhat)
#     
#     # compute the Scharr gradient of the blackhat image and scale the result into the range [0, 255]
#     grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
#     grad = np.absolute(grad)
#     (minVal, maxVal) = (np.min(grad), np.max(grad))
#     grad = (grad - minVal) / (maxVal - minVal)
#     grad = (grad * 255).astype("uint8")
# 
#     # apply a closing operation using the rectangular kernel to close gaps in between characters, 
#     #apply Otsu's thresholding method, and finally a dilation operation to enlarge foreground regions
#     grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, kernel)
#     thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#     return thresh
# 
# 
#     def get_tableofitems(self, cvImage):
#         img_height, img_width = cvImage.shape[:2]
#         morph_rect_width  = int(img_width/2)
#         morph_rect_height = int(2)
#         
#         kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morph_rect_width, morph_rect_height))
#         thresh = apply_thresh(cvImage)
#         dilate = cv2.dilate(thresh, kernel, iterations=1) 
#         
#         cv2.imshow("dilate", dilate)
#         
#         
#         return None
#     
#     def get_median_sizes(self, contours):
#         heights = []
#         widths = []
#         for cnt in contours:
#             x, y, w, h = cv2.boundingRect(cnt)
#             heights.append(h)
#             widths.append(w)
#         if not heights or not widths:
#             return None
#         median_h = int(np.median(heights))
#         median_w = int(np.median(heights))
#         return  (median_h, median_w)
# 
# =============================================================================