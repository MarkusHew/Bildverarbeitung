"""
@data:      main.py
@author:    Markus Hewel
@versions:  ver 0.0.0 - 01.04.2024 
            ver 0.0.1 - 25.04.2024 (Riaan Kaempfer; Minor changes for OS-dependant EnvVar-path-assignment)
            ver 0.0.2 - 03.05.2024 (Riaan Kaempfer; Error-catching, incase OCR doesn't recognise all relevant characters)
            ver 1.0.0 - 20.05.2024 
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
from src.ItemExtraction import ItemExtraction
from src.graphics_service import GraphicsService
from src.file_handling import FileHandling

grs = GraphicsService()
itex = ItemExtraction()
# =============================================================================
# USER PARAMETERS
# =============================================================================
fih=FileHandling("in","out") # select relative in- and output paths

mode = 1
# Mode 1: Webcam
webcam_num = 1
# Mode 2: use saved image in input-folder
searchterm = "120524_Coop_Haag_Chur" # when empty, opens all files 
# =============================================================================


def main():
    global mode
    global webcam_num
    global searchterm
    img = None
    
    if mode == 0: # external webcam: take photos and sticks receipt together
        images=Bild_aufnehmen(webcam_num)     
        img = Zusammenfugen(fih.getDirInput(),images)   
        
    if mode == 1: # folder: open a saved image from there
        if len(searchterm) == 0: # don't use serachterm and open all images in selected folder
            searchterm = None
        results = fih.openSearchedFiles(searchterm)
        img, path = results[0]
    img_table, img_cols = itex.get_tableofitems(img, 3)
    grs.deskew(img_table)
    for i in range(0, len(img_cols)):
        img = img_cols[i]
        gray = grs.cvToGrayScale(img)
        gray = grs.cvApplyRescaling(gray, 2)
        thresh = grs.cvToBlackWhite(gray, 1)
        # gray = grs.cvApplyGaussianBlur(gray, 3)
        # _, thresh_MAN = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
        kernel = np.ones(11)
        thresh_MAN = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        # thresh = grs.cvApplyThickerFont(thresh, 7)
        # thresh = grs.cvApplyThinnerFont(thresh, 1)
        cv2.imshow("thresh_"+str(i), thresh)
        cv2.imshow("TEST"+str(i), thresh_MAN)
        # tx.Texterkennung_Spalten(thresh)
        img_boxes, text, tab = tx.textbox(thresh_MAN, 3)    #1: Rechteck, 2:Text, 3:Index, 4: Alles
        print("erkannter Text: ",text)
        print(tab.to_string())
        # print(tab.to_string())
        # tx.Texterkennung_Spalten(thresh_MAN)
        print(f"\n\n\n")
        i+=1
    return 0
# =============================================================================
# Markus Code
# =============================================================================
    binary = grs.cvToBlackWhite(img, 1)
    #binary=grs.cvToGrayScale(img)
    #borders= grs.cvRemoveBorders(rotate)
    print(binary.shape)
    cv2.imwrite("in/binary.tif", binary)
    rescaled = grs.cvApplyRescaling(img, 0.3)
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.title("zusammengefuegtes Bild")
    plt.show()
    
    ################################################################
    
    # #Methode die mit Textboxen arbeitet
    img_boxes,text,tab=tx.textbox(img,4)    #1: Rechteck, 2:Text, 3:Index, 4: Alles
    
    # cv2.imshow("Bild pytasseract",binary)
    # cv2.waitKey(0)
    img_boxes,text,tab=tx.textbox(binary,4)    #1: Rechteck, 2:Text, 3:Index, 4: Alles
    print("erkannter Text: ",text)
    print(tab.to_string())
    print(tab.to_string())
    #print(tab.to_string())

    #text=pytesseract.image_to_string(img, config="--psm 6")

    # Call funct. to extract shop_name from logo:
    logo_path = fih.getDirLogos()
    found, shop_name = tx.logo(img, logo_path)
    if found:
        print("Rechnung von: ", shop_name)    
    else:
        print("keine Ubereinstimmung")

    # ##########################################
    
    nurText = [tupel[0] for tupel in text]
    print("nur Text: ", nurText)
    
    cs.run_data_to_csv(shop_name, nurText, table_col_text, fih.getDirOutput())
    
    # ###########################################    
    # Ausgabe"
    print("Erkannter Text:", text[7])
    #print(result)
    # # print("Abstände zwischen den Wörtern:", word_distances)
    # # for w,d in zip(words,word_distances):
    # #     print(w,d,"\n")
    cv2.imshow('Detected Text', img_boxes)
    cv2.waitKey(0)

    
            
            
        
    
    return 0

if __name__ == "__main__":
    main()

