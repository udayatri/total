from os import link
from firebase import firebase
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
import time
import datetime
import pandas as pd


#initializing the app
firebase=firebase.FirebaseApplication("https://chatapp-6c060-default-rtdb.firebaseio.com/",None)



def removeFromOnlineAvailable(email):
    result=firebase.get('/onlineavailable/','')  
    data=pd.DataFrame(result)
    data=data.T
    data_new=data[data["emailId"]==email].index
    for i in  data_new:
        result=firebase.delete('/onlineavailable/{}'.format(i),'')
        
    return    



def cancelClientRequest(clientId):
    result=firebase.get('/requestList/','')  
    data=pd.DataFrame(result)
    data=data.T
    data_new=data[data["clientid"]==clientId].index
    for i in  data_new:
        result=firebase.delete('/requestList/{}'.format(i),'')
        
    return 


def cancelListnerRequest(listnerId):
    result=firebase.get('/requestList/','')  
    data=pd.DataFrame(result)
    data=data.T
    data_new=data[data["listnerId"]==listnerId].index
    for i in  data_new:
        result=firebase.delete('/requestList/{}'.format(i),'')    
        
    return 