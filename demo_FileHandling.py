"""
@data:      demo_FileHandling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 05.04.2024 - Jannis Mathiuet
@desc: 
    Demo on how to use file_handling.py
    If there are any questions, please contact me.
"""
from src.file_handling import FileHandling
import cv2

relativeInputPath = "in"
relativeOutputPath = "out"
FileHandling(relativeInputPath, relativeOutputPath, True) # True is for Debug
AbsPathParent = FileHandling().getDirParent()

res = FileHandling().openAllFiles()
i = 0
for img in res:
    cv2.imshow(str(i), img)
    i += 1
# =============================================================================
# ODER
# =============================================================================
fh1 = FileHandling(relativeInputPath, relativeOutputPath)
fh2 = FileHandling("anderesInput", "andererOutput")
AbsPathParent = fh1.getDirParent()

res = fh1.openAllFiles()
res2 = fh2.openAllFiles()
i = 0
for img in res:
    cv2.imshow(str(i), img)
    i += 1