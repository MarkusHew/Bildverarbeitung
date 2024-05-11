# =============================================================================
# source of most code: 
# 
# =============================================================================
# import the necessary packages
from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot as plt
from pytesseract import Output
from tabulate import tabulate
import pandas as pd
import numpy as np
import pytesseract
import argparse
import imutils
import cv2
import os


def plt_imshow(title, image):
    # convert the image frame BGR to RGB color space and display it
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.title(title)
    plt.grid(False)
    plt.show()
    return None

def resize_imshow(cvImage, scale_percent):
    width  = int(cvImage.shape[1] * scale_percent/100)
    height = int(cvImage.shape[0] * scale_percent/100)
    dim = (width, height)
    resize = cv2.resize(cvImage, dim, cv2.INTER_AREA)
    name = str(np.random.seed(42))
    print(name)
    cv2.imshow(name, resize)
    return None

def apply_thresh(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # initialize a rectangular kernel that is ~5x wider than it is tall,
    # then smooth the image using a 3x3 Gaussian blur and then apply a
    # blackhat morpholigical operator to find dark regions on a light background
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (51, 11))
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)

    # compute the Scharr gradient of the blackhat image and scale the result into the range [0, 255]
    grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype("uint8")

    # apply a closing operation using the rectangular kernel to close gaps in between characters, 
    #apply Otsu's thresholding method, and finally a dilation operation to enlarge foreground regions
    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh

def get_median_sizes(contours):
    heights = []
    widths = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        heights.append(h)
        widths.append(w)
    if not heights or not widths:
        return None
    median_h = int(np.median(heights))
    median_w = int(np.median(heights))
    return  (median_h, median_w)

def filter_contours(contours, image_width):
    # Calculate the middle of the image
    middle_x = image_width // 2

    # Threshold distance from the middle
    max_distance_from_middle = image_width // 4  # Adjust this value as needed
    
    median_h, median_w = get_median_sizes(contours)
    
    filtered_contours = []

    for contour in contours:
        # Find the bounding rectangle for the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Calculate the center of the bounding rectangle
        contour_center_x = x + (w // 2)

        # Calculate the distance of the contour's center from the middle
        distance_from_middle = abs(contour_center_x - middle_x)

        # Check if the contour is within the threshold distance from the middle
        if distance_from_middle <= max_distance_from_middle:
            if (h >= median_h) and (w >= median_w):
                filtered_contours.append(contour) 
    filtered_contours.reverse()
    return filtered_contours
    
# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image to be OCR'd")
# ap.add_argument("-o", "--output", required=True,
# 	help="path to output CSV file")
# ap.add_argument("-c", "--min-conf", type=int, default=0,
# 	help="minimum confidence value to filter weak text detection")
# ap.add_argument("-d", "--dist-thresh", type=float, default=25.0,
# 	help="distance threshold cutoff for clustering")
# ap.add_argument("-s", "--min-size", type=int, default=2,
# 	help="minimum cluster size (i.e., # of entries in column)")
# args = vars(ap.parse_args())

# since we are using Jupyter Notebooks we can replace our argument
# parsing code with *hard coded* arguments and values # michael_jordan_stats.png # atevH.jpg
images_list = ["image.tif", "CoopRechnung2.jpg", "03052024_Migros_Jannis.jpg"]
args = {
	"image": images_list[0],
	"output": "results.csv",
	"min_conf": 0,
	"dist_thresh": 25.0,
	"min_size": 2,
}
NUMB_CNT = 5 # Migros: (4, 5) Coop: 
# set a seed for our random number generator
np.random.seed(42)

# load the input image and convert it to grayscale
current_directory = os.getcwd()
print("Aktuelles Verzeichnis:", current_directory)
Verzeichnis=os.path.join(current_directory,"in", args["image"])
image = cv2.imread(Verzeichnis)

thresh = apply_thresh(image)


print(thresh.shape)
thresh_height, thresh_width = thresh.shape[:2]
morph_rect_width  = int(thresh_width/2)# * 300/2600)
morph_rect_height = int(2)#thresh_height * 20/1950)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morph_rect_width, morph_rect_height))
thresh = cv2.dilate(thresh, kernel, iterations=1) 

# resize_imshow(thresh, 30)


# find contours in the thresholded image and grab the largest one,
# which we will assume is the stats table
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# print(cnts, key=cv2.contourArea)
filtered_cnts = filter_contours(cnts, thresh_width)
print(len(filtered_cnts))
tableCnt = filtered_cnts[NUMB_CNT]
# tableCnt = max(cnts, key=cv2.contourArea)

# =============================================================================
# =============================================================================
# # 
# =============================================================================
# =============================================================================

# compute the bounding box coordinates of the stats table and extract
# the table from the input image
(x, y, w, h) = cv2.boundingRect(tableCnt)
table = image[y:y + h, x:x + w]

table_thresh = apply_thresh(table)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, table_thresh.shape[0]))
table_dilate = cv2.dilate(table_thresh, kernel, iterations=1) 

