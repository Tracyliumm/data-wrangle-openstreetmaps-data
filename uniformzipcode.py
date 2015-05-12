#!/usr/bin/env python
"""
Your task is as follows:
- To uniform the zipcode field

import re
"""
import re

def uniformzip(value_name, node):
    zipcodes = value_name.split(";")
    for zipcode in zipcodes:
        m = re.search("\d", zipcode)
        zipcode = zipcode[m.start():]
        if isint(zipcode.strip()):
            if "address" not in node:
                node['address'] = {}
            if "zipcodes" not in node['address']:
                node["address"]["zipcodes"] = []
                        
            if zipcode.strip() not in node["address"]["zipcodes"]:
                node["address"]["zipcodes"].append(zipcode.strip())
            else:
                continue#print zipcode
        
                        

    return node

def isint(value):
  try:
    int(value)
    return True
  except:
    return False
