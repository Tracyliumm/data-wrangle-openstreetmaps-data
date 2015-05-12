#!/usr/bin/env python
"""
Your task is as follows:
- uniform the street names

"""
import re


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

def getUniformedStreetName(ori_name, mapping):
    ori_name = ori_name.capitalize()
    m = street_type_re.search(ori_name)
    
    if m:
        street_type = m.group().capitalize()
        
        if street_type in expected:
           better_name = ori_name
        elif street_type not in expected and street_type in mapping.keys():
           better_name = update_name(ori_name, mapping)
           
        else:
           better_name = ''
    else:
        better_name = ''
        
    return better_name
 
def update_name(name, mapping):

    # YOUR CODE HERE
    oldaddtype = name.split(' ')[-1].capitalize()

    newname = name.replace(oldaddtype, mapping[oldaddtype])
    name = newname

    return name
