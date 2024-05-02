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

from tabulate import tabulate # Tabulate package is only installed in the virtual environment PyVEnvImageProcessing, 
                            # so for this,  preferably execute this PyScript within the terminal with the appropriate VEnv activated!!



# Function to convert ocr-text (as a single string) to a list of strings:
# def string_to_word_list(input_string):
    # # Split the input string into words
    # word_list = input_string.split()
    # return word_list

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




# def extract_receipt_date(ocr_strList):
    # date_pattern = r'\b(?:\d{2}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4})\b'  # Date pattern (DD.MM.YY or DD.MM.YYYY)
    # #!!! maybe also to replace by a range instead of a single index num, for reliability!!:
    # #index_to_check_Coop = -6  # Index of the 6th-last element in the list 
    
    # # Check the 6th-last element for the date pattern match
    # for i in range(len(ocr_strList)):
        # #print(ocr_strList[i])
        # dates_found = re.findall(date_pattern, ocr_strList[i])
        # #print("Test",dates_found)
        # if dates_found:        
            # # Return the date found
            # return dates_found[0]  # Assuming only one date is expected in the element
    
    # #Return None if no date is found
    # return None    

# Or rather this version, since safer - should work for any Coop receipt (no matter how long it is)!:
def extract_receipt_date(ocr_strList):
    date_pattern = r'\b(?:\d{2}\.\d{2}\.\d{2}|\d{2}\.\d{2}\.\d{4})\b'  # Date pattern (DD.MM.YY or DD.MM.YYYY)
    # Check within an index-range instead of a single index num, for reliability!!:
    ###index_to_check_Coop = -6  # Index of the 6th-last element in the list 
    # Check the 6th-last element for the date pattern match
    ###dates_found = re.findall(date_pattern, ocr_strList[index_to_check_Coop])
    
    # Define the range of indices to check
    theor_date_index = -6  # Index of the 6th-last element in the list, where the coop-date usually is
    DateCheck_StartIndex = theor_date_index - 4  # Start index of the range to check for date-pattern
    DateCheck_EndIndex = len(ocr_strList) - 1  # Global End index
    
    # Iterate over the specified range of indices
    for i in range(DateCheck_StartIndex, DateCheck_EndIndex + 1):
        # Check the element at the current index for the date pattern match
        dates_found = re.findall(date_pattern, ocr_strList[i])

        if dates_found:
            # Return the date found
            return dates_found[0]  # Assuming only one date is expected in the element
        
    # Return None if no date is found
    return None




#Func to extract shop adress etc.
def extract_shop_address(ocr_strList):
    shop_address = " ".join(ocr_strList[8:11]) # Extract the address elements from ocr_strList-indices 5 and 6
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
	indexOfElementBAR = ocr_strList.index('DAR')
	print('The index of the ocr_strList-element \'BAR\' is: ', indexOfElementBAR, '\n')
	# Define the range of indices you want to extract
	subList_StartIndex = max(0, indexOfElementBAR - 2)  # Ensure subList_StartIndex is non-negative
	subList_EndIndex = min(len(ocr_strList), indexOfElementBAR + 12)  # Ensure subList_EndIndex is within global bounds

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


# group string-list elements in range [dict_StartIndex:dict_EndIndex] to line-sublists
# Until 'TOTAL' is not reached, from and excl. 'Total' onwards, search for first next digit (integer), 
# append that with previous line-sublist-elements until and excl. 'Total' or until and 
# excl. previous digit-element (as 1st line-sublist-element) and append next 
# 3 elements (that should be digits, maybe floats) to line-sublist_i
def generate_line_sublists(ocr_strList):
    # Find the index of 'Total' and 'TOTAL' in the list
    index_of_Total = ocr_strList.index('Total')
    index_of_TOTAL = ocr_strList.index('TOTAL')
    
    # Initialize a list to hold all line sublists
    line_sublists = []
    
    # Iterate over the indices between 'Total' and 'TOTAL'
    start_index = index_of_Total + 1
    end_index = index_of_TOTAL - 1
    i = start_index
    
    while i <= end_index:
        # Initialize a sublist for the current line
        currentLine_sublist = []
        
        # Collect elements until encountering a non-numeric string or reaching the end of the range
        while i <= end_index and not ocr_strList[i].isdigit() and ocr_strList[i] != 'TOTAL':
            currentLine_sublist.append(ocr_strList[i])
            i += 1
        
        # Add elements until encountering the next non-numeric string or reaching the end of the range
        while i <= end_index and (ocr_strList[i].isdigit() or ocr_strList[i] == '.' or ocr_strList[i] == '0'):
            currentLine_sublist.append(ocr_strList[i])
            i += 1
        
        # Append the collected line sublist to the list of line sublists
        line_sublists.append(currentLine_sublist)
    
    # Group even-indexed line sublists with odd-indexed line sublists
    combined_line_sublists = []
    for j in range(0, len(line_sublists) - 1, 2):
        combined_line_sublists.append(line_sublists[j] + line_sublists[j + 1])
    
    return combined_line_sublists

