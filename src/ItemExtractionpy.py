# -*- coding: utf-8 -*-
"""
Created on Sun May 12 21:00:16 2024

@author: janni
"""
import cv2
import numpy as np

class ItenExtraction():
    def __init__(self, no_table_contour=5):
        self.no_table_contour = int(no_table_contour)
        
        
        return None
    
    def filter_contours(self, contours, image_width):
        # Calculate the middle of the image
        middle_x = image_width // 2

        # Threshold distance from the middle
        max_distance_from_middle = image_width // 4  # Adjust this value as needed
        
        median_h, median_w = self.get_median_sizes(contours)
        
        filtered_contours = []

        for contour in contours:
            # Find the bounding rectangle for the contour
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate the center of the bounding rectangle
            contour_center_x = x + (w // 2)

            # Calculate the distance of the contour's center from the middle
            distance_from_middle = abs(contour_center_x - middle_x)

            # Check if the contour is within the threshold distance from the middle
            if distance_from_middle <= max_distance_from_middle:
                if (h >= median_h) and (w >= median_w):
                    filtered_contours.append(contour) 
        filtered_contours.reverse()
        return filtered_contours
    
    def get_tableofitems(self):
        
        return None
    
    def get_median_sizes(self, contours):
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