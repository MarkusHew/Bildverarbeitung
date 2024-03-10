import os
import cv2
import platform
from PIL import Image
import pytesseract
from webcam import Bild_aufnehmen

# Setze die Umgebungsvariable TESSDATA_PREFIX
os.environ["TESSDATA_PREFIX"] = r"C:\msys64\mingw64\share\tessdata\configs" #hier sind die Sprachdateien

n=2
save_path=r"C:\Users\marku\Documents\StudiumMobileRobotics\6.Semester\Bildverarbeitung1\Github\Bildverarbeitung"

if(n==1): #Bild mit Webcam aufnehmen
    # Pfad in welchem das Bild gespeichert wird
    img=Bild_aufnehmen(save_path)

if(n==2): #Bild aus Verzeichnis lesen
    try:
        # Öffne das Bild mit Pillow
        pfad="C:/Users/marku/Documents/StudiumMobileRobotics/6.Semester/Bildverarbeitung1/Github/Bildverarbeitung/Bild.tif"
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
for item in text:
    result.append(item)
# Ausgabe"
print(result)
############################################

#### Detecting Characters  ######
#############################################
# pytesseract.pytesseract.tesseract_cmd = r"C:/msys64/mingw64/bin/tesseract.exe"
# pytesseract    

# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #in RGB Bild umwandeln

# hImg, wImg,_ = img.shape
# boxes = pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     print(b)
#     b = b.split(' ')
#     print(b)
#     x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
#     cv2.rectangle(img, (x,hImg- y), (w,hImg- h), (50, 50, 255), 2)
#     cv2.putText(img,b[0],(x,hImg- y+25),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)

######################################################
