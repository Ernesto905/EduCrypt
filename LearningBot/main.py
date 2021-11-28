import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from os.path import join, dirname
import json
import time
import asyncio
import pymongo

#Database configuration
conn_str = "mongodb+srv://Ernesto905:mypassword@cluster0.h8feh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DBclient = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=10000)
myDB = DBclient["EducryptDatabase"]["learningBot"]
myPrefDB = DBclient["EducryptDatabase"]["preferences"]

global userInfo
userInfo = {}



# for category,entry in userInfo.items():
#     if category == "discord":
#         print(entry) 
# fileData = myDB.find({"_id": "accounts"})[0]
#collection = db.tradingBot


client = discord.Client()

jsonData1 = myDB.find({"_id": "Test1"})[0]
jsonData2 = myDB.find({"_id": "Test2"})[0]

global completed
global counter
global extra
global numCorrect
global correct_ans

completed = False

counter = 0
numCorrect = 0

# async def hello():
#     print('Hello ...')
#     await asyncio.sleep(5)
#     print('... World!')
# async def main():
#     asyncio.create_task(hello())
#     await asyncio.sleep(1)
#     print("it works!!!")

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


# async def timeInterval(elapse):
    
#     if elapse == 'daily':
def time_Interval(timeinterval):
    if timeinterval == "seconds":
        time.sleep(6)
    if timeinterval == "daily":
        time.sleep(86400)
    if timeinterval == "12hrs":
        time.sleep(43200)
    if timeinterval == "weekly":
        time.sleep(86400*7)
    if timeinterval == "weekly2":
        time.sleep(43200*7)
    return

#     if elapse == '12hrs':

#function to write into json file

    
#loop through question list and check if question is Done or not. If done then skip else return it's information in the form of a dictionary
def get_questionData(currentData):
    
    
    questionOpt = []
    for key, value in currentData.items():
        if currentData[key] != 'Test1' and currentData[key] != 'Test2':
            for isDone, answer in currentData[key].items():
                
                if isDone == "Not Done":
                    
                    for j, k in answer.items():
                        for i,m in k.items():
                            questionOpt.append(i)

                    return answer, key, questionOpt
                else:
                    break

def resetJson(currentData):
    for key, value in currentData.items():
        if currentData[key] != 'Test1' and currentData[key] != 'Test2':
            for isDone, answer in currentData[key].items():
                
                if isDone == "Done":    
                    #Marks question as displayed
                    entry = {"Not Done" : answer}
                    currentData[key] = entry
                
    
    
#function to check if answer is correct. returns correct answer
def ret_answer(q):
    for answerLetter, optionAndCorrect in q.items():
        for option, correctNess in optionAndCorrect.items():
            if correctNess == "correct":
                return answerLetter

def advance(currentData):
    
    for key, value in currentData.items():
        if currentData[key] != 'Test1' and currentData[key] != 'Test2':
            for isDone, answer in currentData[key].items():
                if isDone == "Not Done":
                    
                    #Marks question as displayed
                    entry = {"Done" : answer}
                    currentData[key] = entry
                    
                    return
    
#checks what curriculum and thus learning materials user willl use. This will return the json file to loop through
def makeCurriculum(user):
    userInfo = myPrefDB.find({"_id" : str(user)})[0]
    
    discordID = userInfo["discord"]
    name = userInfo["name"]
    timeInterval = userInfo["interval"]
    course = userInfo["course"]
    if course == "Blockchain" and completed == True: course = "NFT"
    if course == "NFT" and completed == True: course = "Blockchain"
    
    if course == "Blockchain":
        link1 = "https://www.guru99.com/blockchain-tutorial.html#5"
        link2 = ''
        link3 = ''
        correctJsonData = jsonData1
        #imagePath = join(dirname(__file__), 'Blockchain.png')
        
    if course == "NFT":
        link1 = "https://ethereum.org/en/developers/tutorials/how-to-write-and-deploy-an-nft/", 
        link2 = "https://ethereum.org/en/developers/tutorials/how-to-mint-an-nft/", 
        link3 = "https://ethereum.org/en/developers/tutorials/how-to-view-nft-in-metamask/"
        correctJsonData = jsonData2
        
         
    return correctJsonData, link1, link2, link3, timeInterval
    
# def create_IMG_Path(courseID):
#     if courseID == 0:
#         imagePath = join(dirname(__file__), 'Blockchain.png')
#     if courseID == 1:
#         imagePath = join(dirname(__file__), 'NFT.png')
#     return imagePath   

#image Path
# imagePath = create_IMG_Path(0)
 
