import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from os.path import join, dirname, abspath
import json
import time

client = discord.Client()







    
    
@client.event
async def on_ready():
   print("Bot has been loaded")
   channel = client.channel.id
   print(channel)
   send_message.start()
   


@client.event
async def on_message(message):
    if message.author == client.user:
        return


@tasks.loop(seconds=5 )
async def send_message():
    await client.get_channel(channel).send("message")

#Secret stuff
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
discordToken = os.environ.get('TOKEN')

client.run(discordToken)