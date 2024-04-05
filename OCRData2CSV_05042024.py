# Import csv-package for craeting csv-file:
import csv
# Import package for "regular expressions" to define and search string-patterns:
import re
# Import package for current date and time (Timecode):
from datetime import datetime


# Function def to extract shop name for a single string as OCR-output:
# def extract_shop_names(ocr_output):
    # shopname_pattern = r'\b(Denner|Coop|Migros|Volg)\b'
    # matches = re.findall(shopname_pattern, ocr_output)
    # if len(matches) > 1:
        # print("Warning: Multiple shop names found!")
    # return matches
    
# Function def to extract shop name for a string-list as OCR-output:    
def extract_shop_names(ocr_output):
    shopname_pattern = r'\b(Denner|Coop|Migros|Volg)\b'
    matches = []
    for line in ocr_output:
        matches.extend(re.findall(shopname_pattern, line))
    if len(matches) > 1:
        print("Warning: Multiple shop names found!")
    return matches

    
# Function def to extract receipt date for a string-list as OCR-output within a specified range of list elements (start-/end_index): 
def extract_receipt_date(OCR_strList):
    date_pattern = r'\b(?:\d{2}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4})\b'
    start_index = 28
    end_index = 35
    for i in range(start_index, end_index + 1):
        dates_found = re.findall(date_pattern, OCR_strList[i])
        if dates_found:
            return dates_found[0]  # Return the first date found
    return None  # Return None if no date is found



def write_receipt_to_csv(file_name, receipt):
    with open(file_name, mode='w', newline='') as csvfile:
        datacolumns = receipt[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=datacolumns)
        writer.writeheader()
        for row in receipt:
            writer.writerow(row)

ocr_text = """
Date: 15.03.22
Coop
Fir mich und dich.
Denn

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

OCR_strList = ['AN', 'Volg', '.l?vanchtztwcl ‘', 'frandtich', '', '"\\', 'Menzi Metzg |', 'Hauptstrasse 31', '8756 Mitlodi', '+41 55 644 12 31', '', 'Artikel ~ Betrag M', 'SINALCO 50CL 1.50 B', 'BTG-SHAK. CALIF 200G 4.90 B', 'PENNE AL ARABIA 400G 6.20 B 4', '', "Total OHF 12.60 '§", 'Erhalten:', '', 'Bargeld CHF; 20.00', 'Ruckgeld CHF: : 7.40', 'WISTS  Netto  MAST  Brutto M', '', 'Z2.60 12.28  0.32 12.60 B', '', 'LHL 111 719 981 MWST', '', 's bediente Sie: \\', 'Riedi Y. |', 'Besten Dank fur Ihren Einkauf', 
'', "Bon: 76554 y' 03.04.2024 12:06", 'Kasse: 1074101 ) Shop: 10741', '', '{', '', '7557', '', '[o%)', '', '7655', '', 'T', '']

# Create List of receipts
Receipt = [
    {"Item": "baked", "sufix": "beans", "Price [CHF]": "25.95"},
    {"prefix": "milked", "sufix": "cow", "Price [CHF]": "20.00"},
    {"prefix": "wonderful", "sufix": "girl", "Price [CHF]": "2.65"},
    {"prefix": None, "sufix": "tree", "Price [CHF]": 3.80}
]

receipt_date = extract_receipt_date(OCR_strList)
shop_names = extract_shop_names(OCR_strList)
shop_names_string = '_'.join(shop_names)

#%% Time-code; Current date and time:
# datetime object containing current date and time
# now = datetime.now()
# print("now =", now) # Output:	 now = 2022-12-27 10:09:20.430322

# dd/mm/YY H:M:S
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string) #Output:	 date and time = 27/12/2022 10:09:20

now = datetime.now()
date_string = now.strftime("%d%m%Y_%H;%M;%S")
#%%


file_name = f"{receipt_date}_{shop_names_string}_ReceiptData{date_string}.csv"
write_receipt_to_csv(file_name, Receipt)


