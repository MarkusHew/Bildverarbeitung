"""
@data:      main.py
@author:    Markus Hewel
@versions:  ver 0.0.1 - 01.04.2024, 25.04.2024(minor changes for OS-dependant EnvVar-path-assignment, Riaan Kaempfer)
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


# Setze die Umgebungsvariable TESSDATA_PREFIX Betriebssystemabhängig
# (Pfad wo die Tesseract-Sprachdateien abgelegt sind!)
if os.name == "posix":  # Linux or MacOS
    # Fuer Linux Ubuntu:
    #os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata" # Pfad wo die Tesseract-Sprachdateien abgelegt sind!
    os.environ["TESSDATA_PREFIX"] = "/home/riaanlinub/Desktop/Riaan_LinuxUbuntu/FHGR/3_FS24/Bildverarb1/PyVEnv_ImageProcessing/bin"
    print("Fuer Linux gesetzter Pfad der Umgebungsvariable 'TESSDATA_PREFIX':", os.environ["TESSDATA_PREFIX"])
elif os.name == "nt":  # Windows
    os.environ["TESSDATA_PREFIX"] = r"C:\msys64\mingw64\share\tessdata\configs" #Pfad muss auf jeweiligen Rechner angepasst werden #hier sind die Sprachdateien
    print("Fuer Windows gesetzter Pfad der Umgebungsvariable 'TESSDATA_PREFIX':", os.environ["TESSDATA_PREFIX"])
else:
    os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata"
    print("Unknown operating system. Assuming Linux system.")
    print("Gesetzter Pfad der Umgebungsvariable 'TESSDATA_PREFIX':", os.environ["TESSDATA_PREFIX"])


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
        result=fih.openSearchedFiles("CoopReceipt_scan_2024-04-12_11-24-29.png")#CoopReceipt_scan_2024-04-12_11-24-29.jpg        
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
img_boxes,text,tab=tx.textbox(binary,4)    #1: Rechteck, 2:Text, 3:Index, 4: Alles
print("erkannter Text: ",text)
#print(tab.to_string())


# Call funct. to extract shop_name from logo:
found ,shop_name =tx.logo(img, verz)
if found:
    print("Rechnung von: ",shop_name)    
else:
    print("keine Ubereinstimmung")

# ##########################################
# Programm von Riaan Kaempfer
# # schreiben in csv file
# # path = ph.getAbsDir(remove=1)
# # path = ph.editDir(path, "out",)cd
# # print("csv file: ",path)
# # write_receipts_to_csv(path, result)

# Call funct. to extract receipt-date out of string-list:
receipt_date = cs.extract_receipt_date(text)

# Call the shop_address funct.:
shopAddress = cs.extract_shop_address(text)
print(f'This is the shop address: {shopAddress}\n')

# Call the extract_total_price function:
total_price = cs.extract_total_price(text)
# Check if the total price is extracted successfully:
if total_price is not None:
    print(f'Total price of shopping list items: {total_price} CHF \n')
else:
    print('Total price not found in the OCR string list. \n')



# Call the extract_UID function:
shop_UID = cs.extract_UID(text)
    
# Time-code; Current date and time:
# datetime object containing current date and time
# now = datetime.now()
# print("now =", now) # Output:	 now = 2022-12-27 10:09:20.430322
# dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string) #Output:	 date and time = 27/12/2022 10:09:20
# Import package for current date and time (Timecode):
from datetime import datetime
now = datetime.now()
date_string = now.strftime("%d%m%Y_%H;%M;%S")
#
    

# Create a dictionary-/key-value-list of the receipt-extractions:
# Receipt = [
# {"items": "baked beans", "amount": "1", "price [CHF]": 23.50, "total price [CHF]": ""},
# {"items": "milked cow", "amount": "1", "price [CHF]": "20.00", "total price [CHF]": ""},
# {"items": "wonderful girl", "amount": "3", "price [CHF]": "2.65", "total price [CHF]": ""},
# {"items": "tree", "amount": None, "price [CHF]": 3.80, "total price [CHF]": ""}, 
# {"items": "", "amount": "", "price [CHF]": "", "total price [CHF]": total_price}
# ]

# Convert the Receipt list to a table format for prompting as a table within the terminal using tabulate
#table = cs.tabulate(Receipt, headers="keys", tablefmt="fancy_grid")

# Print the table
#print(table)

# Generate combined line sublists
combined_line_sublists = cs.generate_line_sublists(text)

# Print the combined line sublists
for i, combined_line_sublist in enumerate(combined_line_sublists, start=1):
    print(f"combined_line_sublist_{i}: {combined_line_sublist}")



# Call primitive CSV-file-writing funct.:
#file_name = f"{Datum}_{shop_name}_ReceiptData.csv"
#cs.write_receipts_to_csv(file_name, text)
#print("Datum", Datum)

# Construct the file path for the CSV-file and call CSV-file-writing funct.:
file_name = f"{receipt_date}_{shop_name}_ReceiptData{date_string}.csv"
folder_name = 'out'
file_path = os.path.join(folder_name, file_name)
print("Verzeichnis: ", file_path)
cs.write_receipts_to_csv(file_path, combined_line_sublists, total_price, shop_name, shopAddress, shop_UID, receipt_date)


# ###########################################    
# Ausgabe"
#print("Erkannter Text:", text)
#print(result)
# # print("Abstände zwischen den Wörtern:", word_distances)
# # for w,d in zip(words,word_distances):
# #     print(w,d,"\n")
cv2.imshow('Detected Text', img_boxes)
cv2.waitKey(0)
