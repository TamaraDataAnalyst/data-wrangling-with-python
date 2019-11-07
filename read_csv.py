import re
import csv
import json


def read_address_field(csvfile):
    infile = open(csvfile) 
    reader = csv.reader(infile)
    header = next(reader)
    address_field = (row[2].replace(',','') for row in reader)
    return address_field
    
ADDRESS_PATTERN = r'^(\w+-?\w+\s\S+\s\S+\s\S+)\s(\S+)\s(\d{5})\s(\S+)'
STREET_ADDRESS = re.compile(ADDRESS_PATTERN)   

def parse_address_field(address_field):
    groups = (STREET_ADDRESS.match(line) for line in address_field)
    tuples = (g.groups() for g in groups if g)

    colnames = ('addr','city','zipcode','state')
    
    address_fields = (dict(zip(colnames,t)) for t in tuples)

    return address_fields

def save_to_json(object):
    for item in object:
        yield json.dumps(item)
 
 
if __name__=='__main__':
    csvfile = read_address_field('data\issues.csv')
    address_fields = parse_address_field(csvfile)
    savefile = save_to_json(address_fields)
    for item in savefile:
        print(item)
    
