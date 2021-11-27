from api_Gecko import show_price, retAllCrypto
from write_json import makePurchase, viewFunds, newUser, viewHeld, makeSale, deposit
import discord
from discord.ext import commands

import os
from os.path import join, dirname
from dotenv import load_dotenv




client = discord.Client()  #intialize bot


#Test command structure viability
def verifyStructure(buy, amt, crypto):
    if (buy.lower() == '$buy' or buy.lower() == '$sell') and type(amt) == float and verifyCrypto(crypto):
        return True
    else: 
        print((buy.lower() == '$buy' or buy.lower() == '$sell'))
        print(type(amt) == float)
        print(verifyCrypto(crypto))
        return False

#verify Ticker is viable
def verifyCrypto(crypto):
    if crypto in retAllCrypto(): 
        return True
    else: 
        return False
    
    
 
@client.event   
async def on_ready():
    print('A wild Trading Bot appeared! His name is: {0.user}'.format(client))
    


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    

    
    #Hello, my name is lazy. Nice to meet you
    msg = message.content
    send = message.channel.send
    userID = str(message.author)
    newUser(userID)
    
    channel_id = message.channel.id #this is super inneficient and embodies hackathons everywhere
    channel = client.get_channel(channel_id)

    transaction = False
    command = msg.split()
    
    if len(command) == 3:
        purchase = command[0]
        amount = command[1]
        try: amount = float(amount)
        except: pass
        coin = command[2]
        transaction = True
    
    if len(command) == 2:
        qty = command[1]
        try: qty = float[qty] 
        except: pass
    
    
    if msg == "$help":
        await send(f"Hello {message.author}, and welcome to trader Bob's trading emporium where we host all your trading needs!")
        await send("Where we're proud to bring your real time crypto paper trading capabilities thorugh the Use of CoinGecko's API!")
        await send("Please use the following format for interacting with me:\nBuy: $Buy [AMOUNT] [TICKER]\nSell: $Sell [AMOUNT] [TICKER]\nView Portfolio: $View\nDeposit Funds: $deposit [AMOUNT]")
    
    elif transaction == True and verifyStructure(purchase, amount, coin) == True:
        
        price = float(show_price(coin)) * float(amount)
        
        if msg.startswith('$buy'):
            
            if makePurchase(userID, price, coin, amount) == True:
                confirm = "Congrats! you have bought "+str(amount)+ " " + coin + " at a current market price of " + str(price) + " USD"
                
                await send(confirm)
                
            else: 
                await send("Purchase could not be made : Insufficient funds")
                
        if msg.startswith('$sell'):
            mean = makeSale(userID, price, coin, amount)
        
            confirm = "You have sold "+str(amount)+ " " + coin + " at a current market price of " + str(price) + " USD"
            profits = f"Your profits have been: {price - mean}$" 
            await send(confirm)
            await send(profits)
            

        
        
    elif msg.lower() == "$view":
        bal = viewFunds(userID)
        heldCrypto = viewHeld(userID)
        held = ''
        
        for key, value in heldCrypto.items():
            held += str(f'\n{value} : {key}')   
        #held = str(viewHeld(user ID))
        await send(f'Hello {userID},\nYour current balance is {round(bal, 2)}$')
        # for loop of length of amount of crypto in which the lenght 
        await send(f"You currently hold {held}")
        
                
    elif msg.startswith("$deposit"):
        
        await send(f'Success! Your new balance is: {deposit(userID, float(qty))}')
    
    
    else:
        await send("Please bless me with a valid command or type '$help' for a list of commands")




#Secret stuff
dotenv_path = join(dirname(__file__), 'trade.env')
load_dotenv(dotenv_path)
discordToken = os.environ.get('TOKEN')

#run bot
client.run(discordToken) 