# # Generate combined line sublists
# combined_line_sublists = generate_line_sublists(ocr_strList)

# # Print the combined line sublists
# for i, combined_line_sublist in enumerate(combined_line_sublists, start=1):
    # print(f"combined_line_sublist_{i}: {combined_line_sublist}")



# def generate_line_sublists(ocr_strList):
    # # Find the index of 'Total' and 'TOTAL' in the list
    # index_of_Total = ocr_strList.index('Total')
    # index_of_TOTAL = ocr_strList.index('TOTAL')
    
    # # Initialize a list to hold all line sublists
    # line_sublists = []
    
    # # Iterate over the indices between 'Total' and 'TOTAL'
    # start_index = index_of_Total + 1
    # end_index = index_of_TOTAL - 1
    # i = start_index
    
    # while i <= end_index:
        # # Initialize a sublist for the current line
        # line_sublist = []
        
        # # Collect elements until encountering a non-numeric string or reaching the end of the range
        # while i <= end_index and not ocr_strList[i].isdigit() and ocr_strList[i] != 'TOTAL':
            # line_sublist.append(ocr_strList[i])
            # i += 1
        
        # # Add elements until encountering the next non-numeric string or reaching the end of the range
        # while i <= end_index and (ocr_strList[i].isdigit() or ocr_strList[i] == '.' or ocr_strList[i] == '0'):
            # line_sublist.append(ocr_strList[i])
            # i += 1
        
        # # Add the collected line sublist to the list of line sublists
        # line_sublists.append(line_sublist)
    
    # return line_sublists


# def generate_line_sublists(ocr_strList):
    # # Find the index of 'Total' and 'TOTAL' in the list
    # index_of_Total = ocr_strList.index('Total')
    # index_of_TOTAL = ocr_strList.index('TOTAL')
    
    # # Initialize a list to hold all line sublists
    # line_sublists = []
    
    # # Iterate over the indices between 'Total' and 'TOTAL'
    # start_index = index_of_Total + 1
    # end_index = index_of_TOTAL - 1
    # i = start_index
    
    # while i <= end_index:
        # # Initialize a sublist for the current line
        # line_sublist = []
        
        # # Collect the first non-numeric string (excluding 'TOTAL') as the start of the line sublist
        # while i <= end_index and (ocr_strList[i].isdigit() or ocr_strList[i] == 'TOTAL'):
            # i += 1
        
        # # Add the first non-numeric string to the current line sublist
        # if i <= end_index:
            # line_sublist.append(ocr_strList[i])
            # i += 1
        
        # # Collect subsequent numeric values until encountering a non-numeric string (excluding 'TOTAL')
        # while i <= end_index and (ocr_strList[i].isdigit() or ocr_strList[i] == '.'):
            # line_sublist.append(ocr_strList[i])
            # i += 1
        
        # # Add the collected line sublist to the list of line sublists
        # line_sublists.append(line_sublist)
    
    # return line_sublists


# def generate_line_sublists(ocr_strList):
    # # Find the index of 'Total' and 'TOTAL' in the list
    # index_of_Total = ocr_strList.index('Total')
    # index_of_TOTAL = ocr_strList.index('TOTAL')
    
    # # Initialize a list to hold all line sublists
    # line_sublists = []
    
    # # Iterate over the indices between 'Total' and 'TOTAL'
    # start_index = index_of_Total + 1
    # end_index = index_of_TOTAL - 1
    # i = start_index
    
    # while i <= end_index:
        # # Initialize a sublist for the current line
        # line_sublist = []
        
        # # Collect elements for the current line until encountering a numeric value or any string except 'TOTAL'
        # while i <= end_index and (ocr_strList[i].isdigit() or (ocr_strList[i] != 'TOTAL' and not ocr_strList[i].isalpha())):
            # line_sublist.append(ocr_strList[i])
            # i += 1
        
        # # Add the collected line sublist to the list of line sublists
        # line_sublists.append(line_sublist)
        
        # # Move to the next element
        # i += 1
    
    # return line_sublists

