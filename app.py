import pandas as pd
import json
import requests
from pandas import ExcelFile
from apikeys import API_KEY

""" load excel file """
filename = "Schools.xlsx"
df = pd.read_excel(filename, sheet_name = "Sheet1")

""" form search queries by concatenating school and district """
searchQueries = []
schools = df['School']
districts = df['District']
for i in range(len(schools)):
    searchQueries.append(schools[i] + ' ' + districts[i])

""" places API call to get location of schools """
search = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=%s&types=establishment&location=32.7153300,-117.1572600&radius=500&key=%s"
locations = []
for query in searchQueries:
    print("query is : %s" % query)
    formatted = search % (query, API_KEY)
    print("formatted is : %s" % formatted) 
    result = requests.get(formatted)
    parsed_json = json.loads(result.content)
    print(parsed_json['predictions'][0]['structured_formatting']['secondary_text'])

