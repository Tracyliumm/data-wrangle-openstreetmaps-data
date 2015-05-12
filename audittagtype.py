#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re

osm_file = open("sample.osm", "r")

tag_types = defaultdict(int)

def audit_tag_type(tag_types, tag_name):
    tag_types[tag_name] += 1

def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print "%s: %d" % (k, v) 

def is_tag_name(elem):
    #search possible city name
    #return (elem.tag == "tag") and (elem.attrib['k'] == "addr:city")

    #search possible county name
    #return (elem.tag == "tag") and (elem.attrib['k'] == "tiger:county")
    
    #search possible zipcode
    return (elem.tag == "tag") and (":zip" in elem.attrib['k'] or ":postcode" in elem.attrib['k'])
    #return (elem.tag == "tag") and (":postcode" in elem.attrib['k'])

def audit():
    for event, elem in ET.iterparse(osm_file):
        if is_tag_name(elem):
            audit_tag_type(tag_types, elem.attrib['v'])   
    print_sorted_dict(tag_types) 

if __name__ == '__main__':
    audit()
