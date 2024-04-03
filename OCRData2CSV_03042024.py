import csv
#import Real Expressions package to define and search string-patterns:
import re




# Function to extract the shop names from the OCR text:
def extract_shop_names(ocr_text):
    # Regular expression pattern to match one of the specified substrings
    pattern = r'\b(Denner|Coop|Migros)\b'
    
    # Search for the substrings in the OCR text
    matches = re.findall(pattern, ocr_text)
    
    # If more than one match is found, display a warning message
    if len(matches) > 1:
        print("Warning: Multiple shop names found!")
    
    # Return all matches found (if any)
    return matches

# Function to extract the date from the OCR text:
def extract_receipt_date(ocr_text):
	# date pattern (COOP):
	##.##.## (# = a digit 0,...,9)
	date_pattern = r'\b[0-9]{2}\.[0-9]{2}\.[0-9]{2}\b'
	# or 	date_pattern = r'\b\d{2}\.\d{2}\.\d{2}\b'
	
	# Search for dates using the pattern
	dates_found = re.findall(date_pattern, ocr_text)
	
	# Return the found date:
	return dates_found




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


# Time-code:
from datetime import datetime
print("Current date:",datetime.utcnow())
date= datetime.utcnow() - datetime(1970, 1, 1)
print("Number of days since epoch:",date)
seconds =(date.total_seconds())
milliseconds = round(seconds*1000)
print("Milliseconds since epoch:",milliseconds)




# Create List of receipts
Receipt = [
    {"Item": "baked", "sufix": "beans", "Price [CHF]": "25.95"},
    {"prefix": "milked", "sufix": "cow", "Price [CHF]": "20.00"},
    {"prefix": "wonderful", "sufix": "girl", "Price [CHF]": "2.65"},
    {"prefix": None, "sufix": "tree", "Price [CHF]": 3.80}
]

#%% Get OCR output for shop's name and receipt date
# Extract the shop name(s) from the OCR text:
shop_names = extract_shop_names(ocr_text) # Incase there are accidentally multiple shop names detected we handle this case appropriately. 

# Print all shop names found:
#print("Shop names extracted:", shop_names)

# In case there are accidentally multiple shop names detected, 
# convert the list of shop names into a single string with underscores:
shop_names_string = '_'.join(shop_names)
#%%



receipt_date = extract_receipt_date(ocr_text)
UID = 

# Construct file name based on OCR output
file_name = f"{receipt_date}_{shop_names_string}_ReceiptData.csv"

# Call the function to write the receipt to CSV file
write_receipt_to_csv(file_name, Receipt)
