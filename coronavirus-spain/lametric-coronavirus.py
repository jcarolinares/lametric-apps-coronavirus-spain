
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
config.read([os.path.expanduser('~/lametric-apps/coronavirus-spain/config')]) # Put your config file here or chage the path
print(config.sections())
lametric_app_token = config.get('lametric', 'token')

# Download the national data
r = requests.get(
    'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv')
#print(r.text)

file = open("data.csv", 'wb')
file.write(r.text.encode('utf-8'))
file.close()

data = pd.read_csv("data.csv",encoding ='utf-8')
print(data)
print(data["casos_total"].max())  # It take the maximum value, by definition, the most updated one
print(int(data["fallecimientos"].max()))
print(str(int(data["altas"].max())))

list_cases = []
for x in data["casos_total"]: # Little hack to easy convert numpy int64 to int
    list_cases.append(x)

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
print(data_madrid)  # It take the maximum value, by definition, the most updated one
print(data_madrid[-1])
# print(int(data["fallecimientos"].max()))
# print(str(int(data["altas"].max())))

# list_cases = []
# for x in data["casos"]: # Little hack to easy convert numpy int64 to int
#     list_cases.append(x)


# Lametric post request
headers = {
    'Accept': 'application/json',
    'X-Access-Token': lametric_app_token,
    'Cache-Control': 'no-cache',
}
data_request = {"frames": [
    {
        "text": "SPAIN",
        "icon": "i579"
    },
    {
        "text": str(data["casos_total"].max()),
        "icon": "i35318"
    },
    {
        "text": str(int(data["fallecimientos"].max())),
        "icon": "a35723"
    },
    {
        "text": str(int(data["altas"].max())),
        "icon": "i35319"
    },
    {
        "index": 4,
        "chartData": relative_cases[-10:]
    },
    {
    "text": "MADRID",
       "icon": "i933",
       "index": 5
    },
    {
       "text": str(data_madrid[-1]),
       "icon": "i933",
       "index": 6
    }
]}
response = requests.post('https://developer.lametric.com/api/v1/dev/widget/update/com.lametric.37cb93122b1d49ab1d630f5dfe23bdc1/7',
                         headers=headers, data=json.dumps(data_request))
print(response)
