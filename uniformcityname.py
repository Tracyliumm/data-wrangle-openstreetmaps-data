#!/usr/bin/env python
"""
Your task is as follows:
- To uniform the city name field


"""
def uniformaddress(city_name, node):
    city_name = city_name.strip().capitalize().split(".")[0]
    # correct the mainly common typo 
    if  city_name == "San Francicsco":
        city_name = "San Francisco"

    if "address" not in node:
        node['address'] = {}

    node["address"]["city"] = city_name
    

    return node
