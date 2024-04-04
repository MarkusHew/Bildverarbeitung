"""
@data:      image_handling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 04.04.2024 - Jannis Mathiuet
@desc: 
    Image handling functions like denoising or skewing
    
"""
# libraries

# own functions
from src.graphics_service import GraphicsService as grs
from src.data_service import DataService as das
from src.deskrew_service import DeskewService as des
import src.path_handling as ph
import src.webcam as webcam

class ImageHandling : 
    def chooseMode(self, mode: float, imagePath: str):
        if mode == 0: 
            grs.openImageCv(self, imagePath)
        if mode == 1:
            webcam.Bild_aufnehmen(imagePath)
            
def main() :
    print("hi")
    
    return 0

if __name__ == "__main__" :
    main()