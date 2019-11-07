import requests
import json


######### READ DATA FROM API ###########
url = "https://seeclickfix.com/api/v2/issues?"

issues_json = requests.get(url).json()

############ DATA TRANSFORMATION ############
issues = list()

for i, entry in enumerate(issues_json['issues']):
    row = {}
    row['created_at'] = entry['created_at']
    row['summary'] = entry['summary']
    row['address'] = entry['address']
    issues.append(row)

############ DATA QUERYING ###################
from collections import Counter
from dateutil.parser import parse

dates = [parse(issues[0]['created_at']) for issue in issues]
count_months = Counter(date.month for date in dates)
count_weekdays = Counter(date.weekday() for date in dates)

view_last_5_issues = sorted(issues,
                            key=lambda i: i['created_at'],
                            reverse=True)[:5]

view_last_5_summaries = [issues['summary'] 
                                    for issues in view_last_5_issues]

############ SAVE INTO CSV FORMAT ###################
import csv
import os

FILENAME = 'data\issues.csv'

keys = issues[0].keys()
fout = open(FILENAME,'w', newline='')
writer = csv.writer(fout)
writer.writerow(keys)

for entry in issues:
    row=[]
    for key in keys:
        row.append(entry[key])
    writer.writerow(row)
fout.close()