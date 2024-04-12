"""
FHGR, Bildverarbeitung 1
Project - Receipt reading and transcription to CSV-file

OCRData2CSV Python-code, written by Riaan Kämpfer:
This code should take in the OCR-generated text-data as a single string or (preferably) already as a string-list
in order to extract relevant data from the receipt by matching patterns and then writing an according csv-file
contaiing the relevant data (eg. shop name, receipt-date, firm identificatin number (UID), Items bought, Prices each, total price, etc.)

"""

# Import csv-package for creating csv-file:
import csv

# Import package for "regular expressions" to define and search string-patterns:
import re

# Import package for current date and time (Timecode):
from datetime import datetime



# Function to convert ocr-text (as a single string) to a list of strings:
def string_to_word_list(input_string):
    # Split the input string into words
    word_list = input_string.split()
    return word_list

# # Example usage
# input_string = "Hello world! This is a sample string."
# output_list = string_to_word_list(input_string)
# print(output_list)

# Function def to extract shop name for a single string as OCR-output:
# def extract_shop_names(ocr_output):
    # shopname_pattern = r'\b(Denner|Coop|Migros|Volg)\b'
    # matches = re.findall(shopname_pattern, ocr_output)
    # if len(matches) > 1:
        # print("Warning: Multiple shop names found!")
    # return matches
    
# # Function def to extract shop name for a string-list as OCR-output:    
# def extract_shop_names(ocr_output):
    # shopname_pattern = r'\b(Denner|Coop|Migros|Volg)\b'
    # matches = []
    # for line in ocr_output:
        # matches.extend(re.findall(shopname_pattern, line))
    # if len(matches) > 1:
        # print("Warning: Multiple shop names found!")
    # return matches
    
    # # Function def to extract shop name for a string-list as OCR-output within a specified range of list elements (start-/end_index):    
# def extract_shop_name_frStrList(ocr_strList):
    # shopname_pattern = r'\b(Denner|Coop|Migros|Volg)\b'
    # matches = []
    # for line in ocr_strList:
        # matches.extend(re.findall(shopname_pattern, line))
    # if len(matches) > 1:
        # print("Warning: Multiple shop names found!")
    # return matches

    
# Function def to extract receipt date for a string-list as OCR-output within a specified range of list elements (start-/end_index): 
# def extract_receipt_date(ocr_strList):
    # StartDateIndex_Coop=70
    # EndDateIndex_Coop=75
    # date_pattern = r'\b(?:\d{2}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4})\b'
    # start_index = StartDateIndex_Coop
    # end_index = EndDateIndex_Coop
    # for i in range(start_index, end_index + 1):
        # dates_found = re.findall(date_pattern, ocr_strList[i])
        # if dates_found:
            # return dates_found[0]  # Return the first date found
    # return None  # Return None if no date is found
    
# Or rather this version, since safer - should work for any Coop receipt (no matter how long it is)!:
def extract_receipt_date(ocr_strList):
    date_pattern = r'\b(?:\d{2}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4})\b'  # Date pattern (DD.MM.YY or DD.MM.YYYY)
    #!!! maybe also to replace by a range instead of a single index num, for reliability!!:
    index_to_check_Coop = -6  # Index of the 6th-last element in the list 
    
    # Check the 6th-last element for the date pattern match
    dates_found = re.findall(date_pattern, ocr_strList[index_to_check_Coop])
    
    if dates_found:
        # Return the date found
        return dates_found[0]  # Assuming only one date is expected in the element
    
    # Return None if no date is found
    return None    


#Func to extract shop adress etc.
def extract_shop_address(ocr_strList):
    shop_address = " ".join(ocr_strList[5:7]) # Extract the address elements from ocr_strList-indices 5 and 6
    return shop_address

#Func to extract total price
def extract_total_price(ocr_strList):
    # Iterate through the string-list to find the index of 'TOTAL'
    for i in range(len(ocr_strList)):
        if ocr_strList[i] == 'TOTAL':
            # Check if the over-next element after 'TOTAL' (and after 'CHF') can be converted to a float
            # and thus is a valid number [CHF]
            if i + 2 < len(ocr_strList):
                try:
                    total_price = float(ocr_strList[i + 2])
                    return total_price
                except ValueError:
                    break  # Stop searching if the conversion fails
                
            break  # Stop searching once 'TOTAL' and the appropriate price-digit is found.
    return None  # Return None if 'TOTAL' or the price is not found.


