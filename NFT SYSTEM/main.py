import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from os.path import join, dirname
import json
import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

discordToken = os.environ.get('discordToken')

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print(f"Succesfully Logged in as {client.user}")

@client.command()
async def helpme(ctx):
    await ctx.send('List of commands:\n\n1./sell "title {fileurl} price crypto-ticker" (to sell an nft, to know what are crypto tickers use the /tickers command.)\n\n2. /buy {nft-id} (to buy an nft)\n\n3. /change-role {desired roll} (change role, from user to miner or from miner to user)\n\n')

@client.command()
async def tickers(ctx):
    await ctx.send('What are crypto tickers?\n\n A: In essence, a ticker symbol is the short combination of letters that is used to represent an asset, stock, or cryptocurrency token on various exchanges, swapping services, and other DeFi solutions. For example, Bitcoin’s ticker symbol is BTC, while Ethereum’s ticker symbol is ETH. \n\n List of crypto tickers can be found here: https://coinmarketcap.com/all/views/all/')

@client.command()
async def sell(ctx, *, args):
    await client.wait_until_ready()
    guild = ctx.guild
    arguments = args.split()
    channelName = f'{arguments[0]}-NFT'
    category = discord.utils.get(ctx.guild.categories, name="nft-trading")
    await guild.create_text_channel(channelName, category=category)
    channel = discord.utils.get(ctx.guild.channels, name=channelName.lower())
    channel_id = channel.id
    msg_channel = client.get_channel(int(channel_id))
    
    await ctx.send(f"Now You @everyone can buy this nft at #{channelName.lower()}")
    await msg_channel.send(f"{ctx.author} has offered {arguments[0]} at the price of {arguments[2]} {arguments[3]}.\n File URL: {arguments[1]}")

    data = {"user": f"{ctx.author}", "nft-title":arguments[0], "file-url":arguments[1], "price":arguments[2], "ticker":arguments[3]}

    with open(f"NFT SYSTEM/data/{channelName.lower()}-data.json", 'w') as data_json:
        json.dump(data, data_json)
    print(f"{ctx.author} has sucessfully sold the nft of {arguments[0]}")

@client.command()
async def buy(ctx):
    channel = ctx.message.channel
    try:
        with open(f"NFT SYSTEM/data/{channel}-data.json", 'r') as data_json:
            data = json.load(data_json)
            data_json.close()
        
        seller = data["user"]
        title = data["title"]
        file_url = data["file-url"]
        price = data["price"]
        ticker = data["ticker"]
        buyer = ctx.author

        role = discord.utils.find(lambda r: r.name == 'miner', ctx.message.guild.roles)
        ID = ctx.message.guild.id
        guild = client.get_guild(ID)
        memberList = list(guild.members)
        for member in memberList:
                if role in member.roles:
                    user = client.get_user(member.id)
                    await user.send('Processing Transaction')
                    time.sleep(2)
                    await user.send('Transaction Processed Succesfully')
                with open (".../TRADING SYSTEM/accounts.json", "r") as account_data:
                    data = json.load(account_data)
                    data["cryptoheld"][ticker] = 
        # os.remove(f"NFT SYSTEM/data/{channel}-data.json")
        print(member.name)
                
    except: 
        await ctx.send("No, Such NFT exists, or you are messaging, in the wrong channel, please message in a channel under the 'NFT-TRADING' category.")

client.run(discordToken)