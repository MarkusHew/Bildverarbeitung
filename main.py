"""
@data:      main.py
@author:    Markus Hewel
@versions:  ver 0.0.0 - 01.04.2024
@desc: 
    Bild aus Verzeichnis oder von Webcam oeffenen
    Bild in Graubild wandeln und mit opencv optimieren
    optimiertes Bild mit tesseract in Text uebersetzten
    Erkannten Text in Bild schreiben mit Textboxen und Index 
    Text Elemente in Liste umwandeln
    csv File oeffnen und Text in template uebertragen 
"""

import os
import cv2
import platform
from PIL import Image
import pytesseract
from src.webcam import Bild_aufnehmen
import src.Texterkennung as tx
from src.writetocsv import write_receipts_to_csv
from src.graphics_service import GraphicsService
from src.file_handling import FileHandling 


# Setze die Umgebungsvariable TESSDATA_PREFIX
os.environ["TESSDATA_PREFIX"] = r"C:\msys64\mingw64\share\tessdata\configs" #hier sind die Sprachdateien


n=2
save_path=r"C:\Users\marku\Documents\StudiumMobileRobotics\6.Semester\Bildverarbeitung1\Github\Bildverarbeitung\out"

if(n==1): #Bild mit Webcam aufnehmen
    # Pfad in welchem das Bild gespeichert wird
    img=Bild_aufnehmen(save_path)

if(n==2): #Bild aus Verzeichnis lesen
    try:
        # Öffne das Bild mit opencv
        pfad="C:/Users/marku/Documents/StudiumMobileRobotics/6.Semester/Bildverarbeitung1/Github/Bildverarbeitung/in/Rechnung_Volg.jpg"
        img = cv2.imread(pfad)
        

    except Exception as e:
        print(f"Fehler beim Öffnen des Bildes: {e}")
###############################################

# # Bild im TIFF-Format speichern
# cv2.imwrite('img.tif', img)        
# #Vorbereitung für tesseract        
# # Foto in Grauskala wandeln, damit Tesseract besser erkennen kann (Kontrast)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# # Bild abspeichern
# file_path = os.path.join(save_path, "gray_image.tif")
# cv2.imwrite(file_path, img)
# cv2.imshow('Graubild',img)

# # weitere "Vereinfachungen" für Tesseract
# blur=cv2.GaussianBlur(img,(7,7),0)
# threshold_image = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
# file_path = os.path.join(save_path, "blur_image.tif")
# cv2.imwrite(file_path, threshold_image)

# ################################################


#Programm Jannis
#fih = FileHandling("in", "out")
grs = GraphicsService()
#result = fih.openAllFiles() # function returns img and it's path
# print(len(result))
#img, imgpath = result[3]
binary = grs.cvToBlackWhite(img, 3) 
#cv2.imwrite("binary.jpg", binary)
cv2.imshow("binary", binary)
cv2.waitKey(0)
# print(img)
# rescaled = grs.cvApplyRescaling(img, 10)
# grs.displayImage(img)
# grs.displayImage(imgpath)
################################################################


#text = pytesseract.image_to_string(img, lang="deu")    #Umlaute erkennen

my_conf='outputbase digits'   #einzelen Ziffern erkennen
text = pytesseract.image_to_string(binary, config=my_conf)
text=text.split("\n")
result=[]   
for zeile in text:  #einzelne Zeilen in Liste result speichern
    result.append(zeile)
word_distances = [len(t) for t in text]  # Längen der Wörter als Abstände betrachten
# ##########################################
# #Logo in Bild finden und Shopname zurückgeben
# # shop_name=tx.logo(threshold_image)
# # print(shop_name)
# #######################################
# #Methode die mit Textboxen arbeitet
# #img_boxes=tx.textbox(threshold_image)
# #cv2.imshow('Detected Text', img_boxes)
# ##########################################
# # schreiben in csv file
# # path = ph.getAbsDir(remove=1)
# # path = ph.editDir(path, "out",)
# # print("csv file: ",path)
# # write_receipts_to_csv(path, result)

# ###########################################    
# # Ausgabe"
# #print("Erkannter Text:", text)
# print(result)
# # print("Abstände zwischen den Wörtern:", word_distances)
# # for w,d in zip(words,word_distances):
# #     print(w,d,"\n")
# cv2.waitKey(0)


