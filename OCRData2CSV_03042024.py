import csv

def write_receipt_to_csv(file_name, receipt):
    # Make and open new csv file
    with open(file_name, mode='w', newline='') as csvfile:
        # Set the column names to a list:
        datacolumns = receipt[0].keys()  # Get column names from the first item's keys
        
        writer = csv.DictWriter(csvfile, fieldnames=datacolumns)
        
        writer.writeheader()  # Write the header row with column names
        for row in receipt:  # Iterate through the list
            writer.writerow(row)  # Write each dictionary as a row


# Eg. OCR-text:
ocr_text = """
Date: 15.03.22
Fir mich und dich.

Solothurn Rosengarten

Artikel tenge Preis Aktion [otal

Frae Fron Risottoltil 1 5.95 5.950
tnai Gaffe Latte 1 1.95 1,950
Nini Babybel 1 5.10 5.100
Gractiv Chips Natu 1 2.35 2.35 0
BAR 20.00
Zuriick CHF “4.05

GOOF SENOSSENSCIAFT, GHE-LN6.311. 185 MYST
GR AWS TOA HST
0 2.50 5.8 0.37

£5 FEDIENIE SIE Frau Denuth

Viele Sak fir Lire Eka
IAAL

QL VLAT V5el5 0709) 00384371 001 0001101
"""

# Make up and search for key-patterns to assign their values to their appropriate variables (eg. UID_var, Date_var, items_var, Price_var, etc.)

# UID_Pattern:

Price_Pattern:
	#.## or ##.##
	
# assign price and item-amount to two appropriate vectors (because these vars occure multiple times on one single receipt), sothat the vect-elements can then just be iterated through in the dictionary below.


# date pattern (COOP):
	##.##.## (# = a digit 0,...,9)
date_pattern = r'\b[0-9]{2}\.[0-9]{2}\.[0-9]{2}\b'
# or 	date_pattern = r'\b\d{2}\.\d{2}\.\d{2}\b'

# Search for dates using the pattern
dates_found = re.findall(date_pattern, ocr_text)




# Create List of receipts
Receipt = [
    {"Item": "baked", "sufix": "beans", "Price [CHF]": "25.95"},
    {"prefix": "milked", "sufix": "cow", "Price [CHF]": "20.00"},
    {"prefix": "wonderful", "sufix": "girl", "Price [CHF]": "2.65"},
    {"prefix": None, "sufix": "tree", "Price [CHF]": 3.80}
]

# Get OCR output for shop's name and receipt date
shop_name = "ShopNamefromOCR"
receipt_date = "ReceiptDatefromOCR"
UID = 

# Construct file name based on OCR output
file_name = f"{shop_name}_{receipt_date}_ReceiptData.csv"

# Call the function to write the receipt to CSV file
write_receipt_to_csv(file_name, Receipt)