# def extract_total_price(ocr_strList):
    # TotalPriceCoop_pattern = r'\b(TOTAL)\b'
    # matches = []
    # for line in ocr_strList:
        # matches.extend(re.findall(TotalPriceCoop_pattern, line))
    # return matches
    # total_price = 

#Func to extract company identification number / Unternehmens-Identifikationsnummer (UID, eg. CHE-123.456.789) - Coop:
def extract_UID(ocr_strList):
	UID_pattern = r'\b\d{3}\.\d{3}\.\d{3}\b' # digit[0-9]=#: ###.###.###, 'CHE-' still needs to be put before this digit-pattern!
	
	# Find the index of 'BAR' in the list
	indexOfElementBAR = ocr_strList.index('BAR')
	print('The index of the ocr_strList-element \'BAR\' is: ', indexOfElementBAR, '\n')
	# Define the range of indices you want to extract
	subList_StartIndex = max(0, indexOfElementBAR - 2)  # Ensure subList_StartIndex is non-negative
	subList_EndIndex = min(len(ocr_strList), indexOfElementBAR + 12)  # Ensure subList_EndIndex is within bounds

	# Get the sub-list of elements within the defined range
	UID_sublist = ocr_strList[subList_StartIndex:subList_EndIndex]
	
	# Convert the sub-list to a single string
	UID_sublist2String = ' '.join(UID_sublist)

	# Check within the sub_list for UID-pattern match
	UIDs_found = re.findall(UID_pattern, UID_sublist2String)
    
	if UIDs_found:
		# Prepend 'CHE-' to the UID found and return it all together
		return f'CHE-{UIDs_found[0]}'  # Assuming only one UID is expected in the element
	
	# Return None if no UID is found
	return None


#Func for indices according to the different shop's receipt-patterns / -extraction-methods:





# def write_receipt_to_csv(file_name, receipt):
    # with open(file_name, mode='w', newline='') as csvfile:
        # datacolumns = receipt[0].keys()
        # writer = csv.DictWriter(csvfile, fieldnames=datacolumns)
        # writer.writeheader()
        # for row in receipt:
            # writer.writerow(row)
            

