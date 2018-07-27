import pandas as pd
from pandas import ExcelFile

filename = "Schools.xlsx"
df = pd.read_excel(filename, sheet_name = "Sheet1")

searchQueries = []
schools = df['School']
districts = df['District']
for i in range(len(schools)):
    searchQueries.append(schools[i] + ' ' + districts[i])
    
print(searchQueries)
