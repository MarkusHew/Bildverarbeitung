"""
@data:      main.py
@author:    Markus Hewel
@versions:  ver 0.0.0 - 01.04.2024
@desc: 
    Bild aus Verzeichnis oder von Webcam oeffenen
    Bild in Graubild wandeln und mit opencv optimieren
    optimiertes Bild mit tesseract in Text uebersetzten
    csv File oeffnen und Text in template uebertragen 
"""

import os
import cv2
import platform
from PIL import Image
import pytesseract
from src.webcam import Bild_aufnehmen
from src.writetocsv import write_receipts_to_csv
from src.path_handling import getAbsDir, editDir


# Setze die Umgebungsvariable TESSDATA_PREFIX
os.environ["TESSDATA_PREFIX"] = r"C:\msys64\mingw64\share\tessdata\configs" #hier sind die Sprachdateien

n=2
save_path=r"C:\Users\marku\Documents\StudiumMobileRobotics\6.Semester\Bildverarbeitung1\Github\Bildverarbeitung\out"

if(n==1): #Bild mit Webcam aufnehmen
    # Pfad in welchem das Bild gespeichert wird
    img=Bild_aufnehmen(save_path)

if(n==2): #Bild aus Verzeichnis lesen
    try:
        # Öffne das Bild mit Pillow
        pfad="C:/Users/marku/Documents/StudiumMobileRobotics/6.Semester/Bildverarbeitung1/Github/Bildverarbeitung/Rechnung_Coop.png"
        img = cv2.imread(pfad)

    except Exception as e:
        print(f"Fehler beim Öffnen des Bildes: {e}")
###############################################
        
#Vorbereitung für tesseract        
# Foto in Grauskala wandeln, damit Tesseract besser erkennen kann (Kontrast)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

# Bild abspeichern
file_path = os.path.join(save_path, "gray_image.tif")
cv2.imwrite(file_path, img)

# weitere "Vereinfachungen" für Tesseract
blur=cv2.GaussianBlur(img,(7,7),0)
threshold_image = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
file_path = os.path.join(save_path, "blur_image.tif")
cv2.imwrite(file_path, threshold_image)


################################################
# weitere "Vereinfachungen" für Tesseract
#threshold_image = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#Tesseract OCR anwenden in der Sprache Deutsch
#text = pytesseract.image_to_string(img) #Text erkennen

#text = pytesseract.image_to_string(img, lang="deu")    #Umlaute erkennen

my_conf='outputbase digits'   #einzelen Ziffern erkennen
text = pytesseract.image_to_string(img, config=my_conf)
text=text.split("\n")
result=[]   
for zeile in text:  #einzelne Zeilen in Liste result speichern
    result.append(zeile)

###########################################
#schreiben in csv file
path = getAbsDir(remove=1)
path = editDir(path, "out",)
print("csv file: ",path)
write_receipts_to_csv(path, result)

###########################################    
# Ausgabe"
print(result)
############################################