cnts = cv2.findContours(table_dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# cnts = filter_contours(cnts, table_dilate.shape[1])

# resize_imshow(table_dilate, 50)
for cnt in cnts:
    print(cv2.boundingRect(cnt))
    x,y,w,h = cv2.boundingRect(cnt)
    table = table[y:y+h, x:x+w]
    name = str(np.random.rand())
    print(name)
    cv2.imshow(name, table)
    # resize_imshow(table, 30)

# show the original input image and extracted table to our screen
plt_imshow("Input", image)
plt_imshow("Table", table)


# Set the PSM mode to detect sparse text, and then localize text in the table
options = "--psm 6"
results = pytesseract.image_to_data(cv2.cvtColor(table, cv2.COLOR_BGR2RGB),
									config=options,
									output_type=Output.DICT)

# Initialize a list to store the (x, y)-coordinates of the detected text along with the OCR'd text itself
coords = []
ocrText = []

# loop over each of the individual text localizations
for i in range(0, len(results["text"])):
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]

	# extract the OCR text itself along with the confidence of the
	# text localization
	text = results["text"][i]
	conf = int(float(results["conf"][i]))

	# filter out weak confidence text localizations
	if conf > args["min_conf"]:
		# update our text bounding box coordinates and OCR'd text,
		# respectively
		coords.append((x, y, w, h))
		ocrText.append(text)
		
# Extract all x-coordinates from the text bounding boxes, setting the y-coordinate value to zero
xCoords = [(c[0], 0) for c in coords]

# Apply hierarchical agglomerative clustering to the coordinates
clustering = AgglomerativeClustering(
	n_clusters=None,
	#affinity="l1",	#manhattan",
	linkage="complete",
	distance_threshold=args["dist_thresh"])
clustering.fit(xCoords)

# Initialize our list of sorted clusters
sortedClusters = []

# loop over all clusters
for l in np.unique(clustering.labels_):
	# extract the indexes for the coordinates belonging to the
	# current cluster
	idxs = np.where(clustering.labels_ == l)[0]

	# verify that the cluster is sufficiently large
	if len(idxs) > args["min_size"]:
		# compute the average x-coordinate value of the cluster and
		# update our clusters list with the current label and the
		# average x-coordinate
		avg = np.average([coords[i][0] for i in idxs])
		sortedClusters.append((l, avg))

# sort the clusters by their average x-coordinate and initialize our
# data frame
sortedClusters.sort(key=lambda x: x[1])
df = pd.DataFrame()

# loop over the clusters again, this time in sorted order
for (l, _) in sortedClusters:
	# extract the indexes for the coordinates belonging to the
	# current cluster
	idxs = np.where(clustering.labels_ == l)[0]

	# extract the y-coordinates from the elements in the current
	# cluster, then sort them from top-to-bottom
	yCoords = [coords[i][1] for i in idxs]
	sortedIdxs = idxs[np.argsort(yCoords)]

	# generate a random color for the cluster
	color = np.random.randint(0, 255, size=(3,), dtype="int")
	color = [int(c) for c in color]

	# loop over the sorted indexes
	for i in sortedIdxs:
		# extract the text bounding box coordinates and draw the
		# bounding box surrounding the current element
		(x, y, w, h) = coords[i]
		cv2.rectangle(table, (x, y), (x + w, y + h), color, 2)

	# extract the OCR'd text for the current column, then construct
	# a data frame for the data where the first entry in our column
	# serves as the header
	cols = [ocrText[i].strip() for i in sortedIdxs]
	currentDF = pd.DataFrame({cols[0]: cols[1:]})

	# concatenate *original* data frame with the *current* data
	# frame (we do this to handle columns that may have a varying
	# number of rows)
	df = pd.concat([df, currentDF], axis=1)

# replace NaN values with an empty string and then show a nicely
# formatted version of our multi-column OCR'd text
df.fillna("", inplace=True)
print(tabulate(df, headers="keys", tablefmt="psql"))



