from requests.auth import HTTPBasicAuth
import requests
from pycoingecko import CoinGeckoAPI
import json
import os

cg = CoinGeckoAPI()

def show_price(Ticker):
    data = cg.get_price(ids=Ticker, vs_currencies='usd')
    return data[Ticker]['usd']
    
def retAllCrypto():
    data = cg.get_coins_list()
    
    ls = []
    for i in data:
        ls.append(i['id'])
    
    return ls

#rint(retAllCrypto())
#print(retAllCrypto())

