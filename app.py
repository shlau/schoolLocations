import pandas as pd
import json
import requests
from pandas import ExcelFile
from apikeys import API_KEY
import urllib

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
searchText = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&inputtype=textquery&fields=formatted_address&key=%s"
f = open("addresses.txt","w+")
for query in searchQueries:
    """     print("query is : %s" % query) """
    encodedQuery = urllib.parse.quote(query)
    formatted = searchText % (encodedQuery, API_KEY)
    """     print("formatted is : %s" % formatted)   """
    result = requests.get(formatted)
    parsed_json = json.loads(result.content)
    """     print(parsed_json['candidates'][0]['formatted_address']) """
    """     print(parsed_json['predictions'][0]['structured_formatting']['secondary_text']) """
    if (parsed_json['status'] == 'OK'):
        address = parsed_json['candidates'][0]['formatted_address']
    else:
        address = 'NO ADDRESS FOUND FOR %s' % query
    f.write("%s\n" % address)
f.close()
