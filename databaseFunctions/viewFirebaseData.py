from os import link
from firebase import firebase
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
import time
import datetime
import pandas as pd
import numpy as np


#initializing the app
firebase=firebase.FirebaseApplication("https://chatapp-6c060-default-rtdb.firebaseio.com/",None)



def checkIfEmailExist(email):
    try:
        result=firebase.get('/clientDetails','')
        data=pd.DataFrame(result)
        data=data.T
        data=data[data["emailId"]==email]
        #print(data)
        if data.empty==True:
            return False
        else:
            for i in data.index:
                return data["balance"][i]
    except:
         return False   
    
        
        
def listofAllPreviosPsychologist(email):
    try:
        result=firebase.get('/ongoingSession','')
        data=pd.DataFrame(result)
        data=data.T
        data=data[data["clientid"]==email]

        if data.empty==True:
            return False
        else:
            for i in data.index:
                return data["Psychologistid"][i]   
    except:
        result=list()
        return result               
        

def checkRequest(email):
    try:
        result=firebase.get('/requestList','')
        data=pd.DataFrame(result)
        data=data.T
        data=data[data["listnerId"]==email]

        print("data")
        print(data)

        if data.empty==True:
            return "False"
        else:
            for i in data.index:
                return data["clientid"][i] 
    except:
        return "False"          



def ifListnerExist(email):
    result=firebase.get('/listnerDetails','')
    data=pd.DataFrame(result)
    data=data.T
    data=data[data["emailId"]==email]
    if data.empty==True:
        return False
    else:
        return True



def listAllAvailableOnline():
    result=firebase.get('/onlineavailable','')
    data=pd.DataFrame(result)
    data=data.T
    
    availableList=list()
    
    try:
        for val in data['emailId']:
            availableList.append(val)
        
        return availableList
    except: 
         return availableList




def AllListnerDetails():
    result=firebase.get('/listnerDetails','')
    data=pd.DataFrame(result)
    data=data.T
    
    available=listAllAvailableOnline()
    
    result=list()
    for i in range(0,len(data)):
        result.append(list(data.iloc[i].values))
        
        if result[i][2] in available:
            result[i].append("Active")
        else:
            result[i].append("Not Active")
        
    return result    


def checkCLientRequest(email):  
    try:
        result=firebase.get('/requestList','')
        data=pd.DataFrame(result)
        data=data.T
        result=list()  
        data=data[data["clientid"]==email]
        return data['status'].values[0]
    except:
        return "deleted"


def listnerForClient(emailid):
    result=firebase.get('/requestList','')
    data=pd.DataFrame(result)
    data=data.T
    data=data[data["clientid"]==emailid]
    return data["listnerId"].values[0]




def listnerName(email):
    result=firebase.get('/listnerDetails','')
    data=pd.DataFrame(result)
    data=data.T
    data=data[data["emailId"]==email]
    return (data["name"].values[0])


def clientForListner(emailid):
    result=firebase.get('/requestList','')
    data=pd.DataFrame(result)
    data=data.T
    data=data[data["listnerId"]==emailid]
    return data["clientid"].values[0]


    

def updateStatusToJoining(listnerId):
    result=firebase.get('/requestList','')  
    ddata=pd.DataFrame(result)
    ddata=ddata.T
    data1=ddata[ddata["listnerId"]==listnerId]
    print(data1)
    data1=list(data1.index)
    for i in data1:
            result=firebase.put('/requestList/{}'.format(i),"status",'Accepted')