# # Generate line sublists
# line_sublists = generate_line_sublists(ocr_strList)

# # Print the line sublists
# for i, line_sublist in enumerate(line_sublists, start=1):
    # print(f"line_sublist_{i}: {line_sublist}")





# def generate_line_sublists(ocr_strList):
    # # Find the indices of 'Total' and 'TOTAL'
    # start_index = ocr_strList.index('Total')
    # end_index = ocr_strList.index('TOTAL')
    
    # # Extract the relevant part of the list
    # relevant_part = ocr_strList[start_index + 1:end_index]
    
    # line_sublists = []
    # current_sublist = []

    # for item in relevant_part:
        # current_sublist.append(item)
        
        # # Check if the item is a digit (integer or float)
        # if re.match(r'^-?\d+(\.\d+)?$', item):  # Regular expression to match integer or float numbers
            # line_sublists.append(current_sublist)
            # current_sublist = []  # Reset the current sublist
    
    # # Append the last incomplete sublist if any
    # if current_sublist:
        # line_sublists.append(current_sublist)
    
    # return line_sublists

    # # # line_sublists = []
    # # # start_index = ocr_strList.index('Total') + 1
    # # # end_index = ocr_strList.index('TOTAL') - 1

    # # # i = start_index
    # # # while i <= end_index:
        # # # line_sublist = []
        # # # while i <= end_index and not ocr_strList[i].isdigit():
            # # # line_sublist.append(ocr_strList[i])
            # # # i += 1
        # # # line_sublists.append(line_sublist)
        # # # i += 1

    # # # return line_sublists


# # Call the function to generate line_sublists
# line_sublists = generate_line_sublists(ocr_strList)

# # Print the generated line_sublists
# for i, sublist in enumerate(line_sublists, 1):
    # print(f"line_sublist_{i}: {sublist}")



# Generate dictionary for shop item details:
def generate_dictionary(ocr_strList):
	# Find the indices of 'Total' and 'TOTAL' in the list
	dict_StartIndex = ocr_strList.index('Total')
	dict_EndIndex = ocr_strList.index('TOTAL')

	# Extract relevant elements for the dictionary
	items = ocr_strList[dict_StartIndex + 1:dict_EndIndex]  # Elements between 'Total' and 'TOTAL'
	amount = items[0]  # Assuming the first element after 'Total' is the amount
	price_chf = items[1]  # Assuming the second element after 'Total' is the price in CHF
	total_price_chf = items[2]  # Assuming the third element after 'Total' is the total price in CHF

	# Create the dictionary
	receipt_dict = {
		'items': ' '.join(items),
		'amount': amount,
		'price [CHF]': price_chf,
		'total price [CHF]': total_price_chf
	}

	# Print the resulting dictionary
	print(receipt_dict)



#Func for indices according to the different shop's receipt-patterns / -extraction-methods:





# def write_receipt_to_csv(file_name, receipt):
    # with open(file_name, mode='w', newline='') as csvfile:
        # datacolumns = receipt[0].keys()
        # writer = csv.DictWriter(csvfile, fieldnames=datacolumns)
        # writer.writeheader()
        # for row in receipt:
            # writer.writerow(row)
            
######### ###### ######
# def write_receipts_to_csv(file_name, receipt, ShopName, ShopAddress, uid, ReceiptDate):
    # # Open CSV file in write mode
    # with open(file_name, mode='w', newline='') as csvfile:
        # # Create a CSV writer object
        # writer = csv.writer(csvfile)
        
        # # Write the shop name to the CSV file
        # writer.writerow(['Shop Name:', ShopName])
        # # Write the shop address to the CSV file
        # writer.writerow(['Shop Address:', ShopAddress])
        # # Write the shop's UID to the CSV file
        # writer.writerow(['Shop UID:', uid])
         # # Write the receipt date to the CSV file
        # writer.writerow(['Receipt date:', ReceiptDate])
        
        # # Write an empty row for separation
        # writer.writerow([])
        
        # # Write the receipt items to the CSV file
        # writer.writerow(['Items', 'Amount', 'Price [CHF]', 'Total Price [CHF]'])
        # for col_element in receipt:
            # writer.writerow([col_element['items'], col_element['amount'], col_element['price [CHF]'], col_element['total price [CHF]']])





