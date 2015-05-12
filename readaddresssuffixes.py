#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and possible mapping between the address suffixes and the full name 


"""

import xlrd
#datafile = "USPS Street Suffixes.xls"



def get_address_suffixes(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    
    data = {}
    for r in range(1, sheet.nrows):    
        cell_value_id =sheet.cell(r,2).value
        cell_value_value = sheet.cell(r,1).value
        if len(cell_value_id) > 0 and len(cell_value_value) >0:
            data[cell_value_id.capitalize()] = cell_value_value.capitalize()
            #add '.' to the suffixes
            cell_value_id = cell_value_id.capitalize() + "."
            data[cell_value_id] = cell_value_value.capitalize()
     
    #Correct the misspellings 
    data["Boulavard"] = "Boulevard"
    data["Boulavard."] = "Boulevard"
    data["Steet"] = "Street"
    data["Steet."] = "Street"
    return data


