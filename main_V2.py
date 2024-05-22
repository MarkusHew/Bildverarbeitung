"""
@data:      main.py
@author:    Markus Hewel
@versions:  ver 0.0.0 - 01.04.2024 
            ver 0.0.1 - 25.04.2024 (Riaan Kaempfer; Minor changes for OS-dependant EnvVar-path-assignment)
            ver 0.0.2 - 03.05.2024 (Riaan Kaempfer; Error-catching, incase OCR doesn't recognise all relevant characters)
            ver 1.0.0 - 20.05.2024 (Jannis Mathiuet final version)
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
import src.webcam as webcam
import src.Texterkennung as tx
import src.DatatoCSV as cs
import src.replaceUnwanted as rpu
# from src.writetocsv import write_receipts_to_csv


# classes and inits
from src.ItemExtraction import ItemExtraction
from src.graphics_service import GraphicsService
from src.file_handling import FileHandling

grs = GraphicsService()
itex = ItemExtraction()
# =============================================================================
# USER PARAMETERS
# =============================================================================
# CSV Seperator
# is either semicolon ';' or comma ',' currently doesnt work
# ==> for new csv: change SEPERATOR in DatatoCSV.py 
# ==> for already generated csv: use replaceUnwanted.py
#              change filename to desired filename run code

fih=FileHandling("in","out") # select relative in- and output paths

mode = 1
 

# webcam parameters for MODE 0
webcam_num = 1
# searchterm for MODE 1 
searchterm = "IMG_0641.jpg" # when empty, opens all files 
# =============================================================================


def main():
    DEBUG = False
    global mode
    global webcam_num
    global searchterm
# =============================================================================
    # diffrent modes
    
    # MODE 0 external webcam: take photos and sticks receipt together
    if mode == 0: 
        images = webcam.Bild_aufnehmen(webcam_num)     
        img = webcam.Zusammenfugen(fih.getDirInput(),images)   
        images = [img]
    
    # MODE 1 folder: open a saved image from there
    if mode == 1: 
        if len(searchterm) == 0: # don't use serachterm and open all images in selected folder
            searchterm = None
        results = fih.openSearchedFiles(searchterm)
        images, paths = results
        
# =============================================================================
    for img in images:
        print("USER VORBEREITUNG")
        img, success = grs.imgPreperationUser(img)
        if not success:
            return -1
        print(f"\n\n")
# =============================================================================
        print("TABELLE")
        # find item table, extract columms and detect text
        table_col_text = ()
        img_table, img_cols = itex.get_tableofitems(img, 3)
        
        print("gefundener Text in Spalten: ")
        for i in range(0, len(img_cols)):
            current_img = img_cols[i]
            thresh = grs.cvToBlackWhite(current_img, 3)
            thicker_font = grs.cvApplyThickerFont(thresh, 3)
            
            # read text from image and create list
            spalte = tx.Texterkennung_Spalten(thicker_font)
            table_col_text += (spalte, )
            
            print(spalte)
            if DEBUG: 
                cv2.imshow("thresh_col"+str(i), thresh)
                cv2.imshow("thicker_Font_col"+str(i), thicker_font)
                print(spalte)
            
        print(f"\n\n")
# =============================================================================
        binary = grs.cvToBlackWhite(img, 3)
        binary = grs.cvApplyThickerFont(binary, 3)
        img_boxes,text,tab=tx.textbox(img, 4)    #1: Rechteck, 2:Text, 3:Index, 4: Alles

        # Call funct. to extract shop_name from logo:
        logo_path = fih.getDirLogos()
        found, shop_name = tx.logo(img, logo_path)
        if found:
            print("Rechnung von: ", shop_name)    
        else:
            print("keine Ubereinstimmung")
        print(f"\n")
        # ##########################################
        
        nurText = [tupel[0] for tupel in text]
        print("nur Text: ")
        print(nurText)
        print(f"\n\n\n")
        cv2.imshow('Detected Text', img_boxes)
        cv2.waitKey(0)
        

# =============================================================================
        print("CSV")        
        # wirte all data to csv file
        csv_path = cs.run_data_to_csv(shop_name, nurText, table_col_text, fih.getDirOutput())
        # if csv_seperator != ';':
        #     rpu.replace_char(csv_path, ';', ',')
    return 0


if __name__ == "__main__":
    main()

