'''
@data:      Texterkennung.py
@author:    Markus Hewel
@versions:  ver 0.0.0 - 09.04.2024, 25.04.2024(minor changes for OS-dependant EnvVars, Riaan Kaempfer)
@desc: 
    Funktionen: - Bild skalieren auf beliebige Breite
                - Ein Logo auf einer Rechnung als Bildausschnitt erfassen und abspeichern
                - Ein Geschaftslogo auf einer Rechnung erkennen
                - Text auf Rechnung erkennen und grafisch ausgeben sowie als Liste zurückgeben
'''

import os
import cv2
import platform
import numpy as np
from PIL import Image
import pytesseract
import pandas as pd
import pprint

# # Überprüfen der aktuellen Optionen
# print(pd.get_option('display.max_rows'))  # Maximale Anzahl von Zeilen
# print(pd.get_option('display.max_columns'))  # Maximale Anzahl von Spalten

# Setzen der Optionen auf den Standardwert
pd.set_option('display.max_rows', None)  # Keine Begrenzung für die Anzahl von Zeilen
pd.set_option('display.max_columns', None)  # Keine Begrenzung für die Anzahl von Spalten


def Bild_skalieren_und_Farbe(img, width):
    height=(int(img.shape[0]*(width/img.shape[1]))) #Bild skalieren auf 1000*xxxx
    img_resize=cv2.resize(img,(width,height))
    print("skalierte Grösse",img_resize.shape)
    if len(img.shape) > 2: #Farbkanäle des Eingangsbildes überprüfen und Ausgabebild in Farbe erstellen
        return img_resize 
    else:
        return cv2.cvtColor(img_resize, cv2.COLOR_GRAY2BGR)

