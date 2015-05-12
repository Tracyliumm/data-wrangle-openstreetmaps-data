#!/usr/bin/env python
""" 
Add a single line of code to the insert_autos function that will insert the
automobile data into the 'autos' collection. The data variable that is
returned from the process_file function is a list of dictionaries, as in the
example in the previous video.
"""



def insert_steetmap(infile, db):
    data = process_file(infile)
    # Add your code here. Insert the data in one command.
    db.steetmap.insert(data)
    
  
if __name__ == "__main__":
    # Code here is for local use on your own computer.
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples
    collection = db.test

    insert_steetmap('sample.osm.json', db)
    print db.steetmap.find_one()
