import cv2
import os
from graphics_service import GraphicsService
from file_handling import FileHandling 

# def main():
#     # Öffnen Sie die Webcam
#     cap = cv2.VideoCapture(0)  # 0 steht normalerweise für die erste Webcam im System

#     if not cap.isOpened():
#         print("Fehler: Webcam konnte nicht geöffnet werden.")
#         return

#     while True:
#         # Erfassen Sie ein Frame von der Webcam
#         ret, frame = cap.read()

#         if not ret:
#             print("Fehler: Konnte Frame nicht erfassen.")
#             break

#         # Anzeigen des Kamerabildes
#         cv2.imshow("Webcam", frame)

#         # Beenden des Programms mit der ESC-Taste
#         if cv2.waitKey(1) == 27:  # ASCII-Code für die ESC-Taste
#             break

#     # Freigeben der Ressourcen
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# img = cv2.imread("C:/Users/marku/Documents/StudiumMobileRobotics/6.Semester/Bildverarbeitung1/Github/Bildverarbeitung/img.tif")
# print(img.shape)

# # Aktuelles Verzeichnis
# current_directory = os.getcwd()
# print("Aktuelles Verzeichnis:", current_directory)

# # Eine Ebene nach oben
# parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
# print("Übergeordnetes Verzeichnis:", parent_directory)

#Programm Jannis
fih = FileHandling("in", "out")
grs = GraphicsService()
result = fih.openAllFiles() # function returns img and it's path
# print(len(result))
img, imgpath = result[3]
binary = grs.cvToBlackWhite(img, 3) 
#cv2.imwrite("binary.jpg", binary)
binary=grs.rotateImage(binary,20)
binary,angle=grs.deskew(binary)
# print(img)
cv2.imshow("binary", binary)
#rescaled = grs.cvApplyRescaling(binary, 0.3)
# grs.displayImage(img)
# grs.displayImage(imgpath)
#cv2.imshow("binary", rescaled)
cv2.waitKey(0)