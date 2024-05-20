# -*- coding: utf-8 -*-
"""
@data:      TOOL_removeTabs.py
@author:    Jannis Mathiuet
@versions:  ver 0.0.0 - 03.05.2024 
            
@desc: 
    remove tabulators in a file and replaces them with 4 spaces
"""
def main():
    # Define the filename to be processed
    filename = 'file.py'
    # remove tabs and replace with 4 spaces
    replace_char(filename, '\t', '    ')
    return 0

def replace_char(filepath:str, unwanted:str, replacement:str):
    # Initialize an empty list to store the modified lines
    new_lines = []
    try: 
        # Open the file in read mode
        with open(filepath, mode='r', encoding='utf-8') as file:
            # Iterate through each line in the file
            for line in file:
               # Replace each unwanted character with replacement character
               new_line = line.replace(unwanted, replacement)
               # Add the modified line to the list
               new_lines.append(new_line)
            # Close the input file
            file.close()
            
        # Open the file in write mode to overwrite the content  
        with open(filepath, mode='w', encoding='utf-8') as file:
            # Write each modified line back to the file
            for line in new_lines:
                file.write(line)
            # Close the output file
            file.close()
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()