# Information extraction from OCR-output into a csv-file

# Needed library imports
## Import csv-package for creating csv-file:
import csv

## Import package for "regular expressions" to define and search string-patterns:
import re

## Import package for current date and time (Timecode):
from datetime import datetime

## Import package for plotting a table for testing purposes
from tabulate import tabulate 
This package is only used for fast and uncomplicated testings while executing this PyScript directly. 
It can be used to show wheather the functions taking the hard-coded testing-string-list as argument work correctly or not... 

# Additional notes
Note that some of the packages might only be installed in the appropriate Python virtual environment (PyVEnv), so for this,  preferably execute this PyScript within the terminal with the appropriate PyVEnv activated!!