# def write_receipts_to_csv(file_name, combined_line_sublists, ShopName, ShopAddress, uid, ReceiptDate):
    # # Open CSV file in write mode
    # with open(file_name, mode='w', newline='') as csvfile:
        # # Create a CSV writer object
        # writer = csv.writer(csvfile)
        
        # # Write the shop name to the CSV file
        # writer.writerow(['Shop Name:', ShopName])
        # # Write the shop address to the CSV file
        # writer.writerow(['Shop Address:', ShopAddress])
        # # Write the shop's UID to the CSV file
        # writer.writerow(['Shop UID:', uid])
         # # Write the receipt date to the CSV file
        # writer.writerow(['Receipt date:', ReceiptDate])
        
        # # Write an empty row for separation
        # writer.writerow([])
        
        # # Write the receipt items to the CSV file
        # writer.writerow(['Items', 'Amount', 'Price [CHF]', 'Total Price [CHF]'])
        
        # # Iterate over combined_line_sublists
        # for sublist in combined_line_sublists:
            # # Extract relevant elements for each sublist
            # items = sublist[0]
            # amount = sublist[1]
            # price_chf = sublist[2]
            # total_price_chf = sublist[3]
            
            # # Write the extracted elements to the CSV file
            # writer.writerow([items, amount, price_chf, total_price_chf])
            
def write_receipts_to_csv(file_path, combined_line_sublists, total_price_chf, ShopName, ShopAddress, uid, ReceiptDate):
    # Open CSV file in write mode
    with open(file_path, mode='w', newline='') as csvfile:
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
        
        # Iterate over combined_line_sublists
        for sublist_of_CoLiSu in combined_line_sublists:
            # Initialize variables
            items = ''
            amount = ''
            price_chf = ''
            found_amount = False
            found_price = False
            
            # Iterate over elements in the sublist_of_CoLiSu
            for i in range(len(sublist_of_CoLiSu)):
                # If the element contains digits, it's either 'Amount' or 'Price [CHF]'
                if re.search(r'\d', sublist_of_CoLiSu[i]):
                    if not found_amount:
                        amount = sublist_of_CoLiSu[i]
                        found_amount = True
                    elif not found_price:
                        price_chf = sublist_of_CoLiSu[i]
                        found_price = True
                        # Since we only need the first amount and price_chf, we break after finding them
                        break
                 # If the element is a string, concatenate it to the 'items' string
                else:
                    items += sublist_of_CoLiSu[i] + ' '
            
            # Write the extracted elements to the CSV file
            writer.writerow([items.strip(), amount, price_chf, ''])
# Write an empty row for separation
        writer.writerow([])
        
        # Write the total price to the CSV file
        writer.writerow(['', '', '', total_price_chf])
      

# =============================================================================
# TESTING
# =============================================================================
def main():

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
    table = tabulate(Receipt, headers="keys", tablefmt="fancy_grid")

    # Print the table
    print(table)



    # Generate combined line sublists
    combined_line_sublists = generate_line_sublists(ocr_strList)

    # Print the combined line sublists
    for i, combined_line_sublist in enumerate(combined_line_sublists, start=1):
        print(f"combined_line_sublist_{i}: {combined_line_sublist}")

    # # Call the function to generate line_sublists
    # line_sublists = generate_line_sublists(ocr_strList)

    # # Print the generated line_sublists
    # for i, sublist in enumerate(line_sublists, 1):
        # print(f"line_sublist_{i}: {sublist}")

    # # Generate line sublists
    # line_sublists = generate_line_sublists(ocr_strList)

    # # Print the line sublists
    # for i, line_sublist in enumerate(line_sublists, start=1):
        # print(f"line_sublist_{i}: {line_sublist}")





    #file_name = f"{receipt_date}_{shop_name}_ReceiptData{date_string}.csv"
    #write_receipt_to_csv(file_name, Receipt)
    #write_receipts_to_csv(file_name, Receipt, shop_name, shopAddress, shop_UID, receipt_date)
    write_receipts_to_csv(file_path, combined_line_sublists, total_price, shop_name, shopAddress, shop_UID, receipt_date)



if __name__ == "__main__":
    main()