def Bildlogo_erstellen(img):    #Methode kann aus einem Bild das Logo extrahieren und abspeichern
    # Verzeichnis zum Speichern der ausgewählten Bildausschnitte
    current_directory = os.getcwd()    
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    if not os.path.exists(parent_directory):
        print("Das Verzeichnis existiert nicht:", parent_directory)
    elif not os.access(parent_directory, os.W_OK):
        print("Sie haben keine Schreibberechtigungen für das Verzeichnis:", parent_directory)
    Speicherpfad=os.path.join(parent_directory,"in", "template.png")
    print("Speicherpfad: ", Speicherpfad)

    color_img=Bild_skalieren_und_Farbe(img, 400)
    # cv2.imshow('test', color_img)
    # cv2.waitKey(0)

    # Initialisierung der Parameter
    params = {'start_point': None, 'end_point': None, 'selected': False}
    def Auswahl(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            param['start_point'] = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            param['end_point'] = (x, y)
            param['selected'] = True

    # Erstellen eines leeren Bildfensters und Verknüpfen der Callback-Funktion
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', Auswahl, params)
    
    while True:
        clone = color_img.copy()
        
        # Zeichnen des Rechtecks
        if params['start_point'] is not None and params['end_point'] is not None:
            x1, y1 = params['start_point']
            x2, y2 = params['end_point']
            cv2.rectangle(clone, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Anzeigen des Bildes
        cv2.imshow('image', clone)

        # Warten auf die Taste 'Enter' zum Beenden
        key = cv2.waitKey(1)
        if key == 13:  # Enter-Taste
            break
    # Schließen des Bildfensters
    cv2.destroyAllWindows()
    
    # Speichern des ausgewählten Bildausschnitts
    if params['selected']:
        x1, y1 = params['start_point']
        x2, y2 = params['end_point']
        selected_region = color_img[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
        cv2.imwrite(Speicherpfad, selected_region)

    return clone


def textbox(img, Darstellung):   #Methode die mit Textboxen arbeitet und erkannten Text als Liste zurückgibt
    color_image=Bild_skalieren_und_Farbe(img, 1000)
    data = pytesseract.image_to_data(color_image, lang="deu", config='--psm 6', output_type=pytesseract.Output.DICT)    #Bild in Text
    tab = pytesseract.image_to_data(color_image, lang="deu", config='--psm 6', output_type='data.frame')
    tab = tab[tab.conf != -1]
    tab.head()
    tab.groupby(['block_num','par_num','line_num'])['text'].apply(list)

    detected_text=[]
    # Durch die erkannten Textblöcke iterieren und Rechtecke um sie zeichnen
    for i in range(len(data['text'])):
        # Text und Positionsinformationen extrahieren
        text = data['text'][i]
        detected_text.append(text)
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        # Rechteck um den erkannten Text zeichnen
        if Darstellung==1 or Darstellung==4:
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Text auf das Bild einfügen
        if Darstellung==2 or Darstellung==4:
            cv2.putText(color_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Index einfügen
        if Darstellung==3 or Darstellung==4:
            index=str(i)
            cv2.putText(color_image, index, (x-10, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0, 0), 2)

    # Bild übergeben
    img_boxes = Bild_skalieren_und_Farbe(color_image, 400)

    return img_boxes, detected_text, tab


def boundingBox(img, Speicherpfad):
    color_image=Bild_skalieren_und_Farbe(img, 1000)
    gray_img = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray_img,(7,7), 0)
    cv2.imwrite(Speicherpfad+"/in/index_blur.png", blur)
    thresh=cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    cv2.imwrite(Speicherpfad+"/in/index_thresh.png", thresh)
    kernal=cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))
    dilate=cv2.dilate(thresh,kernal, iterations=1)

    cnts=cv2.findContours(dilate,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts=cnts[0] if len(cnts)==2 else cnts[1]
    cnts=sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
    for c in cnts:
        x,y,w,h=cv2.boundingRect(c)
        #if h>50 and w>100:
        roi=color_image[y:y+h, x:x+h]
        cv2.rectangle(color_image,(x,y), (x+w,y+h), (36,255,12),2)
        #ocr_result=pytesseract.image_to_string(roi)
    #print(ocr_result)   
    return color_image


#def logo(img, pfad):  #Methode die Logo in Bild erkennt und Shopnamen zuruckgibt    
#    print("Aktuelles Verzeichnis:", pfad)
#    shop_names={"Coop":"Logo_Coop.png","Volg":"Logo_Volg.png"}
#    found_shop=None
#    for key,value in shop_names.items():
#        color_image=Bild_skalieren_und_Farbe(img, 400)
#        template = cv2.imread(pfad+ '\\in\\'+value)
#        w, h = template.shape[0], template.shape[1]
#        res = cv2.matchTemplate(color_image, template, cv2.TM_CCOEFF_NORMED)
#        threshold = .8
#        loc = np.where(res >= threshold)
#        if loc[0].size > 0:  # Wenn ein Ubereinstimmung gefunden wurde
#            found_shop = key
#            # Markieren des gefundenen Bereichs im Bild
#            for pt in zip(*loc[::-1]):
#                cv2.rectangle(color_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
#            
#            cv2.imshow('Ausschnitt in bild gefunden', color_image)
#            cv2.imshow('template', template)
#            cv2.waitKey(0)
#            return True, found_shop     
#          
#    return False, None

def logo(img, pfad):  # OS-sensitive Methode die Logo in Bild erkennt und Shopnamen zuruckgibt 
    print("Aktuelles Verzeichnis:", pfad)
    shop_names = {"Coop": "Logo_Coop.png", "Volg": "Logo_Volg.png"}
    found_shop = None
    
    # Determine the path separator based on the current operating system
    # (sep-assigning, only for illustrative purposes. ;-) )
    if os.name == "posix":  # Linux or MacOS
        sep = '/'
    elif os.name == "nt":  # Windows
        sep = '\\'
    else:
        sep = '/'
        print("Unknown operating system. Assuming Linux path separator '/'.")

    for key, value in shop_names.items():
        color_image = Bild_skalieren_und_Farbe(img, 400)
        template_path = os.path.join(pfad, 'in', value) # Pfaderweiterung per os.path.join() automatisch 
                                                        # entspr. des erkannten Betriebssystems (OS)
        template = cv2.imread(template_path)
        
        w, h = template.shape[0], template.shape[1]
        res = cv2.matchTemplate(color_image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        
        if loc[0].size > 0:  # If a match is found
            found_shop = key
            
            # Highlight the found area in the image
            for pt in zip(*loc[::-1]):
                cv2.rectangle(color_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            
            cv2.imshow('Ausschnitt in bild gefunden', color_image)
            cv2.imshow('template', template)
            cv2.waitKey(0)
            
            return True, found_shop
    
    return False, None



# =============================================================================
# TESTING
# =============================================================================
def main():    
    
    # Setze die Umgebungsvariable TESSDATA_PREFIX
    os.environ["TESSDATA_PREFIX"] = r"C:\msys64\mingw64\share\tessdata\configs" #hier sind die Sprachdateien
    #os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata" # Fuer Linux Ubuntu
    
    n=2 # 1:Shoplogo abspeichern, 2:Logo erkennen, 3: Text erkennen und ausgeben
    try: #Bild öffnen aus ubergeordnetem Verzeichnis        
        current_directory = os.getcwd()
        print("Aktuelles Verzeichnis:", current_directory)
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
        Verzeichnis=os.path.join(parent_directory,"in", "Rechnung_Coop.png")
        img = cv2.imread(Verzeichnis)
        print(img.shape)  

    except Exception as e:
        print(f"Fehler beim Öffnen des Bildes: {e}")


    if n==1:
        Bildlogo_erstellen(img)
    if n==2:
        found ,shop_name =logo(img, parent_directory)
        if found:
            print("Rechnung von: ",shop_name)
        else:
            print("keine Ubereinstimmung")
    if n==3:
        img_boxes,text,tab=textbox(img,2)    #1: Rechteck, 2:Text, 3:Index, 4: Alles
        print("erkannter Text: ",text)
        print(tab.to_string())
        #pprint.pprint(tab)    

        
        cv2.imshow('Detected Text', img_boxes)
        cv2.waitKey(0)

    if n==4:
        image= boundingBox(img,current_directory)
        cv2.imshow('bounding boxes', image)
        cv2.waitKey(0)

if __name__ == "__main__" :
    main()
