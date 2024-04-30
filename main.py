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

weiteres Vorgehen:
Bild einlesen, Bild binär umwandeln, Bild automatisch ausrichten,
Bild an pytasseract übergeben und in Text umwandeln
Text als Liste übergeben und in csv-file abspeichern

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
import src.DatatoCSV as cs


# Setze die Umgebungsvariable TESSDATA_PREFIX
os.environ["TESSDATA_PREFIX"] = r"C:\msys64\mingw64\share\tessdata\configs" #Pfad muss auf jeweiligen Rechner angepasst werden #hier sind die Sprachdateien
verz= os.getcwd()

n=2

fih=FileHandling("in","out");
# current_directory = os.getcwd() #aktuelles Verzeichnis holen
# #print("Aktuelles Verzeichnis:", current_directory)
# save_path=current_directory+"\in"   #Speicherverzeichnis für Webcambild
# print(save_path)


if(n==1): #Bild mit Webcam aufnehmen
    # Pfad in welchem das Bild gespeichert wird
    #img=Bild_aufnehmen(save_path)
    pass

if(n==2): #Bild aus Verzeichnis lesen
    try:
        # Öffne das Bild mit opencv        
        result=fih.openSearchedFiles("CoopReceipt_scan_2024-04-12_11-24-29.jpg")#CoopReceipt_scan_2024-04-12_11-24-29.jpg        
        #Rechnung_Volg.jpg
        img,pfad = result[0];
        #pfad=current_directory+"/in/CoopRechnung2.jpg"

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
#img=cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
#rotate,_=grs.deskew(img) 
binary = grs.cvToBlackWhite(img, 1)
binary=grs.cvToGrayScale(img)
#borders= grs.cvRemoveBorders(rotate)
print(binary.shape)
cv2.imwrite("binary.tif", binary)
rescaled = grs.cvApplyRescaling(img, 0.3)
# cv2.imshow("Bild binaer und gedreht", rescaled)
# cv2.waitKey(0)
# print(img)
# 
# grs.displayImage(img)
# grs.displayImage(imgpath)
################################################################


#text = pytesseract.image_to_string(img, lang="deu")    #Umlaute erkennen

# my_conf='outputbase digits'   #einzelen Ziffern erkennen
# text = pytesseract.image_to_string(binary, config=my_conf)
# text=text.split("\n")
# result=[]   
# for zeile in text:  #einzelne Zeilen in Liste result speichern
#     result.append(zeile)
# word_distances = [len(t) for t in text]  # Längen der Wörter als Abstände betrachten
# ##########################################
# #Logo in Bild finden und Shopname zurückgeben
# # shop_name=tx.logo(threshold_image)
# # print(shop_name)
# #######################################
# #Methode die mit Textboxen arbeitet
img_boxes,text,tab=tx.textbox(binary,2)    #1: Rechteck, 2:Text, 3:Index, 4: Alles
print("erkannter Text: ",text)
#print(tab.to_string())

found ,shop_name =tx.logo(img, verz)
if found:
    print("Rechnung von: ",shop_name)
else:
    print("keine Ubereinstimmung")
# ##########################################
# # schreiben in csv file
# # path = ph.getAbsDir(remove=1)
# # path = ph.editDir(path, "out",)cd
# # print("csv file: ",path)
# # write_receipts_to_csv(path, result)

Datum=cs.extract_receipt_date(text)
file_name = f"{Datum}_{shop_name}_ReceiptData.csv"
#cs.write_receipts_to_csv(file_name, text)
print("Datum", Datum)

# ###########################################    
# Ausgabe"
#print("Erkannter Text:", text)
#print(result)
# # print("Abstände zwischen den Wörtern:", word_distances)
# # for w,d in zip(words,word_distances):
# #     print(w,d,"\n")
cv2.imshow('Detected Text', img_boxes)
cv2.waitKey(0)
# cv2.waitKey(0)


