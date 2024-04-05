"""
@data:      image_handling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 04.04.2024 - Jannis Mathiuet
@desc: 
    Image handling functions like denoising or skewing
    
"""
# libraries
import cv2
# own functions
from graphics_service import GraphicsService 
# =============================================================================
# from dataset_service import DatasetService as das
# from deskrew_service import DeskewService as des
# import path_handling as ph
# import webcam as webcam
# 
# =============================================================================
# =============================================================================
# class ImageHandling : 
#     def chooseMode(self, mode: float, imagePath: str):
#         if mode == 0: 
#             grs.openImageCv(self, imagePath)
#         if mode == 1:
#             print("Webcam")
# =============================================================================
            
def main() :
    img = GraphicsService.openImageCv("../in/OCRtest/page_01.jpg")
    thresh = GraphicsService.cvToBlackWhite(img)
    
    cv2.imshow("orginal", img)
    cv2.imshow("thresh", thresh)
    cv2.waitKey(0)
    
    
    return 0

if __name__ == "__main__" :
    main()