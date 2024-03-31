import csv

def write_receipts_to_csv(file_name, receipts):
    # Make and open new csv file
    with open(file_name, mode='w', newline='') as csvfile:
        # Set the column names to a list:
        datacolumns = receipts[0].keys()  # Get column names from the first item's keys
        
        writer = csv.DictWriter(csvfile, fieldnames=datacolumns)
        
        writer.writeheader()  # Write the header row with column names
        for row in receipts:  # Iterate through the list
            writer.writerow(row)  # Write each dictionary as a row

# Create List of receipts
Receipts = [
    {"prefix": "baked", "sufix": "beans", "Price [CHF]": "25.95"},
    {"prefix": "milked", "sufix": "cow", "Price [CHF]": "20.00"},
    {"prefix": "wonderful", "sufix": "girl", "Price [CHF]": "2.65"},
    {"prefix": None, "sufix": "tree", "Price [CHF]": 3.80}
]

# Get OCR output for shop's name and receipt date
shop_name = "ShopNamefromOCR"
receipt_date = "ReceiptDatefromOCR"

# Construct file name based on OCR output
file_name = f"{shop_name}_{receipt_date}_ReceiptData.csv"

# Call the function to write the receipts to CSV file
write_receipts_to_csv(file_name, Receipts)