from os import link
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
import time
from numpy.lib.function_base import blackman
import datetime
import pandas as pd

 
#creating service account key
 #initializing the app
firebase=firebase.FirebaseApplication("https://chatapp-6c060-default-rtdb.firebaseio.com/",None)




def clientDetails(emailId):
 tableNew1={
     'emailId':emailId,
     'balance':'0'
 }
 result=firebase.post('/clientDetails',tableNew1)



def listnerDetails(name,contact,emailId,description,image,sessionconduted):
 tableNew1={
     'name':name,
     'contact':contact,
     "emailId":emailId,
     "description":description,
     "image":image,
     "sessionconduted":sessionconduted,
 }
 result=firebase.post('/listnerDetails',tableNew1)




def messageLog(incomingMessageId,outgoingMesageId,Value):
 tableNew1={
     "msgTime":datetime.datetime.now(),
     "incomingMessageId":incomingMessageId,
     "outgoingMesageId":outgoingMesageId,
     "Value":Value
 }
 result=firebase.post('/messageLog',tableNew1)
 
 
def requestList(clientId,listnerId,status):
 try:   
     result=firebase.get('/requestList','')
     data=pd.DataFrame(result)
     data=data.T
     data=data[(data["listnerId"]==listnerId) & (data["clientid"]==clientId)]   
     if data.empty==False:
         return
     tableNew1={
         "clientid":clientId,
         "listnerId":listnerId,
         "status":status
     }
     result=firebase.post('/requestList',tableNew1)
 except:
      tableNew1={
         "clientid":clientId,
         "listnerId":listnerId,
         "status":status
      }
      result=firebase.post('/requestList',tableNew1)
      



def ongoingSession(clientid,PsychologistId):
 tableNew1={
     "clientid":clientid,
     "Psychologistid":PsychologistId,
     "currentTime":datetime.datetime.now()
 }
 result=firebase.post('/ongoingSession',tableNew1)



def completedSession(clientid,PsychologistId,startingTime):
 tableNew1={
     "clientid":clientid,
     "Psychologistid":PsychologistId,
     "startingTime":startingTime,
     "total duration":"to be calculated"

 }
 result=firebase.post('/completedSession',tableNew1)  

 
def onlineavaible(emailId):
    result=firebase.get('/listnerDetails','')
    data=pd.DataFrame(result)
    data=data.T
    data=data[data["emailId"]==emailId]  
    
    if data.empty==False:
        return
    
    tableNew1={
             "emailId":emailId
    
    }
    result=firebase.post('/onlineavailable',tableNew1)
 

def insertmessage(name,message):
     if name=='ABC':
         messageLog(session['cemail'],session['lemail'],message)
     else:
         messageLog(session['lemail'],session['cemail'],message)    