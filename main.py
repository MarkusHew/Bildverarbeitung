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
#result = fih.openAllFiles() # function returns img and it's path
# print(len(result))
#img, imgpath = result[3]
#img=cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
#rotate,_=grs.deskew(img) 
binary = grs.cvToBlackWhite(img, 1)
#binary=grs.cvToGrayScale(img)
#borders= grs.cvRemoveBorders(rotate)
print(binary.shape)
cv2.imwrite("binary.tif", binary)
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


# Call funct. to extract shop_name from logo:
found ,shop_name =tx.logo(img, verz)
if found:
    print("Rechnung von: ",shop_name)    
else:
    print("keine Ubereinstimmung")

# ##########################################

# # Call funct. to extract receipt-date out of string-list:
# receipt_date = cs.extract_receipt_date(text)

# # Call the shop_address funct.:
# shopAddress = cs.extract_shop_address(text)
# print(f'This is the shop address: {shopAddress}\n')

# # Call the extract_total_price function:
# total_price = cs.extract_total_price(text)
# # Check if the total price is extracted successfully:
# if total_price is not None:
#     print(f'Total price of shopping list items: {total_price} CHF \n')
# else:
#     print('Total price not found in the OCR string list. \n')



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
print("Erkannter Text:", text[7])
#print(result)
# # print("Abstände zwischen den Wörtern:", word_distances)
# # for w,d in zip(words,word_distances):
# #     print(w,d,"\n")
cv2.imshow('Detected Text', img_boxes)
cv2.waitKey(0)
