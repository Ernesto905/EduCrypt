import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from os.path import join, dirname
import json
import time
from pycoingecko import CoinGeckoAPI
import traceback
import sys
cg = CoinGeckoAPI()
def retAllCrypto():
    data = cg.get_coins_list()
    
    ls = []
    for i in data:
        ls.append(i['id'])
    
    return ls
def verifyCrypto(crypto):
    if crypto in retAllCrypto(): 
        return True
    else: 
        return False

dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

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
    if verifyCrypto(arguments[3]):
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
    else: 
        await ctx.send("Ticker Not Good")

@client.command()
async def buy(ctx):
    channel = ctx.message.channel
    try:
            with open(f"NFT SYSTEM/data/{channel}-data.json", 'r') as data_json:
                    data = json.load(data_json)
                    data_json.close()
                
            seller = data["user"]
            title = data["nft-title"]
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
                            # print(member.name+"#"+member.discriminator)
 
                        # json_path = os.path.join(os.path.dirname(__file__), 'test.json')
                        # with open(json_path, 'r') as f:
                        #     data = json.load(f)
                        #     dictionary = data[member.name+"#"+member.discriminator]["cryptoHeld"][ticker]
                        #     for key in dictionary:
                        #         print (f"key: {key}, value: {dictionary[key]}")
                        #         new__balance = float(key) + 1/price * 100
                        #         key = str(new__balance)
                        #Update DB Here, give 1% of transaction to miners and deduct the buyers balance + increase the seller's balance. Also have a record for the nft.
            channel = client.get_channel(914508940186894397)
            await channel.send(f"{buyer} now owns {title}")
            await channel.send(f"{buyer} gave {price}{ticker} to {seller}")

    except Exception: 
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        await ctx.send("No, Such NFT exists, or you are messaging, in the wrong channel, please message in a channel under the 'NFT-TRADING' category, if the problem persists tag server admins.")

client.run(discordToken)
