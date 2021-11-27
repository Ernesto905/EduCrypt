import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from os.path import join, dirname
import json
import time

#global count used to loop through questions


client = discord.Client()

#different json datas
json_path1 = join(dirname(__file__), 'Test1.json')
jsonFile1 = open(json_path1)
jsonData1 = json.load(jsonFile1)
jsonFile1.close()

#different json datas
json_path2 = join(dirname(__file__), 'Test2.json')
jsonFile2 = open(json_path2)
jsonData2 = json.load(jsonFile2)
jsonFile2.close()

global counter
global numCorrect
global correct_ans

counter = 0
numCorrect = 0


def timeInterval(elapse):
    if elapse == "day": gap = 86400
    if elapse == "45" : gap = 2700
    if elapse == "30" : gap = 1800
    
    time.sleep(2)

#function to write into json file
def write_to(currentData, currentPath):
    jsonFile = open(currentPath, "w")
    json.dump(currentData, jsonFile)
    jsonFile.close()
    
#loop through question list and check if question is Done or not. If done then skip else return it's information in the form of a dictionary
def get_questionData(currentData, currentPath):
    
    
    questionOpt = []
    for key, value in currentData.items():
        for isDone, answer in currentData[key].items():
            if isDone == "Not Done":
                
                
                
                for j, k in answer.items():
                    for i,m in k.items():
                        questionOpt.append(i)
                
                #print(f"The current answer value is: {answer}")
                
                return answer, key, questionOpt
            else:
                break

def resetJson(currentData, currentPath):
    for key, value in currentData.items():
        for isDone, answer in currentData[key].items():
            if isDone == "Done":
                
                #Marks question as displayed
                entry = {"Not Done" : answer}
                currentData[key] = entry
                
                write_to(currentData, currentPath)
    
#function to check if answer is correct. returns correct answer
def ret_answer(q):
    for answerLetter, optionAndCorrect in q.items():
        for option, correctNess in optionAndCorrect.items():
            if correctNess == "correct":
                return answerLetter

def advance(currentData, currentPath):
    
    for key, value in currentData.items():
        for isDone, answer in currentData[key].items():
            if isDone == "Not Done":
                
                #Marks question as displayed
                entry = {"Done" : answer}
                currentData[key] = entry
                write_to(currentData, currentPath)
                return
    
#checks what curriculum and thus learning materials user willl use. This will return the json file to loop through
def makeCurriculum(courseID):
    if courseID == 0:
        link = ("https://www.guru99.com/blockchain-tutorial.html#5")
        correctJsonData = jsonData1
        correctJsonPath = json_path1
        return correctJsonData, correctJsonPath

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
    global currentPath
    msg = message.content
    send = message.channel.send
    
    
    
    if msg == "Begin!":
        currentData, currentPath = makeCurriculum(0)
        
        correct_ans = ''
        counter += 1
        
        
        await send(f"Welcome to EduCrypt! {message.author}, we have hand picked the following lectures and quizzes to meet your educational goals.\nPlease proceed to the following link")
        await send("https://www.guru99.com/blockchain-tutorial.html#5")
        await send("Estimated time of completion: 45 minutes")
        
        timeInterval(1) #Placeholder time interval for now
        
        await send("It has been 45 minutes")
        await send(f'Quiz Time!\n------------\nPlease type your answer in the following example format : ".A"')
        
    
    if counter == 0: await send("Please type 'Begin!' to recieve your first learning resource!")
        
    if counter == 1 or counter == 2 or counter == 3 or counter == 4 : 
         
        questionData, actualQuestion, actualOptions = get_questionData(currentData, currentPath)

        #ask question and ask to input answer
        await send(f"{counter}. {actualQuestion}")
        await send(f"A : {actualOptions[0]}\nB : {actualOptions[1]}\nC : {actualOptions[2]}\nD : {actualOptions[3]}")
        
        
        
        
        
        
        
    if counter == 2 or counter == 3 or counter == 4 or counter == 5:   
         #returns three things. First, key value question in question. Second, the actual question being asked in plaintext form. Third, the actual answers in the form of a list
        questionData, actualQuestion, actualOptions = get_questionData(currentData, currentPath) 
        correct_ans = ret_answer(questionData)
        
        print(f"Current correct is {correct_ans}")
        print(f"You chose: {msg[1]}")
        
        if msg[1] == "A" or msg[1] =="B" or msg[1]=="C" or msg[1]=="D":  
            if counter == 2:
                if msg[1] == str(correct_ans): 
                    numCorrect +=1
                     
            if counter == 3:
                if msg[1] == str(correct_ans): numCorrect +=1
            if counter == 4:
                if msg[1] == str(correct_ans): numCorrect +=1
            if counter == 5:
                if msg[1] == str(correct_ans): numCorrect +=1
            advance(currentData, currentPath)   
            counter += 1

        
    if counter == 1 : counter +=1   #this is weird, just disregard me
    if counter == 6:
        await send(f"Your total score has been {numCorrect}/4")     
    
    #else:
        #await send("Are you ready to begin? Type 'Begin!' whenever you feel ready to start your journey")
        #await send (f"You have scored {numCorrect} out of 4")
   

    if msg == ".Reset":
        resetJson(currentData, currentPath)
        await send("Questions Reset! Please input 'Begin!' to get started")

#Secret stuff
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
discordToken = os.environ.get('TOKEN')

client.run(discordToken)