"""
@data:      test_OCR_Jannis.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 01.04.2024 - Jannis Mathiuet
@desc: 
    testing ground for OCR
    
"""
# libraries
from PIL import Image
import pytesseract as tes
import cv2 
import os
import matplotlib.pyplot as plt

# own functions
import path_handling as ph
# =============================================================================
# functions
# =============================================================================
# https://stackoverflow.com/questions/28816046/
# displaying-different-images-with-actual-size-in-matplotlib-subplot
def display_image_in_actual_size(im_path) :
    dpi = 80
    im_data = plt.imread(im_path)
    # height, width, depth = im_data.shape
    height, width = im_data.shape
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)
    
    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    
    # Hide spines, ticks, etc.
    ax.axis('off')
    
    # Display the image.
    ax.imshow(im_data, cmap='gray')
    
    plt.show()
    return None


# =============================================================================
# Pillow test
# =============================================================================
if (0):
    abs_path = ph.getAbsDir(remove=1)
    in_path = ph.editDir(abs_path, "in\\test")
    out_path = ph.editDir(abs_path, "out")
    print(os.listdir(in_path))

    img_list = []
    for img in os.listdir(in_path): 
        print(img)
        img_list += [ph.editDir(in_path, img)]


    for img_ele in img_list: 
        img = Image.open(img_ele)
        print(img)
        print(img.size)
        # img.show()
        # img.rotate(180).show()
        # img.save(out_path+"/hallo.jpeg")

# =============================================================================
# tesseract test
# =============================================================================
if (1): 
    #  Image open / display
    abs_path = ph.getAbsDir(remove=1)
    # in_path = ph.editDir(abs_path, "in", "test", "sharpText.jpg")
    in_path = ph.editDir(abs_path, "in", "OCRtest", "page_01.jpg")
    out_path = ph.editDir(abs_path, "out")
    img = cv2.imread(in_path)
    # display_image_in_actual_size(in_path)
    
    # Inverting Images (isn't needed for Tesseract 4.x and newer)
    if (0) : 
        inverted_image = cv2.bitwise_not(img)
        out_imgpath = out_path+"/page_01_inverted.jpg"
        cv2.imwrite(out_imgpath, inverted_image)
        # display_image_in_actual_size(out_path+"/page_01_inverted.jpg")
    
    # Rescaling
    
    
    # Binarisation
    if (1):
        def grayscale(image):
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = grayscale(img)
        out_imgpath = out_path+"/page_01_gray.jpg"
        cv2.imwrite(out_imgpath, gray_image)
        # display_image_in_actual_size(out_imgpath)
        
        thresh, im_bw = cv2.threshold(gray_image, 200, 230, cv2.THRESH_BINARY)
        out_imgpath = out_path+"/page_01_blackwhite.jpg"
        cv2.imwrite(out_imgpath, im_bw)
        # display_image_in_actual_size(out_imgpath)
        # cv2.imshow("", gray_image)
        
    
    # Noise Reduction
    if (1):
        def noise_removal(image):
            import numpy as np
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.dilate(image, kernel, iterations=1)
            
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.erode(image, kernel, iterations=1)
            
            #reduces Noise
            image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            image = cv2.medianBlur(image, 3) 
            
            # direkte Fuktion von opencv (ausprobieren) 
            # Quelle: https://docs.opencv.org/3.4/d1/d79/group__photo__denoise.html#ga4c6b0031f56ea3f98f768881279ffe93
            # cv2.fastNlMeansDenoising(im_bw, noNoise_image, 11)
            
            return image
        no_noise = noise_removal(im_bw)
        out_imgpath = out_path+"/page_01_no-noise.jpg"
        
        cv2.imwrite(out_imgpath, no_noise)
        display_image_in_actual_size(out_imgpath)

    
    
    # Dilation and Erosion
    def thinner_font(image) : 
        import numpy as np
        # funktioniert besser wenn Bild zuerst invertiert, wenn nicht ist hier Dilation
        image = cv2.bitwise_not(image)
        kernel = np.ones((2, 2), np.uint8) # groesserer Kernel --> groesserer Filter
        image = cv2.erode(image, kernel, iterations=1) # iterations: Durchlaeufe
        image = cv2.bitwise_not(image)
        
        return image

    def thicker_font(image) : 
        import numpy as np
        # funktioniert besser wenn Bild zuerst invertiert, wenn nicht ist hier Erosion
        image = cv2.bitwise_not(image)
        kernel = np.ones((2, 2), np.uint8) # groesserer Kernel --> groesserer Filter
        image = cv2.dilate(image, kernel, iterations=1) # iterations: Durchlaeufe
        image = cv2.bitwise_not(image)
        # zurueck invertieren
        
        return image
    
    # Rotation and Deskewing
    # OCR braucht vertikal orientierter Text
    if (1):
        in_path = ph.editDir(abs_path, "in", "OCRtest", "page_01_rotated.jpg")
        # RECHERECHE! Borders muessen zuerst weg
        # https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
        
    # Removing Borders
    
    
    # Missing Borders
    
    
    # output
    
    
    # out_path = ph.editDir(abs_path, "out")
    # img = Image.open(in_path+"sharpText.jpg")
    # image_file.show()
    # img = cv2.imread(in_path)