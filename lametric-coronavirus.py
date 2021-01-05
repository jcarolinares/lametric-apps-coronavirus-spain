
'''
A simple coronavirus APP for my Lametric time device

It scrapes the official information from the Spanish goverment and put it on
the device. Using the datadista repository https://github.com/datadista/datasets/blob/master/COVID%2019/nacional_covid19.csv

Based on the idea of "H" who did the first Lametric with global data

Julián Caro Linares

jcarolinares@gmail.com
'''

import requests
import os
import json
import pandas as pd
import configparser

# Enviroment variables

config = configparser.ConfigParser()
config.read([os.path.expanduser('config')]) # Put your config file here or chage the path
lametric_app_token = config.get('lametric', 'token')
lametric_push_url = config.get('lametric', 'push_url')

# Download the national data
r = requests.get(
    'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv')
#print(r.text)

file = open("data.csv", 'wb')
file.write(r.text.encode('utf-8'))
file.close()

data = pd.read_csv("data.csv",encoding ='utf-8')
print(data)
print("datos")
print(data["casos_total"].max())  # It takes the maximum value, by definition, the most updated one
print(int(data["fallecimientos"].max()))
print(str(int(data["altas"].max())))

list_cases = []
for x in data["casos_total"]: # Little hack to easy convert numpy int64 to int
    if pd.isna(x):
        list_cases.append(0)
        print(x)
    else:
        list_cases.append(x)
        print(x)

relative_cases = []
for i in range(len(list_cases)):
    if (i!=0):
        relative_cases.append(list_cases[i]-list_cases[i-1])
    else:
        relative_cases.append(list_cases[i])
print(relative_cases[-10:])

# Download the regional data
r = requests.get(
    'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos.csv')
#print(r.text)

file = open("data_regional.csv", 'wb')
file.write(r.text.encode('utf-8'))
file.close()

data_regional = pd.read_csv("data_regional.csv",encoding ='utf-8').loc[:,:]
# print(data_regional)
data_madrid = data_regional.loc[13,:]
print(data_madrid)  # It takes the maximum value, by definition, the most updated one
print(data_madrid[-1])


# Download Spanish vaccination by region
# https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_vacunas.csv
r = requests.get(
    'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_vacunas.csv')
print(r.text)

file = open("ccaa_vacunas.csv", 'wb')
file.write(r.text.encode('utf-8'))
file.close()

data_vaccines = pd.read_csv("ccaa_vacunas.csv",encoding ='utf-8', sep=";")

print(data_vaccines)
data_vaccines.set_index("CCAA", inplace=True)
vaccines_number= data_vaccines.loc['Madrid','Dosis administradas']
print(vaccines_number)
vaccines_percentage = data_vaccines.loc['Madrid','% sobre entregadas']
print(vaccines_percentage)

# Lametric post request
headers = {
    'Accept': 'application/json',
    'X-Access-Token': lametric_app_token,
    'Cache-Control': 'no-cache',
}
data_request = {"frames": [
    {
        "text": "SPAIN",
        "icon": "i579",
        "index": 0
    },
    {
        "text": str(int(data["casos_total"].max())),
        "icon": "i35318",
        "index": 1
    },
    {
        "text": str(int(data["fallecimientos"].max())),
        "icon": "a35723",
        "index": 2
    },
    {
        "text": str(int(data["altas"].max())),
        "icon": "i35319",
        "index": 3
    },
    {
    "text": "MADRID",
       "icon": "i933",
       "index": 4
    },
    {
       "text": str(int(data_madrid[-1])),
       "icon": "i933",
       "index": 5
    },
    {
        "text": vaccines_number,
        "icon": "i22570",
        "index": 6
    },
    {
        "text": vaccines_percentage,
        "icon": 'null',
        "index": 7
    }
]}
response = requests.post(lametric_push_url,
                         headers=headers, data=json.dumps(data_request))
print(response)
