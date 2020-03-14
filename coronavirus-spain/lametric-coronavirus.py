# -*- coding: utf-8 -*-

'''
A simple coronavirus APP for my Lametric time device

It scrapes the official information from the Spanish goverment and put it on
the device. Using the datadista repository https://github.com/datadista/datasets/blob/master/COVID%2019/nacional_covid19.csv

Based on the idea of "H" who did the first Lametric with global data

Julián Caro Linares

jcarolinares@gmail.com
'''

import requests
import json
import pandas as pd

# Enviroment variables
lametric_app_token = '<token>'


# Download of the data
r = requests.get(
    'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv')

file = open("data.csv", 'w')
file.write(r.text)
file.close()

data = pd.read_csv("data.csv")
print(data["Casos"].max())  # It take the maximum value, by definition, the most updated one
print(int(data["Fallecimientos"].max()))

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
        "text": str(data["Casos"].max()),
        "icon": "i35318"
    },
    {
        "text": str(int(data["Fallecimientos"].max())),
        "icon": "a35723"
    }
]}
response = requests.post('https://developer.lametric.com/api/v1/dev/widget/update/com.lametric.37cb93122b1d49ab1d630f5dfe23bdc1/2',
                         headers=headers, data=json.dumps(data_request))
print(response)
