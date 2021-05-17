from django.shortcuts import render
from datetime import datetime
from plyer import notification # pip install plyer
import pyttsx3 # pip3 install pyttsx3
import time
import threading
import ast
# Create your views here.

current_time=''
title=''
voices = 'Female'
voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
updateReminder=[]
Reminder=[]
displayReminder=[]
showReminder=[]
today_tasks=[]

def presentTime():
    now = datetime.now()
    global current_time
    current_time_date = now.strftime("%H:%M")
    now_time = datetime.strptime(current_time_date, '%H:%M') # convert time datatype string to date
    current_time = now_time.strftime("%I:%M %p") # string to date
    if current_time == '12:00 AM':
        currentDate()
presentTime()

def currentDate():
    today = datetime.today()
    global todayDate
    todayDate = today.strftime("%d-%m-%Y")
currentDate()

def home(req):
    return render(req, "index.html")


def addReminder(request):
    global name, title
    name = request.POST['your_email'] # user name
    title = request.POST['phone'] # reminder name
    when = request.POST['first-name'] # date for reminder
    reminderTime = request.POST['last-name'] # time for reminder
    
    # change date datatype and format
    convertToDate = datetime.strptime(when, '%Y-%m-%d')
    remindetDate = convertToDate.strftime('%d-%m-%Y')

    # change time datatype and format
    string_to_date = datetime.strptime(reminderTime, '%H:%M') # convert time datatype string to date
    at = string_to_date.strftime("%I:%M %p") # convert 24 hours into 12 hours and convert datatype to string of time
    
    # set values in dictionary
    temp = {'time': at, 'title': title, 'date': remindetDate}
    
    # if temp is not exist append updateReminder
    global updateReminder
    if temp not in updateReminder:
        updateReminder.append(temp) # store dictionary into list

    # sorting updateReminder
    global Reminder
    Reminder = sorted(updateReminder, key=lambda row: (row['date'], row['time'])) 
    
    display() # display into html template
    
    threading.Thread(target=todayTask).start() # call todayTask()
    
    return render(request, "index.html", {"title":title, "when":remindetDate, "at":at, "reminder":displayReminder})

def chooseVoice(req):
    global voices
    global voice_id
    voices = req.POST['gender']
    if voices == 'Female':
        voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
    elif voices == 'Male':
        voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    return render(req, "index.html", {"title":title, "reminder":displayReminder})

def deleteReminder(req):
    t = req.POST['delrem'] # call on delete button & get deleted value
    delrem=ast.literal_eval(t)
    for i in range(len(displayReminder)):
        if displayReminder[i] == delrem:
            del displayReminder[i]
            break
    for i in range(len(showReminder)):
        if showReminder[i] == delrem:
            del showReminder[i]
            break
    for i in range(len(updateReminder)):
        if updateReminder[i] == delrem:
            del updateReminder[i]
            break
    for i in range(len(Reminder)):
        if Reminder[i] == delrem:
            del Reminder[i]
            break
    for i in range(len(today_tasks)):
        if today_tasks[i] == delrem:
            del today_tasks[i]
            break
    return render(req, "index.html", {"title":title, "reminder":displayReminder})

def display():
    for i in Reminder:
        if not i in showReminder:
            showReminder.append(i)
    global displayReminder
    displayReminder = sorted(showReminder, key=lambda row: (row['date'], row['time'])) 

def todayTask():
    currentDate()
    global today_tasks
    today_tasks = [task for task in Reminder if task["date"] == todayDate]
   
    if len(today_tasks)>0:
        threading.Thread(target=todayReminder()).start()

def removeFromUpdateReminder(visitedTime, VisitedTitle, visitedDate):
    for i in range(len(updateReminder)): 
        if updateReminder[i]['time'] == visitedTime and updateReminder[i]['title'] == VisitedTitle and updateReminder[i]['date'] == visitedDate: 
            del updateReminder[i]
            break

def todayReminder():
    for i in range(len(today_tasks)):
        presentTime()
        print(i)
        while today_tasks[i]['time'] != current_time:
            presentTime()
        if today_tasks[i]['time'] == current_time:
            msg =  today_tasks[i]['title']
            talk="hey " + name + ", please " + msg + ", its " + today_tasks[i]['time'] + "."
            threading.Thread(target=talkNotification(talk, msg)).start()
            removeFromUpdateReminder(today_tasks[i]['time'], today_tasks[i]['title'], today_tasks[i]['date'])

def talkNotification(talk, msg):
    engine = pyttsx3.init()
    notification.notify(title=msg, message=" ", timeout=10)
    engine.setProperty('voice', voice_id)
    engine.say(talk)  
    engine.runAndWait()
