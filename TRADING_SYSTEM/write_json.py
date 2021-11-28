import json
from bson.json_util import dumps

import os
from os.path import join, dirname
from dotenv import load_dotenv

import pymongo

#Database configuration
conn_str = "mongodb+srv://Ernesto905:mypassword@cluster0.h8feh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DBclient = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
myDB = DBclient["EducryptDatabase"]["tradingBot"]

fileData = myDB.find({"_id": "accounts"})[0]
#collection = db.tradingBot



jsonData = myDB.find({"_id": "accounts"})[0]

#print(jsonData)



#Initial account state
exampleUser = {'balance': 50000.00, 'cryptoHeld': {}}







def reLoad():
    pass

def deposit(user, amount):
    
    print(jsonData[user]['balance'])
    print(type(jsonData[user]['balance']))
    
    jsonData[user]['balance'] += float(amount)
    return jsonData[user]['balance']

def newUser(discordID):
    if discordID not in jsonData:
        print(jsonData)
        jsonData[discordID] = exampleUser
        
        write_to()

def checkPurchase(user, priceTag):
    if jsonData[user]['balance'] >= priceTag:
        return True
    else: return False

def makePurchase(user, priceTag, Ticker, amt):
    if checkPurchase(user, priceTag) == True:
        jsonData[user]['balance'] -= priceTag
        
        if Ticker in jsonData[user]['cryptoHeld']:

            
            for j,k in jsonData[user]['cryptoHeld'][Ticker].items():
                newVal = float(j) + priceTag
                newAmt = k + amt
            
            newEntry = {str(newVal) : newAmt}
            
            jsonData[user]['cryptoHeld'][Ticker] = newEntry
            write_to()
        else: 
            jsonData[user]['cryptoHeld'][Ticker] = {str(priceTag) : amt}
            
        write_to() 
        return True
    else: return False
    
def verifySale(user, Ticker, amt):
    for j, k in jsonData[user]["cryptoHeld"][Ticker].items():
        if k < amt:
            return False
        else: return True
    
def makeSale(user, priceTag, Ticker, amt):
    if verifySale(user, Ticker, amt) ==  True: 
        for j,k in jsonData[user]["cryptoHeld"][Ticker].items():
            totalVal = float(j)
            totalAmt = k
            newAmt = k - amt
    else: return False
    #magic 
    currentMean = totalVal / totalAmt 
    newEntry = {str(currentMean * newAmt) : newAmt}
    
    #update json data
    jsonData[user]["cryptoHeld"][Ticker] = newEntry
    jsonData[user]['balance'] += priceTag
    
    write_to()
    return currentMean


        

def viewFunds(user):
    return jsonData[user]['balance']
def viewHeld(user):
    #return a dictionary 
    #for crypto in jsonData[user]['cryptoHeld']:
    what = jsonData[user]["cryptoHeld"]
    entry = {}
    
    for j, k in jsonData[user]["cryptoHeld"].items():
        for d, v in k.items():
            entry[j] = v
    
     
    return entry

def write_to():
    
    #db
    myDB.replace_one({"_id": "accounts"}, jsonData)
    
    


