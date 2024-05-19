"""
@data:      main.py
@author:    Markus Hewel
@versions:  ver 0.0.0 - 01.04.2024 
            ver 0.0.1 - 25.04.2024 (Riaan Kaempfer; Minor changes for OS-dependant EnvVar-path-assignment)
            ver 0.0.2 - 03.05.2024 (Riaan Kaempfer; Error-catching, incase OCR doesn't recognise all relevant characters)
@desc: 
    Bild aus Verzeichnis oder von Webcam oeffenen
    Bild in Graubild wandeln und mit opencv optimieren
    optimiertes Bild mit tesseract in Text uebersetzten
    Erkannten Text in Bild schreiben mit Textboxen und Index 
    Text Elemente in Liste umwandeln
    csv File oeffnen und Text in template uebertragen 

weiteres Vorgehen:
Bild einlesen, Bild binär umwandeln, Bild automatisch ausrichten,
Bild an pytasseract übergeben und in Text umwandeln
Text als Liste übergeben und in csv-file abspeichern

"""
# libraries
import os
import cv2
import platform
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import numpy as np

# own functions
from src.webcam import Bild_aufnehmen, Zusammenfugen
import src.Texterkennung as tx
from src.writetocsv import write_receipts_to_csv
import src.DatatoCSV as cs


# classes and inits
from src.graphics_service import GraphicsService
from src.file_handling import FileHandling
from src.ItemExtraction import ItemExtraction
fih=FileHandling("in","out")
grs = GraphicsService()
itex = ItemExtraction()

def main():
    mode = 1
    img = None
    if mode == 0: # external webcam: take photos and sticks receipt together
        webcam_num = 1
        images=Bild_aufnehmen(webcam_num)     
        img = Zusammenfugen(fih.getDirInput(),images)   
        
    if mode == 1: # folder: open a saved image from there
        searchterm = ""
        if len(searchterm) == 0: # don't use serachterm and open all images in selected folder
            searchterm = None
        results = fih.openSearchedFiles(searchterm)
        img, path = results[0]
    img_table, img_cols = itex.get_tableofitems(img, 3)
    i=0
    for img in img_cols:
        gray = grs.cvToGrayScale(img)
        gray = grs.cvApplyRescaling(gray, 5)
        thresh = grs.cvToBlackWhite(gray, 1)
        # gray = grs.cvApplyGaussianBlur(gray, 3)
        _, thresh_MAN = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
        kernel = np.ones(51)
        thresh_MAN = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        # thresh = grs.cvApplyThickerFont(thresh, 7)
        # thresh = grs.cvApplyThinnerFont(thresh, 1)
        cv2.imshow("thresh_"+str(i), thresh)
        cv2.imshow("TEST"+str(i), thresh_MAN)
        tx.Texterkennung_Spalten(thresh)
        tx.Texterkennung_Spalten(thresh_MAN)
# =============================================================================
#         result = tx.textbox(thresh, 2)
#         print(f"HALLO\n\n\n\n\n\n")
#         print(result)
#         result = tx.textbox(thresh_MAN, 2)
#         print(f"\n\n\n\n\n\n")
#         print(result)
# =============================================================================
        break
        i+=1
    
            
            
        
    
    return 0

if __name__ == "__main__":
    main()

