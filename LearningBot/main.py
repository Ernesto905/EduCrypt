import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from os.path import join, dirname
import json
import time

client = discord.Client()
json_path = join(dirname(__file__), 'userData.json')

jsonFile = open(json_path)
jsonData = json.load(jsonFile)
jsonFile.close()

def timeInterval(unit, time):
    
    hour = 3600 
    day = 86400 
    time.sleep(day)

def get_question():
    pass

def makeCurriculum(courseID):
    if courseID == 0:
        link = ("https://www.guru99.com/blockchain-tutorial.html#5")

@client.event   
async def on_ready():
    print('A wild Learning Bot appeared! His name is: {0.user}'.format(client))
    



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content
    send = message.channel.send
    
    if msg == "!register":
        lings 
        await send(f"Welcome to EduCrypt! {message.author}, we have hand picked the following lectures and quizzes to meet your educational goals.\nPlease proceed to the following link")
        await send("https://www.guru99.com/blockchain-tutorial.html#5")
        await send("Estimated time of completion: 45 minutes")
    
   




#Secret stuff
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
discordToken = os.environ.get('TOKEN')

client.run(discordToken)