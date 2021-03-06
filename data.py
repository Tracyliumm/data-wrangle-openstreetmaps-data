#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
from readaddresssuffixes import get_address_suffixes
from uniformstreetaddress import getUniformedStreetName, update_name
from uniformcityname import uniformaddress
from uniformzipcode import uniformzip
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#gold standard for the mapping between the Street Suffixes and full name
suffixefile = "USPS Street Suffixes.xls"
# UPDATE THIS VARIABLE
#
#mapping = { "St": "Street",
#            "St.": "Street",
#            "Ave": "Avenue",
#            "Rd.": "Road"
#            }

def shape_element(element, mapping):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        #print element.attrib
        #for tag in element.iter("tag"):
        #     print tag.attrib
        #node = element.attrib
        node['type'] = element.tag
        new_dict = {}
        pos_ind = 0
        pos_list = [0, 0]
        for attribute in element.attrib:
            #print "attribute", attribute
            if attribute in CREATED:
               if "created" not in node:
                    node['created'] = {}
               node['created'][attribute] = element.get(attribute)
            elif attribute == "lat":
               pos_list[0] =  float(element.get(attribute))
               pos_ind += 1
            elif attribute == "lon":
               pos_list[1] =  float(element.get(attribute))
               pos_ind += 1
            else:
               node[attribute] = element.get(attribute)

            for tag in element.iter("tag"):
                key = tag.attrib['k']
                
                if problemchars.search(key):
                    continue
                ### uniform the city name field in the address 
                elif key.startswith('addr:city'):
                    node = uniformaddress(tag.attrib['v'], node)
                ### uniform the street fields in the address            
                elif key.startswith('addr') and  key.count(":") == 1:
                    #update the street name if the format is not in the expected list
                    #print tag.attrib['v']
                    streetaddress_str = getUniformedStreetName(tag.attrib['v'].strip(), mapping)
                    if len(streetaddress_str) > 0:
                        if "address" not in node:
                            node['address'] = {}
                        node["address"][key.split(":")[1]] = streetaddress_str
                    #    print key.split(":")[1], streetaddress_str
                    #except:
                    #   raise
                ### uniform the zipcode fields in the address 
                elif ":zip" in key or ":postcode" in key:
                    
                    node = uniformzip(tag.attrib['v'], node)
                    
                    
                elif not key.startswith('addr') and ":" in key:
                    node[key] =tag.attrib['v']
                    
                elif key.startswith('addr') and key.count(":") == 2:
                    continue
                ### uniform the zipcode fields in the address which may combine the street and house number together
                elif key == "address":
                    fistpartaddress = tag.attrib['v'].split()[0]
                    if fistpartaddress.isdigit():
                        #update the street name if the format is not in the expected list
                        streetaddress_str = getUniformedStreetName(tag.attrib['v'][len(fistpartaddress):].strip(), mapping)
                        if len(streetaddress_str) >0: # valid address
                           if "address" not in node:
                               node['address'] = {}
                           node["address"]["housenumber"] = fistpartaddress
                           node["address"]["street"] = streetaddress_str
                    else:
                        #update the street name if the format is not in the expected list
                        streetaddress_str = getUniformedStreetName(tag.attrib['v'].strip(), mapping)
                        if len(streetaddress_str) >0: # valid address
                           if "address" not in node:
                               node['address'] = {}
                           node["address"]["housenumber"] = ""
                           node["address"]["street"] = streetaddress_str
                        
                                   
                else:
                    node[key] =tag.attrib['v']
                    
            #    if is_street_name(tag):
            #        audit_street_type(street_types, tag.attrib['v'])
        if element.tag == "way":
             for tag in element.iter("nd"):
                     
                     key = tag.attrib['ref']
                     if "node_refs" not in node:
                         node['node_refs'] = []
                     node["node_refs"].append(tag.attrib['ref'])
            
        if pos_ind == 2:
           node['pos'] = pos_list

           
        
        return node
    else:
        return None




def process_map(file_in, mapping, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element, mapping)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    mapping = {}
    mapping = get_address_suffixes(suffixefile)
    #print mapping 
    #data = process_map('sample.osm', mapping, True)
    data = process_map('san-francisco_california.osm', mapping, True)
    
    #pprint.pprint(data)
    
   

if __name__ == "__main__":
    test()
