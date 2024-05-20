"""
@data:      demo_FileHandling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 05.04.2024 - Jannis Mathiuet
@desc: 
    Demo on how to use file_handling.py
    
"""
from src.file_handling import FileHandling
import cv2

relativeInputPath = "in"
relativeOutputPath = "out"
fih = FileHandling(relativeInputPath, relativeOutputPath, True) # True is for Debug
AbsPathParent = fih.getDirParent()

test = ["config", "tessdata"]
# test_path = fih.editDir(AbsPathParent, test)

res = FileHandling().openAllFiles()
i = 0
for img in res:
    cv2.imshow(str(i), img)
    i += 1