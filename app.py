from flask import Flask,session,render_template,request,redirect, url_for,send_file,jsonify
import databaseFunctions.createFirebaseData as inst 
import databaseFunctions.viewFirebaseData as vwdt 
import databaseFunctions.deleteFirebaseData as dlt 
from flask_socketio import SocketIO, join_room, leave_room, emit

from flask_session import Session


app = Flask(__name__) #create a flask object
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)


Session(app)
socketio = SocketIO(app, manage_session=False)



#clientside login
@app.route('/clientlogin')
def login():
    return render_template('clientLogin.html') 


#clientemail
@app.route('/clientformvalues',methods=["POST"])
def clientformvalues():
    email=request.values.get('email')
    print(email)
    session['cemail']=email
    session['who']='client'
    return  checkingClinet(email)



@app.route('/client/<email>')
def checkingClinet(email):
    avail=vwdt.checkIfEmailExist(email)
    if avail==False:
        inst.clientDetails(email)
        balance=0
    else:
        pass
        #balance=avail
        #pychologistList=vwdt.listofAllPreviosPsychologist(email) #will contain list of dates and names 

    pychologistList=vwdt.AllListnerDetails()
    print(pychologistList)
    return render_template('cadleyIntegration.html',balance=0,pychologistList=pychologistList)


@app.route('/sendrequest/<email>')
def creatingRequest(email):
    print(session['cemail'])
    inst.requestList(session['cemail'],email,'Requested')
    return render_template('waitingforrequest.html')

@app.route('/request/status/<email>')
def checkingRequest(email):
    return checkStatusOfRequest(email)


@app.route('/request/accepted')
def creatingRoom():
    email=vwdt.listnerForClient(session['cemail'])
    roomname= session['cemail'] + str(email)
    session['username'] = 'ABC'
    session['room'] = roomname
    return render_template('chat.html', session = session,email=session['cemail'],Name='ABC ')

@app.route('/deleteRequest/<clientName>', methods=['GET', 'POST'])
def deleteRequest(clientName):
    dlt.cancelClientRequest(clientName) 
    return jsonify({'data': 'delete'})


@app.route('/cancelClientRequest')
def cancelCltRequest():
    print(session['cemail'])
    return checkingClinet(session['cemail'])



#listnerside

@app.route('/lister/login')
def homeListner():
    return render_template('listnerLogin.html') 
    

#listneremail
@app.route('/listnerformvalues',methods=["POST"])
def listnerformvalues():
    email=request.values.get('email')
    session['cemail']=email
    session['who']='client'
    return  checkingListner(email)

@app.route('/listner/<email>')
def checkingListner(email):
    session['lemail']=email
    session['who']='listner'

    if vwdt.ifListnerExist(email)==True:
       inst.onlineavaible(email)
       return render_template('listnerDashboard.html',name=email,email=email)

    return "wrong entry"    


@app.route('/checkrequestforme/email')
def checkrequestform(email):
    val=vwdt.checkRequest(email)
    if val==False:
        return val
    else:
        "send request to join chat channel"    
        roomname= session['email'] + str(email)
        session['username'] = session['email']
        session['room'] = roomname
        dlt.removeFromOnlineAvailable(session['email'])
        return render_template('chat.html', session = session,email=session['email'],Name=session['email'])



@app.route('/requestaccepted/<email>')
def requestaccepted(email):
    clinetId=vwdt.clientForListner(email)
    ListnerId=email
    vwdt.updateStatusToJoining(email)
    name=vwdt.listnerName(email)
    roomname= clinetId + ListnerId
    return render_template('index.html',name=name,roomname=roomname)





##### admin side

@app.route('/addingListnerdetails')
def addingCaledlydetails():
    return render_template("admin/listnerAddition.html")

@app.route('/addingListnerInfo',methods=["POST"])
def addingCalendlyUrlInfo():
    name=request.values.get('name')
    emailId=request.values.get('email')
    contact=request.values.get('contact')
    imageName=request.values.get('imageName')
    description=request.values.get('Description')
    Type=request.values.get('Type')

    inst.listnerDetails(name,contact,emailId,description,imageName,'0')
    return "Done"







####

@app.route("/changestatus/<status>/<email>", methods=['GET', 'POST'])
def changestatus(status,email):
    if status=='available':
        inst.onlineavaible(email)
        return jsonify({'data': 'added'})
    else:
        dlt.removeFromOnlineAvailable(email)    
        return jsonify({'data': 'delete'})







@app.route('/val/<name>/<roomname>', methods=['GET', 'POST'])
def index(name,roomname):
    return render_template('index.html',name=name,roomname=roomname)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session,email=session['lemail'],Name=username)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session,email=session['lemail'],Name=username)
        else:
            return redirect(url_for('index'))

@app.route('/leaveChat', methods=['GET', 'POST'])
def leaveChat():
    try :    
        if session['who']=='client':
            return url_for(checkingClinet(session['cemail'])) 
        else:    
            return url_for(checkingListner(session['lemail']))
    except:
      return "No email found"


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    #vwdt.insertmessage(session.get('username'),message['msg'])
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg'] +"\\n"}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)



@app.route('/listnerstatus_update', methods=['POST'])
def listnerstatus_update():

    currentOnline=vwdt.listAllAvailableOnline()
    try:
        if currentOnline==session['previousOnline']:
            return jsonify({'data': 'nochange'})
        else:
            toggels = [i for i in currentOnline + session['previousOnline'] if i not in currentOnline or i not in session['previousOnline']] 
            session['previousOnline']=currentOnline
            return jsonify({'data': toggels})
    except:
        session['previousOnline']=list()     
        return jsonify({'data': currentOnline})


    return jsonify({'data': 'ABC'})
    #return jsonify({'data': render_template('response.html', batch_list=batch_list)})


@app.route('/requestUpdate/<email>', methods=['POST'])
def requestUpdate(email):
    result=vwdt.checkRequest(email)

    return jsonify({'data': result})


@app.route('/clinetRequestUpdate/', methods=['POST'])
def clinetCequestUpdate():
    email=session['cemail']
    result=vwdt.checkCLientRequest(email)  ## edit this

    print("result  :",result)
    return jsonify({'data': result})




if __name__ == '__main__':
    socketio.run(app) #debug enabled is creating warning and error