@client.event   
async def on_ready():
    print('A wild Learning Bot appeared! His name is: {0.user}'.format(client))
    


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    global counter
    global correct_ans
    global numCorrect
    
    global correct_ans
    global currentData
    
    msg = message.content
    send = message.channel.send
    
    
    
    if msg == "Begin!":
        currentData, link1, link2, link3, timeInt = makeCurriculum(message.author)
        resetJson(currentData)
        correct_ans = ''
        counter += 1
        
        await send(f"Welcome to EduCrypt! {message.author}, we have hand picked the following lectures and quizzes to meet your educational goals.\nPlease proceed to the following link(s)")
        if link3 != '':
            await send(link3)
        if link2 != '':
            await send(link2)
        await send(link1)
        await send("Estimated time of completion: 45 minutes")
        
        time_Interval(timeInt) #Placeholder time interval for now
        
        await send("It has been 45 minutes")
        await send(f'Quiz Time!\n------------\nPlease type your answer in the following example format : ".A"')
        
    
    if counter == 0: await send("Please type 'Begin!' to recieve your first learning resource!")
        
    if counter == 1: 
         
        questionData, actualQuestion, actualOptions = get_questionData(currentData)
        
        #ask question and ask to input answer
        
        await send(f"{counter}. {actualQuestion}")
        await send(f"A : {actualOptions[0]}\nB : {actualOptions[1]}\nC : {actualOptions[2]}\nD : {actualOptions[3]}")
        
        
        
        
        
        
    if counter == 2 or counter == 3 or counter == 4 or counter == 5 or counter == 6:   
        
        questionData, actualQuestion, actualOptions = get_questionData(currentData) 
        correct_ans = ret_answer(questionData)
        
        print(f"Current correct is {correct_ans}")
        print(f"You chose: {msg[1]}")
        
        if msg[1] == "A" or msg[1] =="B" or msg[1]=="C" or msg[1]=="D":  
            if counter == 2:
                if msg[1] == str(correct_ans): numCorrect +=1  
            if counter == 3:
                if msg[1] == str(correct_ans): numCorrect +=1
            if counter == 4:
                if msg[1] == str(correct_ans): numCorrect +=1
            if counter == 5:
                if msg[1] == str(correct_ans): numCorrect +=1
            if counter == 6:
                if msg[1] == str(correct_ans): numCorrect +=1
            advance(currentData)
            if counter == 5:
                
                questionData, actualQuestion, actualOptions = get_questionData(currentData)
                correct_ans = ret_answer(questionData)
                #await send(file=discord.File(imagePath))
                await send(f"{counter}. {actualQuestion}")
                await send(f"A : {actualOptions[0]}\nB : {actualOptions[1]}\nC : {actualOptions[2]}\nD : {actualOptions[3]}")
                counter += 1
            elif counter != 6:
                questionData, actualQuestion, actualOptions = get_questionData(currentData)
                correct_ans = ret_answer(questionData)
                await send(f"{counter}. {actualQuestion}")
                await send(f"A : {actualOptions[0]}\nB : {actualOptions[1]}\nC : {actualOptions[2]}\nD : {actualOptions[3]}")
                counter += 1
            
            
            else: counter += 1

        
    if counter == 1 : counter +=1   #this is weird, just disregard me
    if counter == 7:
        completed = True
        counter += 1
        await send(f"Your total score has been {numCorrect}/5")
        if numCorrect != 5:
            await send(f'No worries! Crypto is a tricky beast. Feel free to input ".Reset" to reset your answer choices and try again! Remember, Practice makes perfect!')
        if numCorrect == 5:
            await send("Congrats on scoring 100% ! Here's a bonus video to feed your hungry mind!")
            await send("https://www.youtube.com/watch?v=9oERTH9Bkw0&t=7668s")
         
    

    if msg == ".Reset":
        resetJson(currentData)
        counter = 0
        numCorrect = 0
        await send("Questions Reset! Please input 'Begin!' to get started")
        
    if completed == True:
        currentData, link1, link2, link3, timeInt = makeCurriculum(message.author)
        time_Interval(timeInt)
        resetJson(currentData)
        correct_ans = ''
        counter += 1
        
        await send(f"Congratulations {message.author}, You are now ready for the next step in your learning journey.\nPlease proceed to the following link(s)")
        if link3 != '':
            await send(link3)
        if link2 != '':
            await send(link2)
        await send(link1)
        await send("Estimated time of completion: 45 minutes")
        
        time_Interval(timeInt) #Placeholder time interval for now
        
        await send("It has been 45 minutes")
        await send(f'Quiz Time!\n------------\nPlease type your answer in the following example format : ".A"')

#Secret stuff
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
discordToken = os.environ.get('TOKEN')

client.run(discordToken)