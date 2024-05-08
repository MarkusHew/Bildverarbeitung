# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:46:17 2024

@author: janni
"""
filename = 'DatatoCSV.py'

new_lines = []

# get all lines form input file and replace tabs with spaces
inputFile = open(filename, 'r') 
for line in inputFile:
   new_line = line.replace('\t', '    ')
   new_lines.append(new_line)
inputFile.close()

# write all lines back into file
exportFile = open(filename, 'w')
for line in new_lines:
    exportFile.write(line) 
exportFile.close()