def write_receipts_to_csv(file_name, receipt, ShopName, ShopAddress, uid, ReceiptDate):
    # Open CSV file in write mode
    with open(file_name, mode='w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        
        # Write the shop name to the CSV file
        writer.writerow(['Shop Name:', ShopName])
        # Write the shop address to the CSV file
        writer.writerow(['Shop Address:', ShopAddress])
        # Write the shop's UID to the CSV file
        writer.writerow(['Shop UID:', uid])
         # Write the receipt date to the CSV file
        writer.writerow(['Receipt date:', ReceiptDate])
        
        # Write an empty row for separation
        writer.writerow([])
        
        # Write the receipt items to the CSV file
        writer.writerow(['Items', 'Amount', 'Price [CHF]', 'Total Price [CHF]'])
        for col_element in receipt:
            writer.writerow([col_element['items'], col_element['amount'], col_element['price [CHF]'], col_element['total price [CHF]']])





# For Tesseract Usage on Linux Ubuntu within command line terminal:
# 1st: activate the Python environment where Tesseract-OCR package is installed
# 2nd: change to the directory containing the image file to do the OCR-process on.
# 3rd: Enter following cmd-line: tesseract imageName.png OutputTextfileName -l TextLanguageAbreviation(eg. deu, eng, fra) --dpi NumberOfDPIforOCR(eg. 150)
# 4th: View the extracted text in the appropriate txt-file. 
ocr_text = """
coop

Für mich und dich.

Solothurn Rosengarten

Artikel

Menge

Preis Aktion

Total

Free From Risottofil

1 5.95

5.95 0

Emmi Caffè Latte

1

1.95

1.95 0

Mini Babybel

1 5.10

5.10 0

Cractiv Chips Natur

1 2.35

2.35 0

TOTAL CHF

15.35

BAR

20.00

Zurück CHF

-4.65

COOP GENOSSENSCHAFT, CHE-116.311.185 MWST

GR

MWST%

TOTAL

MWST

0

2.50

15.35

0.37

ES BEDIENTE SIE Frau Demuth

Vielen Dank für Ihren Einkauf

9900010709121111700015351101

21.11.17 15:15 07091 00384371 001 0001101
"""

ocr_strList = string_to_word_list(ocr_text)
# ocr_strList = ['coop', 'Für', 'mich', 'und', 'dich.', 'Solothurn', 'Rosengarten', 'Artikel', 'Menge', 'Preis', 
# 'Aktion', 'Total', 'Free', 'From', 'Risottofil', '1', '5.95', '5.95', '0', 'Emmi', 'Caffè', 'Latte', '1', '1.95', 
# '1.95', '0', 'Mini', 'Babybel', '1', '5.10', '5.10', '0', 'Cractiv', 'Chips', 'Natur', '1', '2.35', '2.35', '0', 
# 'TOTAL', 'CHF', '15.35', 'BAR', '20.00', 'Zurück', 'CHF', '-4.65', 'COOP', 'GENOSSENSCHAFT,', 'CHE-116.311.185', 
# 'MWST', 'GR', 'MWST%', 'TOTAL', 'MWST', '0', '2.50', '15.35', '0.37', 'ES', 'BEDIENTE', 'SIE', 'Frau', 'Demuth', 'Vielen', 
# 'Dank', 'für', 'Ihren', 'Einkauf', '9900010709121111700015351101', '21.11.17', '15:15', '07091', '00384371', '001', '0001101']


receipt_date = extract_receipt_date(ocr_strList)
shop_name = ocr_strList[0]
#shop_names_string = '_'.join(shop_names)

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

print(f'\n\nThe string list has {len(ocr_strList)} string-elements!')
print(f'\n\n\nReceipt date: {receipt_date}, \nShop name: {shop_name}, \nCurrent date and time: {date_string}\n\n\n')

# Call the shop_address funct.:
shopAddress = extract_shop_address(ocr_strList)
print(f'This is the shop address: {shopAddress}\n')



# Call the extract_total_price function:
total_price = extract_total_price(ocr_strList)

# Check if the total price is extracted successfully:
if total_price is not None:
    print(f'Total price of shopping list items: {total_price} CHF \n')
else:
    print('Total price not found in the OCR string list. \n')

# Call the extract_UID function:
shop_UID = extract_UID(ocr_strList)

print('\n\n\n')



# # Usage example:
# shop_address = "Solothurn Rosengarten"
# receipt = [
    # {"prefix": "baked", "sufix": "beans", "Price [CHF]": "25.95"},
    # {"prefix": "milked", "sufix": "cow", "Price [CHF]": "20.00"},
    # {"prefix": "wonderful", "sufix": "girl", "Price [CHF]": "2.65"},
    # {"prefix": None, "sufix": "tree", "Price [CHF]": "3.80"}
# ]



# Create a dictionary-/key-value-list of the receipt-extractions:
Receipt = [
    {"items": "baked beans", "amount": "1", "price [CHF]": 23.50, "total price [CHF]": ""},
    {"items": "milked cow", "amount": "1", "price [CHF]": "20.00", "total price [CHF]": ""},
    {"items": "wonderful girl", "amount": "3", "price [CHF]": "2.65", "total price [CHF]": ""},
    {"items": "tree", "amount": None, "price [CHF]": 3.80, "total price [CHF]": ""}, 
    {"items": "", "amount": "", "price [CHF]": "", "total price [CHF]": total_price}
]

# Convert the Receipt list to a table format for prompting as a table within the terminal using tabulate
from tabulate import tabulate # Tabulate package is only installed in the virtual environment PyVEnvImageProcessing, 
							  # so for this,  preferably execute this PyScript within the terminal with the appropriate VEnv activated!!
table = tabulate(Receipt, headers="keys", tablefmt="fancy_grid")

# Print the table
print(table)


file_name = f"{receipt_date}_{shop_name}_ReceiptData{date_string}.csv"
#write_receipt_to_csv(file_name, Receipt)
write_receipts_to_csv(file_name, Receipt, shop_name, shopAddress, shop_UID, receipt_date)



if __name__ == "__main__":
    main()




