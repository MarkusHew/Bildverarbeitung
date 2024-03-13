#webcam.py

import numpy as np
import cv2
import platform
import os


def Bild_aufnehmen(save_path=None):    # change here, to open your preferred webcam
    DEVICE_ID=0 
    
    if platform.system() == 'Windows':
        videoBackend = cv2.CAP_DSHOW
    else:
        videoBackend = cv2.CAP_ANY
    cap = cv2.VideoCapture(DEVICE_ID, videoBackend);
    
    if not cap.isOpened():
        print('ERROR: could not open webcam');
    
    # Überprüfe und drucke die maximale Auflösung der Kamera default 640x480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    max_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    max_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Maximale Auflösung der Kamera: {max_width} x {max_height}")


    while(True):
        ret, frame = cap.read();
        if not ret:
            print('ERROR: could not read data from webcam')
            break;
        
        cv2.imshow("Press 'q' to quit.", frame)
        ch = cv2.waitKey(20);
        if ch==ord('q'):
            break;
        elif ch==ord('s'):
            image=frame.copy()
            # Bild abspeichern
            file_path = os.path.join(save_path, "image.tif")
            cv2.imwrite(file_path, image)
            cv2.imshow("image",image)
        if ch==ord('0'):
            cap.set(cv2.CAP_PROP_SETTINGS,0);

    cap.release();
    cv2.destroyAllWindows();
    return image