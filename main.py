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
import os
import cv2
import platform
from PIL import Image
import pytesseract
from src.webcam import Bild_aufnehmen, Zusammenfugen
import src.Texterkennung as tx
from src.writetocsv import write_receipts_to_csv
from src.graphics_service import GraphicsService
from src.file_handling import FileHandling
import src.DatatoCSV as cs
import matplotlib.pyplot as plt


fih=FileHandling("in","out")
verz= os.getcwd()

n=1

if(n==1): #Bild mit Webcam aufnehmen
    # Pfad in welchem das Bild gespeichert wird
    images=Bild_aufnehmen(1)     
    img=Zusammenfugen(fih.getDirInput(),images)   

if(n==2): #Bild aus Verzeichnis lesen
    try:
        # Öffne das Bild mit opencv        
        result=fih.openSearchedFiles("stiched_image.tif")#CoopReceipt_scan_2024-04-12_11-24-29.jpg        
        img,pfad = result[0];
    except Exception as e:
        print(f"Fehler beim Öffnen des Bildes: {e}")

###############################################


grs = GraphicsService()
# binary = grs.cvToBlackWhite(img, 1)
# #binary=grs.cvToGrayScale(img)
# #borders= grs.cvRemoveBorders(rotate)
# print(binary.shape)
# cv2.imwrite("binary.tif", binary)
rescaled = grs.cvApplyRescaling(img, 0.3)
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.title("zusammengefuegtes Bild")
plt.show()

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
img_boxes,text,tab=tx.textbox(img,4)    #1: Rechteck, 2:Text, 3:Index, 4: Alles

print("erkannter Text: ",text)
print(tab.to_string())


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

# Import package for current date and time (Timecode):
from datetime import datetime
now = datetime.now()
date_string = now.strftime("%d%m%Y_%H;%M;%S")
  
# Print the table
#print(table)

# Generate combined line sublists
combined_line_sublists = cs.generate_line_sublists(text)

if combined_line_sublists is not None:
    # Print the combined line sublists
    for i, combined_line_sublist in enumerate(combined_line_sublists, start=1):
        print(f"combined_line_sublist_{i}: {combined_line_sublist}")
else:
    print(f"Error: Unable to generate combined line sublists in main.py, 'combined_line_sublists'. 'NoneType' object is not iterable, i.e. \n probably the product-detail-list could not be generated previously, \n probably due to OCR-issue with the provided receipt-pic...")


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
print("Erkannter Text:", text[7])
#print(result)
# # print("Abstände zwischen den Wörtern:", word_distances)
# # for w,d in zip(words,word_distances):
# #     print(w,d,"\n")
cv2.imshow('Detected Text', img_boxes)
cv2.waitKey(0)
