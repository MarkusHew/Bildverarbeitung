# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:43:07 2024

@author: janni
"""
import csv
configfile = r'config.csv'
def search_company(companyName:str):
    company_info = ['']*8
    found_company: bool=0
    # read data from configfile
    with open(configfile) as config:
        data_semicolon = csv.reader(config, delimiter=';')
        data_comma = csv.reader(configfile, delimiter=',')
        
        # determine which format and get correct data
        data = data_semicolon
        if (len(data_semicolon) < len(data_comma)):
            data = data_comma
        for row in data:
            if (row[0] is companyName):
                company_info = row
                found_company = 1
    if (not found_company):
        return None
    
    return company_info

class Shop:
    def __init__(self, companyName:str):
        data = search_company(companyName)
        if data is None:
        
            print()
        # given information
        self.name 
        self.mwst_UID 

        # line numbers (lino) of relevant information
        self.lino_name 
        self.lino_adress 
        self.lino_telefon 
        self.lino_mwst 
        self.lino_date 
        self.lino_total 
        self.lino_startItems 
        
shopinfo = Shop('coop')
shopinfo.name
# =============================================================================
#         i = 0
#         self.name = data[i]
#         i+=1
#         self.mwst_UID = data[i]
#         i+=1
#         
#         # row numbers of relevant information
#         self.lino_name = data[i]
#         i+=1
#         self.lino_location = data[i]
#         i+=1
#         self.lino_telefon = data[i]
#         i+=1
#         self.lino_mwst = data[i]
#         i+=1
#         self.lino_date = data[i]
#         i+=1
#         self.lino_total = data[i]
#         i+=1
#         self.lino_startItems = data[i]
# =============================================================================
        
