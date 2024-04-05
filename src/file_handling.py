"""
@data:      file_handling.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 31.03.2024 - Jannis Mathiuet
            ver 1.0.0 - 05.04.2024 - Jannis Mathiuet
@desc: 
    file to handle paths and files
    If there are any questions, please contact me.
"""
import os
from PIL import Image as imageMain
from PIL.Image import Image
import cv2
import pdf2image
import tempfile
import numpy as np

# =============================================================================
# PUBLIC FUNCTIONS
# =============================================================================
class FileHandling(): 
    # =========================================================================
    # Path Functions (PUBLIC)
    # =========================================================================
    def __init__(self, inRelPath: str="in", outRelPath: str="out", debug: bool=False): 
        global DIR_PARENT, DIR_INPUT, DIR_OUTPUT, CLASS_DEBUG
        
        DIR_PARENT = self._setDirParent()
        DIR_INPUT = self._setDirInput(inRelPath)
        DIR_OUTPUT = self._setDirOutput(outRelPath)
        CLASS_DEBUG = debug
        
        if CLASS_DEBUG is True:
            print(DIR_PARENT)
            print(DIR_INPUT)
            print(DIR_OUTPUT)
            print(CLASS_DEBUG)
        
        return None
    
    def getDirParent(self):
        global DIR_PARENT
        return DIR_PARENT
    
    def getDirInput(self):
        global DIR_INPUT
        return DIR_INPUT
    
    def getDirOutput(self):
        global DIR_OUTPUT
        return DIR_OUTPUT
    

    def getAbsDir(self):
        path = os.getcwd()
        # path = self._removePathEndings(path, remove)
        return path


    def editDir(self, path, *folders, remove: np.uint=0) :
        newpath = self._removePathEndings(path, remove)
        
        folderpath = ""
        for folder in folders :
            banned = ["", " "]
            if folder != banned: 
                folderpath = os.path.join(folderpath, folder)
        newpath = os.path.join(path, folderpath)
        if (os.path.exists(newpath)) is False: 
            print(f"\nThis path does not exist! Try another one. \n{newpath = }\n")
            return ""
        return newpath

    # -------------------------------------------------------------------------
    # Path Functions (PRIVATE)
    # -------------------------------------------------------------------------
    DIR_PARENT = ""
    DIR_INPUT = ""
    DIR_OUTPUT = ""
    CLASS_DEBUG = False
    
    def _setDirParent(self):
        return self.getAbsDir()

    def _setDirInput(self, relpath: str):
        path = self.getDirParent()
        newpath = self.editDir(path, relpath)
        return newpath

    def _setDirOutput(self, relpath: str):
        path = self.getDirParent()
        newpath = self.editDir(path, relpath)
        return newpath
    # =========================================================================
    # Files Functions (PUBLIC)
    # =========================================================================
    # all Functions are inspired from Leo Ertuna
    # source: https://github.com/JPLeoRX/opencv-text-deskew/blob/master/python-service/services/graphics_service.py
    def openAllFiles(self):
        path = self.getDirInput()
        result = []
        for root, dirs, files in os.walk(path):
            for f in files: 
                filePath = self.editDir(path, str(f))
                item = self.openOneFile(filePath)
                result.append(item)
        
        return result
    
    def openOneFile(self, path: str=""):
        if ".pdf" in path:
            print("PDF detected")
            return
        imageCv = self._openImageCv(path)
        return imageCv


    # -------------------------------------------------------------------------
    # Files Functions (PRIVATE)
    # -------------------------------------------------------------------------
    # all Functions are from Leo Ertuna
    # source: https://github.com/JPLeoRX/opencv-text-deskew/blob/master/python-service/services/graphics_service.py
    def _openImagePil(self, imagePath: str) -> Image:
        return imageMain.open(imagePath)

    def _convertPilImageToCvImage(self, pilImage: Image):
        return cv2.cvtColor(np.array(pilImage), cv2.COLOR_RGB2BGR)

    def _convertCvImagetToPilImage(self, cvImage) -> Image:
        return imageMain.fromarray(cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB))

    def _openImageCv(self, imagePath: str):
        return self._convertPilImageToCvImage(self._openImagePil(imagePath))
    
    # Render one page of a PDF document to image
    def _renderPdfDocumentPageToImageFromPath(self, pdfDocPath: str, pageNumber: int, dpi: int) -> str:
        tempFolder = tempfile.gettempdir()
        pageImagePaths = pdf2image.convert_from_path(pdfDocPath, dpi=dpi, output_folder=tempFolder, fmt='png', paths_only=True, thread_count=1, first_page=pageNumber, last_page=pageNumber)
        return pageImagePaths[0]
    
    def _removePathEndings(self, path, cntremove: np.uint=1):
        if cntremove is None:
            return path
        try: 
            cntremove = int(cntremove)
        except RuntimeError as error: 
            print(error)
            print("cntremove must be an integer")
    
        if cntremove < 0 :
            raise Exception(f"The number should be higher than 0. ({cntremove=})")
    
        for i in range(cntremove): 
            path, element = os.path.split(path)
            # path = os.path.join(path, os.pardir)
        newpath = path
    
        return newpath

# =============================================================================
#     def chooseFile(self, path: str, **kwargs) :
#         # kwargs list
#         ftype = kwargs.get('ftype', None) # file type
#         fname = kwargs.get('fname', None) # file name
#         # depth = kwargs.get('depth', 0)
#         dircs = kwargs.get('dircs', [""]) 
#     
#         # select path
#         newpath = path
#         for dirc in dircs :    
#             newpath = os.path.join(newpath, dirc)
#             if (os.path.exists(newpath)) is False: 
#                 print(f"\nThis path does not exist! Try another one. \n{newpath = }\n")
#     
#     
#         d_limiter = 0
#         for (root, dirs, files) in os.walk(path):
#             if ftype is None : 
#                 print(f"Directory ({len(dirs)}): {dirs} ")
#                 print(f"Files     ({len(files)}): {files} ")
#                 
#             if ftype and fname is type(str): 
#                 for file in files:
#                     if (ftype.endswith(file)):
#                         if (fname in file):
#                             print(file)            
#             if d_limiter == 0: 
#                 break
#             d_limiter += 1
#             # for f in file:
#             #     f.conta
#             #     for ftype in f:
#             #         for fname in f:
#             #         if fname is None: 
#             #             print(f)
#             #         if k_ele is element: 
#             #             filepath = os.path.join(newpath, f)
#             #             return filepath
#             #         k_ele += 1
#         return path
# =============================================================================
