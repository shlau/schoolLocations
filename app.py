import pandas as pd
import json
import requests
from pandas import ExcelFile, ExcelWriter
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

locations = []
""" places API call to get location of schools """
searchText = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=%s&inputtype=textquery&fields=formatted_address&key=%s"
""" f = open("addresses.txt","w+") """
for query in searchQueries:
    try:
        encodedQuery = urllib.parse.quote(query)
    except: 
        encodedQuery = urllib.quote_plus(query)
    formatted = searchText % (encodedQuery, API_KEY)
    result = requests.get(formatted)
    parsed_json = json.loads(result.content.decode('utf-8'))

    if (parsed_json['status'] == 'OK'):
        address = parsed_json['candidates'][0]['formatted_address']
    else:
        address = 'NO ADDRESS FOUND FOR %s' % query
    locations.append(address)
"""     f.write("%s\n" % address) """
""" f.close() """
addressDF = pd.DataFrame({'title':searchQueries,'address':locations })
writer = ExcelWriter('maptemplate.xlsx')
addressDF.to_excel(writer,'Sheet1',index=False)
writer.save()