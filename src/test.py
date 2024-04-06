import cv2

def main():
    # Öffnen Sie die Webcam
    cap = cv2.VideoCapture(0)  # 0 steht normalerweise für die erste Webcam im System

    if not cap.isOpened():
        print("Fehler: Webcam konnte nicht geöffnet werden.")
        return

    while True:
        # Erfassen Sie ein Frame von der Webcam
        ret, frame = cap.read()

        if not ret:
            print("Fehler: Konnte Frame nicht erfassen.")
            break

        # Anzeigen des Kamerabildes
        cv2.imshow("Webcam", frame)

        # Beenden des Programms mit der ESC-Taste
        if cv2.waitKey(1) == 27:  # ASCII-Code für die ESC-Taste
            break

    # Freigeben der Ressourcen
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()