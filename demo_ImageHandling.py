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
from src.graphics_service import GraphicsService
from src.file_handling import FileHandling
# from src.deskew_service import DeskewService

            
def main() :   
    fih = FileHandling("in", "out")
    grs = GraphicsService()
    
    result = fih.openAllFiles() # function returns img and it's path
    print(len(result))
    img, imgpath = result[0]
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    # print(img)
    # rescaled = grs.cvApplyRescaling(img, 0.5)
    img = grs.cvToBlackWhite(img, 10)
    # img = grs.deskew(img)
    # img = grs.cvApplyThickerFont(img, 2)
    img = grs.cvRemoveBorders(img)
    # grs.displayImage(img)
    # grs.displayImage(imgpath)
    
    
# =============================================================================
#     # path = "F:/.DEV/_Programming/_GitHub/Bildverarbeitung/in/OCRtest/page_01.jpg"
#     # path = "in/OCRtest/index_3.jpg"
#     path = "in/OCRtest/page_01_rotated.jpg"
#     # img = cv2.imread(path)
#     img = grs.openImageCv(path)
#     
#     # grs.getSkewAngle(img, debug=True)
#     new = img
#     new, angle = grs.deskew(new)
#     cv2.imshow("0", img)
#     # new = grs.cvToBlackWhite(img)
#     cv2.imshow("1", new)
#     # new = grs.cvApplyThickerFont(new, 3)
#     # cv2.imshow("2", new)
#     # new = grs.cvApplyThinnerFont(new, 3)
#     # cv2.imshow("3 ", new)
#     # cv2.imshow("orginal", img)
#     # cv2.imshow("new", new)
#     cv2.waitKey(0)
# =============================================================================
    
    
    return 0

if __name__ == "__main__" :
    main()
    
    

# =============================================================================
# from src.dataset_service import DataService as das
# from src.deskrew_service import DeskewService as des
# import src.path_handling as ph
# import src.webcam as webcam
# =============================================================================

# =============================================================================
# class ImageHandling : 
#     def chooseMode(self, mode: float, imagePath: str):
#         if mode == 0: 
#             grs.openImageCv(self, imagePath)
#         if mode == 1:
#             print("Webcam")
# =============================================================================