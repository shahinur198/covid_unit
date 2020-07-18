# import pyrebase
from flask import Flask, render_template, url_for,Response, request,flash, redirect,jsonify, url_for,session,escape
import os
import time, threading
# from datetime import datetime,timedelta,date
import datetime
import numpy as np
from covid_19_db import Db
from build_query import insert_query,update_query,select_query
import json
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS,cross_origin
# from flask_moment import Moment
from werkzeug.utils import secure_filename
import uuid
import requests
from flask_session import Session
from cryptography.fernet import Fernet
import uuid
import math, random
# pip install twilio
# from twilio.rest import Client
# from flask_socketio import SocketIO, send, emit
import sqlite3
from sqlite3 import Error

# the following line needs your Twilio Account SID and Auth Token
# client = Client("ACdddae55deb998832b70b8c1239255751", "bcd140ac72427768f386f30ef55daa3e")

# from flask_talisman import Talisman, ALLOW_FROM

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Ctrl + k +1 folding

db=Db()
db.createDb()
app = Flask(__name__)
# moment = Moment(app)
cors = CORS(app)
# app.secret_key = 'super secret key'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)
api = Api(app)

# socketio = SocketIO( app )
# socket_users = {}

users = {}
def secret_key_setup():
    app.secret_key = os.urandom(32)
    # print(app.secret_key)
def app_setup():
    try:
        column_names=['key','ciphered_text','auth_id','phone_number','phone_number_verified','name',
                'gender','nid','profile_pic','district','town','village','create_date','collection','collection_number','donated','status']
        values=['','','','','1','','','','','','','',str(time.time()),'0','0','0','1']
                                           
        phone =  "01718057283"
        values[3]=phone
        password = 'admin'
        values[5] = 'root admin'
        values[6] = 'Male'
        values[9] = 'Jhenaidah'
        values[10] = 'Harinakunda'
        values[11] = 'Boalia'
       
        
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        # print(password.encode('ASCII'))
        ciphered_text = cipher_suite.encrypt(password.encode('ASCII'))   #required to be bytes
        # auth_id = uuid.uuid4()
        values[0]= key.decode('ASCII')
        values[1] = ciphered_text.decode('ASCII')
        values[2] = str(uuid.uuid4())

            

        # session['user'] = 
        db=Db()
        # column_names[1]=session['user']['localId']
        query=insert_query("tblUser",column_names,values)
        # print(query)
        user_id = db.insert_data(query)

        column_names=['user_id',
                    'admin_type',
                    'access_all',
                    'create_date',
                    'security_key',
                    'status']
        values=[str(user_id),
                    'root admin',
                    '1',
                    str(time.time()),
                    'security_key',
                    '1']


        security_key =str(len(values[0])+len(values[1])+len(values[2])+len(values[3])+len(values[5]))
        ciphered_key = cipher_suite.encrypt(security_key.encode('ASCII'))   #required to be bytes
       
        values[4] = ciphered_key.decode('ASCII')

        query=insert_query("tblAdmin",column_names,values)
        # print(query)
        admin_id = db.insert_data(query)
        secret_key_setup()

    except Exception as e:
        secret_key_setup()
        

app_setup()
def authentication():
    try:
        # print(session['login'])
        # print(session['user'])
        if session['user'] == None or len(session['user'])<=0:
            session['login'] =False
            return False
        elif session['login']==False:
            session['user'] =None
            return False
        elif session['user'][3] == 0:
            return False

    except Exception as e:
        session['login'] =False
        session['user'] = None
        session['login_user']=['',0,0,0]
        return False

    return True
    
# function to generate OTP 
def generateOTP() : 
  
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = "" 
  
   # length of password can be chaged 
   # by changing value in range 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP

def send_web_message(sender_id,receiver_id,message,root_message_id,db):
    
    column_names=['sender_id',
                    'receiver_id',
                    'message',
                    'read',
                    'important_sender',
                    'important_receiver',
                    'sending_date',
                    'sender_statu',
                    'receiver_status',
                    'root_message_id']

    values=[str(sender_id),
            str(receiver_id),
            message,
            '0',
            '0',
            '0',
            str(time.time()),
            '1',
            '1',
            str(root_message_id)]

    query=insert_query("tblWebMessage",column_names,values)
    # print(query)
    web_message_id = db.insert_data(query)

    return web_message_id

def update_web_message(web_message_id,column_names,values,db): 
    

    where_stetment="web_message_id = '"+str(web_message_id)+"'"
    query=update_query("tblWebMessage",column_names,values,where_stetment)
    
    res = db.update_data(query)

    return res

def rmqt(data):
    data=data.replace("'", "''")
    data=data.replace('"', '""')
    # print(data)
    return data

@app.teardown_appcontext
def close_connection(exception):
    # pass
    db = Db()
    if db is not None:
        db.close_db()
        print("close db")

@app.route("/")
@app.route("/index")
def index():
    # insert_query("tbl",['a','b'],['1','2'])
    if authentication()==False:
        return render_template('index.html', title='কোভিড-১৯ ইউনিট তৈরী',login_user=session['login_user'])
    return render_template('index.html', title='কোভিড-১৯ ইউনিট তৈরী',login_user=session['login_user'])

@app.route("/video_recorder")
def video_recorder():
    # insert_query("tbl",['a','b'],['1','2'])
    if authentication()==False:
        return render_template('index.html',login_user=session['login_user'])
    return render_template('video_recorder.html',login_user=session['login_user'])


@app.route("/phone_verification", methods=['GET', 'POST'])
def phone_verification():

    if session['login']==False:
        return redirect(url_for('login'))

    # print("dddddddd",session['user'])
    if session['user'][3] == 0:
        # print("request",request.method)                
        if request.method == 'POST':

            if request.form['action']=="submit":

                # try:   
                verification_code = request.form['verification_code']
                # print((time.time() - session['OTP'][1]))
                if (time.time() - session['OTP'][1])>100:
                    flash("Time out. Please re-send OTP.")
                elif verification_code == session['OTP'][0]:
                    # Update database........here....
                    column_names=['phone_number_verified']
                    values=['1']
                    where_stetment = 'user_id = '+str(session['user'][0])
                    query=update_query("tblUser",column_names,values,where_stetment)
                    # print(query)
                    db=Db()
                    res = db.update_data(query)
                    if res:
                        flash('Verification successfully')
                        lst=list(session['user'])
                        lst[3]=1
                        session['user'] = tuple(lst)
                        return redirect(url_for('index'))
                    else:
                        flash('Verification faild . Please try again.')
                    
                else:
                    flash('Verification Faild.')

            elif request.form['action']=="resend":

                flg=True
                try:
                    if (time.time() - session['OTP'][1])<100:
                        flash('Verification code already send to your phone. For new code try after few minutes.')
                        flg = False
                    elif session['OTP'][2]>3:
                        if (time.time() - session['OTP'][1])>3600:
                            session['OTP']=['OTP@',time.time(),0]
                        else:
                            flash("Please try after 1 hours.")
                            flg = False
                except Exception as e:
                    session['OTP']=['OTP@',time.time(),0]

                if flg == True:
                    OTP =generateOTP()
                    if send_code(session['user'][2],OTP)==1:
                        session['OTP']=[OTP,time.time(),(session['OTP'][2]+1)]

    else:
        # print("index...")
        return redirect(url_for('index'))

    return render_template('phone_verification.html', title='phone_verification',
        login_user=session['login_user'])

@app.route("/logout")
def logout():    
    session.clear()
    session['user']=None
    session['login'] =False
    session['login_user']=['',0,0,0]
    flash("Logout successfully.")
    return redirect(url_for('login'))

def send_code(to,OTP):

    YOUR_API_USERNAME="shahin198"
    YOUR_API_HASH_TOKEN = "6b0f49678d2d1e183f48aeb5280938bc"
    # to="01718057283"
    msg = "Your Covid-19 health care Phone Verification OTP is: "+OTP

    response = requests.get("http://alphasms.biz/index.php?app=ws&u="+YOUR_API_USERNAME+"&h="+YOUR_API_HASH_TOKEN+"&op=pv&to="+to+"&msg="+msg)
    # print(response)
    # flash(response.status_code)
    if response.status_code == 200:
        return 1

    return 0
def send_mobile_msg(to,msg):

    YOUR_API_USERNAME="shahin198"
    YOUR_API_HASH_TOKEN = "6b0f49678d2d1e183f48aeb5280938bc"
    # to="01718057283"
    # msg = "Verification form Covid-19 health care. Your OTP is "+OTP

    response = requests.get("http://alphasms.biz/index.php?app=ws&u="+YOUR_API_USERNAME+"&h="+YOUR_API_HASH_TOKEN+"&op=pv&to="+to+"&msg="+msg)
    
    print(response)
    flash(response.status_code)
    if response.status_code == 200:
        return 1

    return 0

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    try:
        if session['login']==True:
            if session['user'][3] == 0:
                return redirect(url_for('phone_verification'))
    except Exception as e:
        session['user']=None
        session['login'] =False
        session['login_user']=['',0,0,0]
    

    if request.method == 'POST':
        
        if request.form['action']=="submit":
            
            # try:   
            phone = request.form['phone']
            password = request.form['password']

            columns="key,ciphered_text,user_id ,auth_id,phone_number,phone_number_verified,name,gender,profile_pic,district,town"
            where_stetment="status = 1 AND phone_number = '"+phone+"'"
            query=select_query("tblUser",columns,where_stetment)
            # print(query)
            db=Db()
            login_data = db.get_data_by_key(query)
            # print("sss",session['user'])
            if login_data != None:

                cipher_suite = Fernet(login_data[0].encode('ASCII'))
                unciphered_text = (cipher_suite.decrypt(login_data[1].encode('ASCII')))
                # print(unciphered_text)
                if unciphered_text == password.encode('ASCII'):
                    # print(query)
                    session['user'] = login_data[2:]
                    print(session['user'])
                    session['login'] =True
                    
                    flash('Login successful')

                    columns="admin_type,access_all"
                    where_stetment="status = 1 AND user_id = '"+str(session['user'][0])+"'"
                    query=select_query("tblAdmin",columns,where_stetment)                    
                    admin_user = db.get_data_by_key(query)
                    if admin_user != None:
                        session['login_user']=[session['user'][4],1,(1+int(admin_user[1])),session['user'][0]]
                        # print(session['login_user'])
                    else:
                        session['login_user']=[session['user'][4],1,0,session['user'][0]]

                    if session['user'][3] == 0:
                        OTP =generateOTP()
                        if send_code(session['user'][2],OTP)==1:
                            session['OTP']=['OTP@',time.time(),0]
                            session['OTP']=[OTP,time.time(),(session['OTP'][2]+1)]
                            
                        return redirect(url_for('phone_verification'))
                    else:
                        return redirect(url_for('index'))
                else:
                    session['login'] =False
                    session['user'] = None
                    session['login_user']=['',0,0,0]
                    flash('Login Faild.')                    

        else:
            session['user'] =[]

    try:
        if session['login_user']:
            pass
    except Exception as e:
        session['login_user']=['',0,0,0]
    

    
    return render_template('login.html', title='ব্যবহারকারী লগ - ইন',login_user=session['login_user'])

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    db=Db()
    if request.method == 'POST':
        
        if request.form['action']=="submit":
            # try:
            column_names=['key','ciphered_text','auth_id','phone_number','phone_number_verified','name',
                'gender','nid','profile_pic','district','town','village','create_date','collection','collection_number','donated','status']
            values=['','','','','1','','','','','','','',str(time.time()),'0','0','0','1']
                                               
            phone =  request.form['phone']
            values[3]=phone
            password = request.form['password']
            repassword = request.form['repassword']
            values[5] = request.form['user_name']
            values[6] = request.form['gender']
            values[9] = request.form['district']
            town = request.form['town']
            town=town.split("_")
            values[10] = town[0]
            values[11]=request.form['village']

            if password == repassword:
                key = Fernet.generate_key()
                cipher_suite = Fernet(key)
                # print(password.encode('ASCII'))
                ciphered_text = cipher_suite.encrypt(password.encode('ASCII'))   #required to be bytes
                # auth_id = uuid.uuid4()
                values[0]= key.decode('ASCII')
                values[1] = ciphered_text.decode('ASCII')
                values[2] = str(uuid.uuid4())

                    

                # session['user'] = 
                
                # column_names[1]=session['user']['localId']
                query=insert_query("tblUser",column_names,values)
                # print(query)
                user_id = db.insert_data(query)
                # user_account_id=create_account(user_id,db)

                # columns="user_id ,'auth_id','phone_number','phone_number_verified','first_name','last_name',gender"
                # where_stetment="status = 1 AND user_id = "+str(user_id)
                # query=select_query("tblUser",columns,where_stetment)
                # session['user'] = db.get_data_by_key(query)
                # # print(session['user'])

                flash('Registration successful')

                return redirect(url_for('login'))
            else:
                flash('Password and re-password not mach.')

            # except :
            #     flash('Something wrong')

    districts = db.get_all_district()
    return render_template('registration.html', title='নিবন্ধন',districts=districts,login_user=session['login_user'])

@app.route("/hospital", methods=['GET', 'POST'])
def hospital():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key
    
    return render_template('hospital.html', title='hospital',key=key,login_user=session['login_user'])

class HospitalApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        hospital=None
        if user_key == key:
            db=Db()
            district = session['user'][7]
            town = session['user'][8]
            # print("dddddddd:",district,town)
            columns=" th.*,tu.name,tu.profile_pic,tu.phone_number "
            where_stetment="th.district = '"+district+"' AND th.town = '"+town+"'"
            join_query="tblHospital as th "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON th.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            hospital = db.get_data_by_key(query)
            code =200
            msg="successfully"

        return {'message': msg, 'hospital': hospital}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        hospital=None
        hospital_id=0
        if user_key == key:

            db=Db()
            
            if args['method']=='delete':
                hospital_id = data['hospital_id']

                columns="user_id"
                where_stetment="hospital_id = '"+str(hospital_id)+"' AND accept_proposal = 0" 
                query=select_query("tblHospital",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search != None and search[0]==user_id:                    
                    query="DELETE FROM tblHospital WHERE hospital_id = '"+str(hospital_id)+"'" 
                    msg = db.update_data(query)

            elif args['method']=='post':
                hospital_name = data['hospital_name']
                hospital_pic = data['hospital_pic']
                district = session['user'][7]
                town = session['user'][8]
                proposal = data['proposal']
                proposal_video_link = data['proposal_video_link']
                    
                columns="hospital_id"
                where_stetment="user_id = '"+str(user_id)+"'" 
                query=select_query("tblHospital",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    column_names=['user_id',
                                    'hospital_name',
                                    'hospital_pic',
                                    'district',
                                    'town',
                                    'proposal',
                                    'proposal_video_link',
                                    'facebook_group',
                                    'development_start_date',
                                    'development_end_date',
                                    'accept_date',
                                    'accept_proposal',
                                    'stop',
                                    'completed',
                                    'create_date',
                                    'status']
                    values=[str(user_id),
                            hospital_name,
                            hospital_pic,
                            district,
                            town,
                            proposal,
                            proposal_video_link,
                            '',
                            '',
                            '',
                            '',
                            '0',
                            '0',
                            '0',
                            str(time.time()),
                            '1']
                    query=insert_query("tblHospital",column_names,values)
                    # print(query)
                    hospital_id = db.insert_data(query)

                    column_names=['hospital_id',
                                    'number_of_collection',
                                    'collection',
                                    'donated',
                                    'costing',
                                    'updated_date',
                                    'create_date',
                                    'status']
                    values=[str(hospital_id),
                            '0',
                            '0',
                            '0',
                            '0',
                            str(time.time()),
                            str(time.time()),
                            '1']
                    query=insert_query("tblTotalSummary",column_names,values)
                    # print(query)
                    total_summary_id = db.insert_data(query)


            elif args['method']=='update':                
                hospital_id = data['hospital_id']

                columns="user_id"
                where_stetment="hospital_id = '"+str(hospital_id)+"'" 
                query=select_query("tblHospital",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search[0]==user_id:

                    hospital_name = data['hospital_name']
                    hospital_pic = data['hospital_pic']
                    proposal = data['proposal']
                    proposal_video_link = data['proposal_video_link']

                    column_names=['hospital_name',
                                    'hospital_pic',
                                    'proposal',
                                    'proposal_video_link',
                                    'status']
                    values=[hospital_name,
                            hospital_pic,
                            proposal,
                            proposal_video_link,
                            '1']

                    where_stetment="hospital_id = '"+str(hospital_id)+"'"
                    query=update_query("tblHospital",column_names,values,where_stetment)
                    # print(query)
                
                    res = db.update_data(query)
                
                
            
            columns=" th.*,tu.name,tu.profile_pic,tu.phone_number "
            where_stetment="th.user_id = '"+str(user_id)+"'"
            join_query="tblHospital as th "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON th.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            hospital = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': hospital}, code

api.add_resource(HospitalApi, '/hospital_api')

@app.route("/hospital_verifi", methods=['GET', 'POST'])
def hospital_verifi():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    if session['login_user'][2]<2:
        return redirect(url_for('index'))
        
    return render_template('hospital_verifi.html', title='hospital_verifi',key=key,login_user=session['login_user'])

class HospitalVerifiApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        hospitals=None
        if session['login_user'][2]<2:
            return {'message': msg, 'hospitals': hospitals}, code
        if user_key == key:
            db=Db()
            columns=" th.*,tu.name,tu.profile_pic,tu.phone_number "
            where_stetment="th.status = 1 "
            join_query="tblHospital as th "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON th.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            hospitals = db.get_data(query)
            code =200
            msg="successfully"

        return {'message': msg, 'hospitals': hospitals}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        hospital=None
        hospital_id=0
        if session['login_user'][2]<2:
            return {'message': msg, 'hospital': hospital}, code
        if user_key == key:

            db=Db()
            
            if args['method']=='accepte':                
                hospital_id = data['hospital_id']                
                facebook_group = data['facebook_group']

                column_names=['facebook_group',
                                'accept_date',
                                'accept_proposal',
                                'status']
                values=[facebook_group,
                        str(time.time()),
                        '1',
                        '1']

                where_stetment="hospital_id = '"+str(hospital_id)+"'"
                query=update_query("tblHospital",column_names,values,where_stetment)
                
                res = db.update_data(query)
            elif args['method']=='dev_start':
                hospital_id = data['hospital_id']

                column_names=['development_start_date',
                                'status']
                values=[str(time.time()),
                        '1']

                where_stetment="hospital_id = '"+str(hospital_id)+"'"
                query=update_query("tblHospital",column_names,values,where_stetment)
                
                res = db.update_data(query)

            elif args['method']=='stop':
                hospital_id = data['hospital_id'] 

                column_names=['stop',
                                'status']
                values=['1',
                        '1']

                where_stetment="hospital_id = '"+str(hospital_id)+"'"
                query=update_query("tblHospital",column_names,values,where_stetment)
                
                res = db.update_data(query)

            elif args['method']=='start_again':
                hospital_id = data['hospital_id'] 

                column_names=['stop',
                                'status']
                values=['0',
                        '1']

                where_stetment="hospital_id = '"+str(hospital_id)+"'"
                query=update_query("tblHospital",column_names,values,where_stetment)
                
                res = db.update_data(query)

            elif args['method']=='finishe':
                hospital_id = data['hospital_id']

                column_names=['completed',
                                'development_end_date',
                                'status']
                values=['1',
                        str(time.time()),
                        '1']

                where_stetment="hospital_id = '"+str(hospital_id)+"'"
                query=update_query("tblHospital",column_names,values,where_stetment)
                
                res = db.update_data(query)

            elif args['method']=='next_start':
                hospital_id = data['hospital_id']

                column_names=['completed',
                                'status']
                values=['0',
                        '1']

                where_stetment="hospital_id = '"+str(hospital_id)+"'"
                query=update_query("tblHospital",column_names,values,where_stetment)
                
                res = db.update_data(query)
            
            columns=" th.*,tu.name,tu.profile_pic,tu.phone_number "
            where_stetment="th.status = 1 AND th.hospital_id = '"+str(hospital_id)+"'"
            join_query="tblHospital as th "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON th.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            hospital = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': hospital}, code

api.add_resource(HospitalVerifiApi, '/hospital_verifi_api')

@app.route("/volunteer", methods=['GET', 'POST'])
def volunteer():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))
    
    return render_template('volunteer.html', title='স্বেচ্ছাসেবক',hospital=hospital,key=key,login_user=session['login_user'])

class VolunteerApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search', required=True)
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        volunteers=None
        volunteer=None
        search = args['search']
        search = json.loads(search)
        if user_key == key:
            db=Db()
            district = session['user'][7]
            town = session['user'][8]
            # print("dddddddd:",district,town)
            columns=" tu.name,tu.profile_pic,tu.phone_number,tv.village,tv.profession,tv.verified,tv.email_id,tv.volunteer_id "
            if search['search']==0:
                where_stetment="tv.user_id = '"+str(user_id)+"' OR th.district = '"+district+"' AND th.town = '"+town+"' AND tv.verified = 1 ORDER BY tv.create_date DESC LIMIT 50  OFFSET "+offset
            else:
                volunteer_name=search['volunteer_name']
                village=search['village']
                where_stetment="tv.user_id = '"+str(user_id)+"' OR th.district = '"+district+"' AND th.town = '"+town+"' AND tv.verified = 1 AND tu.name LIKE '"+'%'+volunteer_name+'%'+"' AND tv.village LIKE '"+'%'+village+'%'+"' ORDER BY tv.create_date DESC LIMIT 50  OFFSET "+offset
            
            
            join_query="tblVolunteer as tv "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblHospital as th ON th.hospital_id = tv.hospital_id "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON tv.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            volunteers = db.get_data(query)

            columns="*"
            where_stetment="user_id = '"+str(user_id)+"'" 
            query=select_query("tblVolunteer",columns,where_stetment)                    
            volunteer = db.get_data_by_key(query)
            code =200
            msg="successfully"

        return {'message': msg, 'volunteers': volunteers, 'volunteer': volunteer}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        volunteer=None
        volunteer_id=0
        if user_key == key:

            db=Db()
            
            if args['method']=='delete':
                volunteer_id = data['volunteer_id']

                columns="user_id"
                where_stetment="volunteer_id = '"+str(volunteer_id)+"' AND accept_proposal = 0" 
                query=select_query("tblVolunteer",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search != None and search[0]==user_id:                    
                    query="DELETE FROM tblVolunteer WHERE volunteer_id = '"+str(volunteer_id)+"'" 
                    msg = db.update_data(query)

            elif args['method']=='post':
                hospital_id = data['hospital_id']
                email_id = data['email_id']
                profession = data['profession']
                    
                columns="volunteer_id"
                where_stetment="user_id = '"+str(user_id)+"'" 
                query=select_query("tblVolunteer",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    columns="village"
                    where_stetment="user_id = '"+str(user_id)+"'" 
                    query=select_query("tblUser",columns,where_stetment)                    
                    user_village = db.get_data_by_key(query)

                    column_names=['user_id',
                                    'hospital_id',
                                    'email_id',
                                    'village',
                                    'profession',
                                    'verified',
                                    'create_date',
                                    'status']
                    values=[str(user_id),
                            hospital_id,
                            email_id,
                            user_village[0],
                            profession,
                            '0',
                            str(time.time()),
                            '1']
                    query=insert_query("tblVolunteer",column_names,values)
                    # print(query)
                    volunteer_id = db.insert_data(query)
                else:                
                    volunteer_id = search[0]

                    column_names=['email_id',
                                    'profession',
                                    'status']
                    values=[email_id,
                            profession,
                            '1']

                    where_stetment="volunteer_id = '"+str(volunteer_id)+"'"
                    query=update_query("tblVolunteer",column_names,values,where_stetment)
                    # print(query)
                
                    res = db.update_data(query)
                    
                
            
            columns=" * "
            where_stetment="user_id = '"+str(user_id)+"'"           
            query=select_query("tblVolunteer",columns,where_stetment)                    
            volunteer = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': volunteer}, code

api.add_resource(VolunteerApi, '/volunteer_api')

@app.route("/volunteer_verifi", methods=['GET', 'POST'])
def volunteer_verifi():
    if authentication()==False:
        return redirect(url_for('login'))

    if session['login_user'][2]<2:
        return redirect(url_for('index'))

    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))
    
    return render_template('volunteer_verifi.html', title='স্বেচ্ছাসেবক যাচাইকরণ',hospital=hospital,key=key,login_user=session['login_user'])

class VolunteerVerifiApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search', required=True)
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        volunteers=None
        volunteer=None
        search = args['search']
        search = json.loads(search)
        if user_key == key:
            db=Db()
            district = session['user'][7]
            town = session['user'][8]
            # print("dddddddd:",district,town)
            columns=" tu.name,tu.profile_pic,tu.phone_number,tv.village,tv.verified,tv.email_id,tv.volunteer_id "
            if search['search']==0:                
                where_stetment="tv.hospital_id = '"+search['hospital_id']+"' ORDER BY tv.create_date DESC LIMIT 50  OFFSET "+offset
            else:
                volunteer_name=search['volunteer_name']
                phone_number=search['phone_number']
                where_stetment="tv.hospital_id = '"+search['hospital_id']+"' AND tu.name LIKE '"+'%'+volunteer_name+'%'+"' AND tu.phone_number LIKE '"+'%'+phone_number+'%'+"' ORDER BY tv.create_date DESC LIMIT 50  OFFSET "+offset
            
            
            join_query="tblVolunteer as tv "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblHospital as th ON th.hospital_id = tv.hospital_id "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON tv.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            volunteers = db.get_data(query)
            code =200
            msg="successfully"

        return {'message': msg, 'volunteers': volunteers}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        volunteer=None
        volunteer_id=0
        if user_key == key:

            db=Db()
            
            if args['method']=='accept':
                volunteer_id = data['volunteer_id']

                column_names=['verified']
                values=['1']

                where_stetment="volunteer_id = '"+str(volunteer_id)+"'"
                query=update_query("tblVolunteer",column_names,values,where_stetment)
            
                res = db.update_data(query)

            elif args['method']=='stoped':
                volunteer_id = data['volunteer_id']

                column_names=['verified']
                values=['0']

                where_stetment="volunteer_id = '"+str(volunteer_id)+"'"
                query=update_query("tblVolunteer",column_names,values,where_stetment)
            
                res = db.update_data(query)
                    
                
            
            columns=" tu.name,tu.profile_pic,tu.phone_number,tv.village,tv.verified,tv.email_id,tv.volunteer_id "
                            
            where_stetment="tv.volunteer_id = '"+str(volunteer_id)+"'"
                        
            join_query="tblVolunteer as tv "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblHospital as th ON th.hospital_id = tv.hospital_id "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON tv.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            volunteer = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': volunteer}, code

api.add_resource(VolunteerVerifiApi, '/volunteer_verifi_api')

@app.route("/collection", methods=['GET', 'POST'])
def collection():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))
    
    return render_template('collection.html', title='অর্থ সংগ্রহ',hospital=hospital,key=key,login_user=session['login_user'])

class CollectionApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search', required=True)
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        collections=None
        search = args['search']
        search = json.loads(search)
        if user_key == key:
            db=Db()
            hospital_id=search['hospital_id']
            columns=" * "
            if search['search']==0:
                where_stetment="hospital_id = '"+hospital_id+"' AND user_id = '"+str(user_id)+"' ORDER BY collection_date DESC LIMIT 50  OFFSET "+offset
            else:
                name=search['name']
                phone_number=search['phone_number']
                where_stetment="hospital_id = '"+hospital_id+"' AND user_id = '"+str(user_id)+"' AND name LIKE '"+'%'+name+'%'+"' AND phone_number LIKE '"+'%'+phone_number+'%'+"' ORDER BY collection_date DESC LIMIT 50  OFFSET "+offset
            
            query=select_query("tblCollection",columns,where_stetment)                    
            collections = db.get_data(query)

            columns="collection,collection_number,donated"
            where_stetment="user_id = '"+str(user_id)+"'"  
            query=select_query("tblUser",columns,where_stetment)                    
            collector = db.get_data_by_key(query)

            code =200
            msg="successfully"

        return {'message': msg, 'collections': collections,'collector':collector}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        collection=None
        collection_id=0
        if user_key == key:

            db=Db()

            if args['method']=='post':
                hospital_id = data['hospital_id']
                name = data['name']
                phone_number = data['phone_number']
                photo = data['photo']
                amount = data['amount']
                collection_date=time.time()-60                    
                columns="collection_id"
                where_stetment="user_id = '"+str(user_id)+"' AND name = '"+name+"' AND collection_date >= '"+str(collection_date)+"'"  
                query=select_query("tblCollection",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    column_names=['user_id',
                                    'hospital_id',
                                    'name',
                                    'phone_number',
                                    'photo',
                                    'amount',
                                    'collection_date',
                                    'status']
                    values=[str(user_id),
                            hospital_id,
                            name,
                            phone_number,
                            photo,
                            amount,
                            str(time.time()),
                            '0']
                    query=insert_query("tblCollection",column_names,values)
                    # print(query)
                    collection_id = db.insert_data(query)

                    columns="collection,collection_number"
                    where_stetment="user_id = '"+str(user_id)+"'"  
                    query=select_query("tblUser",columns,where_stetment)                    
                    collector = db.get_data_by_key(query)

                    column_names=['collection',
                                    'collection_number']
                    values=[str(collector[0]+int(amount)),
                            str(collector[1]+1)]

                    where_stetment="user_id = '"+str(user_id)+"'"
                    query=update_query("tblUser",column_names,values,where_stetment)
                    # print(query)
                
                    res = db.update_data(query)
                
            
            columns=" * "
            where_stetment="collection_id = '"+str(collection_id)+"'"           
            query=select_query("tblCollection",columns,where_stetment)                    
            collection = db.get_data_by_key(query)

            columns="collection,collection_number,donated"
            where_stetment="user_id = '"+str(user_id)+"'"  
            query=select_query("tblUser",columns,where_stetment)                    
            collector = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': collection, 'collector': collector}, code

api.add_resource(CollectionApi, '/collection_api')

@app.route("/collection_view", methods=['GET', 'POST'])
def collection_view():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))

    
    return render_template('collection_view.html', title='অর্থ সংগ্রহ',hospital=hospital,key=key,login_user=session['login_user'])

@app.route("/get_collection_view", methods=['GET'])
def get_collection_view():

    db = Db()
    offset = request.args.get('offset')
    district = session['user'][7]
    town = session['user'][8]
    columns=" tc.* "    
    where_stetment="th.district = '"+district+"' AND th.town = '"+town+"' ORDER BY collection_date DESC LIMIT 50  OFFSET "+offset    
    join_query="tblCollection as tc "
    join_query=join_query+"LEFT JOIN "
    join_query=join_query+"tblHospital as th ON tc.hospital_id = th.hospital_id "
    query=select_query(join_query,columns,where_stetment)                    
    collections = db.get_data(query)

    result={"collections":collections}
    # print(result)

    return jsonify(result)

@app.route("/donated", methods=['GET', 'POST'])
def donated():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))
    
    return render_template('donated.html', title='অর্থ প্রদান',hospital=hospital,key=key,login_user=session['login_user'])

@app.route("/donated_verifi", methods=['GET', 'POST'])
def donated_verifi():
    if authentication()==False:
        return redirect(url_for('login'))

    if session['login_user'][2]<2:
        return redirect(url_for('index'))

    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))
    
    return render_template('donated_verifi.html', title='donated_verifi',hospital=hospital,key=key,login_user=session['login_user'])

class DonatedApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        donates=None
        if user_key == key:
            db=Db()
            
            columns=" td.*,th.hospital_name "
            where_stetment="td.user_id = '"+str(user_id)+"' ORDER BY td.create_date DESC LIMIT 50  OFFSET "+offset
            join_query="tblDonated as td "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblHospital as th ON th.hospital_id = td.hospital_id "
            query=select_query(join_query,columns,where_stetment)                   
            donates = db.get_data(query)

            columns="collection,collection_number,donated"
            where_stetment="user_id = '"+str(user_id)+"'"  
            query=select_query("tblUser",columns,where_stetment)                    
            collector = db.get_data_by_key(query)

            code =200
            msg="successfully"

        return {'message': msg, 'donates': donates,'collector':collector}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        donated=None
        donated_id=0
        if user_key == key:

            db=Db()

            if args['method']=='post':
                hospital_id = data['hospital_id']
                account_name = data['account_name']
                to_account_number = data['to_account_number']
                from_account_number = data['from_account_number']
                delever_msg = data['delever_msg']
                amount = data['amount']
                create_date=time.time()-60                    
                columns="donated_id"
                where_stetment="user_id = '"+str(user_id)+"' AND create_date >= '"+str(create_date)+"'"  
                query=select_query("tblDonated",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    column_names=['user_id',
                                    'hospital_id',
                                    'account_name',
                                    'to_account_number',
                                    'from_account_number',
                                    'delever_msg',
                                    'amount',
                                    'create_date',
                                    'received',
                                    'status']
                    values=[str(user_id),
                            hospital_id,
                            account_name,
                            to_account_number,
                            from_account_number,
                            delever_msg,
                            amount,
                            str(time.time()),
                            '0',
                            '1']
                    query=insert_query("tblDonated",column_names,values)
                    # print(query)
                    donated_id = db.insert_data(query)

                    donated_amount=int(amount)

                    columns="donated"
                    where_stetment="user_id = '"+str(user_id)+"'"  
                    query=select_query("tblUser",columns,where_stetment)                    
                    collector = db.get_data_by_key(query)

                    column_names=['donated']
                    values=[str(collector[0]+donated_amount)]

                    where_stetment="user_id = '"+str(user_id)+"'"
                    query=update_query("tblUser",column_names,values,where_stetment)
                
                    res = db.update_data(query)


                    
                    columns=" collection_id,amount "
                    where_stetment="user_id = '"+str(user_id)+"' AND status = 0"           
                    query=select_query("tblCollection",columns,where_stetment)                    
                    pending_collections = db.get_data(query)
                    for pending_collection in pending_collections:
                        if pending_collection[1]<=donated_amount:
                            
                            column_names=['status']
                            values=['1']                            
                            where_stetment="collection_id = '"+str(pending_collection[0])+"'"
                            query=update_query("tblCollection",column_names,values,where_stetment)
                            
                            res = db.update_data(query)
                            donated_amount=donated_amount-pending_collection[1]
                        else:
                            break

            elif args['method']=='update':
                donated_id = data['donated_id']
                account_name = data['account_name']
                to_account_number = data['to_account_number']
                from_account_number = data['from_account_number']
                delever_msg = data['delever_msg']
                amount = data['amount']

                columns=" received "
                where_stetment="donated_id = '"+str(donated_id)+"' AND received = 0"           
                query=select_query("tblDonated",columns,where_stetment)                    
                donated = db.get_data_by_key(query)
                if donated != None:
                    column_names=['account_name',
                                    'to_account_number',
                                    'from_account_number',
                                    'delever_msg',
                                    'amount',
                                    'status']
                    values=[account_name,
                            to_account_number,
                            from_account_number,
                            delever_msg,
                            amount,
                            '1']
                    
                    where_stetment="donated_id = '"+str(donated_id)+"'"
                    query=update_query("tblDonated",column_names,values,where_stetment)
                    # print(query)
                    
                    res = db.update_data(query)

                    
                
            
            columns=" * "
            where_stetment="donated_id = '"+str(donated_id)+"'"           
            query=select_query("tblDonated",columns,where_stetment)                    
            donated = db.get_data_by_key(query)

            columns="collection,collection_number,donated"
            where_stetment="user_id = '"+str(user_id)+"'"  
            query=select_query("tblUser",columns,where_stetment)                    
            collector = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': donated, 'donated': collector}, code

api.add_resource(DonatedApi, '/donated_api')

@app.route("/donated_view", methods=['GET', 'POST'])
def donated_view():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))

    
    return render_template('donated_view.html', title='অর্থ সংগ্রহ',hospital=hospital,key=key,login_user=session['login_user'])

@app.route("/get_donated_view", methods=['GET'])
def get_donated_view():

    db = Db()
    offset = request.args.get('offset')
    district = session['user'][7]
    town = session['user'][8]
    columns=" td.*,tu.name,tu.profile_pic "    
    where_stetment="th.district = '"+district+"' AND th.town = '"+town+"' ORDER BY td.create_date DESC LIMIT 50  OFFSET "+offset    
    join_query="tblDonated as td "
    join_query=join_query+"LEFT JOIN "
    join_query=join_query+"tblUser as tu ON td.user_id = tu.user_id "
    join_query=join_query+"LEFT JOIN "
    join_query=join_query+"tblHospital as th ON td.hospital_id = th.hospital_id "
    query=select_query(join_query,columns,where_stetment)                    
    donates = db.get_data(query)

    result={"donates":donates}
    # print(result)

    return jsonify(result)

@app.route("/developer", methods=['GET', 'POST'])
def developer():
    if authentication()==False:
        return redirect(url_for('login'))
    if session['login_user'][2]<2:
        return redirect(url_for('index'))

    key = str(uuid.uuid4())
    users[session['user'][0]] = key

   
    
    return render_template('developer.html', title='developer',key=key,login_user=session['login_user'])

class DeveloperApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search', required=True)
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        developers=None
        user=None
        search = args['search']
        search = json.loads(search)
        if user_key == key:
            db=Db()

            phone_number=search['phone_number']
            if phone_number !=0:
                columns="user_id,name,gender,profile_pic,district,town,phone_number"
                where_stetment="phone_number = '"+str(phone_number)+"'"  
                query=select_query("tblUser",columns,where_stetment)                    
                user = db.get_data_by_key(query)
                return {'user':user}, 200
            else:
                hospital_id=search['hospital_id']
                columns=" td.*,th.hospital_name,tu.name,tu.profile_pic,tu.phone_number "
                if hospital_id==0:
                    where_stetment="td.status = 1 ORDER BY td.create_date DESC LIMIT 50  OFFSET "+offset
                else:
                    where_stetment="td.status = 1 AND td.hospital_id = '"+hospital_id+"' ORDER BY td.create_date DESC LIMIT 50  OFFSET "+offset
                
                
                join_query="tblDeveloper as td "
                join_query=join_query+"LEFT JOIN "
                join_query=join_query+"tblUser as tu ON td.user_id = tu.user_id "
                join_query=join_query+"LEFT JOIN "
                join_query=join_query+"tblHospital as th ON td.hospital_id = th.hospital_id "
                query=select_query(join_query,columns,where_stetment)                    
                developers = db.get_data(query)

            
            code =200
            msg="successfully"

        return {'message': msg, 'developers': developers,'user':user}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        developer=None
        developer_id=0
        if user_key == key:

            db=Db()

            if args['method']=='post':
                dev_user_id = data['dev_user_id']
                hospital_id = data['hospital_id']
                                    
                columns="developer_id"
                where_stetment="user_id = '"+str(dev_user_id)+"' AND hospital_id = '"+hospital_id+"'"  
                query=select_query("tblDeveloper",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    column_names=['user_id',
                                    'hospital_id',
                                    'work_start_date',
                                    'work_end_date',
                                    'work_fedback',
                                    'working',
                                    'create_date',
                                    'status']
                    values=[str(dev_user_id),
                            hospital_id,                           
                            '',
                            '',
                            '',
                            '0',
                            str(time.time()),
                            '1']
                    query=insert_query("tblDeveloper",column_names,values)
                    # print(query)
                    developer_id = db.insert_data(query)
            elif args['method']=='dev_start':
                developer_id = data['developer_id']

                column_names=['work_start_date',
                                'working']
                values=[str(time.time()),
                        '1']

                where_stetment="developer_id = '"+str(developer_id)+"'"
                query=update_query("tblDeveloper",column_names,values,where_stetment)
                
                res = db.update_data(query)

            elif args['method']=='stop':
                developer_id = data['developer_id'] 

                column_names=['work_end_date',
                                'working']
                values=[str(time.time()),
                        '0']

                where_stetment="developer_id = '"+str(developer_id)+"'"
                query=update_query("tblDeveloper",column_names,values,where_stetment)
                
                res = db.update_data(query)

            

            
            columns=" td.*,th.hospital_name,tu.name,tu.profile_pic,tu.phone_number "
            where_stetment="td.developer_id = '"+str(developer_id)+"'"  
            
            join_query="tblDeveloper as td "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON td.user_id = tu.user_id "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblHospital as th ON td.hospital_id = th.hospital_id "
            query=select_query(join_query,columns,where_stetment)                    
            developer = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': developer}, code

api.add_resource(DeveloperApi, '/developer_api')

@app.route("/costing", methods=['GET', 'POST'])
def costing():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))
    
    return render_template('costing.html', title='costing',hospital=hospital,key=key,login_user=session['login_user'])

class CostingApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hospital_id', required=True)
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        collections=None
        hospital_id = args['hospital_id']
        if user_key == key:
            db=Db()
            
            columns=" tc.* "
            where_stetment="tc.hospital_id = '"+hospital_id+"' AND tu.user_id = '"+str(user_id)+"' ORDER BY tc.create_date DESC LIMIT 50  OFFSET "+offset
            join_query="tblCosting as tc "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblDeveloper as td ON td.developer_id = tc.developer_id "
            join_query=join_query+"LEFT JOIN "
            join_query=join_query+"tblUser as tu ON td.user_id = tu.user_id "
            query=select_query(join_query,columns,where_stetment)                    
            costings = db.get_data(query)

            code =200

        return {'costings': costings}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        costing=None
        costing_id=0
        if user_key == key:

            db=Db()
            hospital_id = data['hospital_id']
            columns=" developer_id "
            where_stetment="user_id = '"+str(user_id)+"' AND hospital_id = '"+str(hospital_id)+"'"           
            query=select_query("tblDeveloper",columns,where_stetment)                    
            developer = db.get_data_by_key(query)
            if developer==None:
                return {'data': costing}, code

            developer_id=developer[0]

            if args['method']=='delete':
                costing_id = data['costing_id']
                columns="costing_id"
                where_stetment="developer_id = '"+str(developer_id)+"' AND costing_id = '"+str(costing_id)+"'  AND verified = 0"  
                query=select_query("tblCosting",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search != None:                    
                    query="DELETE FROM tblCosting WHERE costing_id = '"+str(costing_id)+"'" 
                    msg = db.update_data(query)

            elif args['method']=='post':
                hospital_id = data['hospital_id']
                item_name = data['item_name']
                item_count = data['item_count']
                unit=data['unit']
                cost = data['cost']
                item_pic = data['item_pic']
                create_date=time.time()-60                    
                columns="costing_id"
                where_stetment="developer_id = '"+str(developer_id)+"' AND item_name = '"+item_name+"' AND create_date >= '"+str(create_date)+"'"  
                query=select_query("tblCosting",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    column_names=['developer_id',
                                    'hospital_id',
                                    'item_name',
                                    'item_count',
                                    'unit',
                                    'cost',
                                    'verified',
                                    'paid',
                                    'item_pic',
                                    'paid_date',
                                    'create_date',
                                    'status']
                    values=[str(developer_id),
                            hospital_id,
                            item_name,
                            item_count,
                            unit,
                            cost,
                            '0',
                            '0',
                            item_pic,
                            '',
                            str(time.time()),
                            '1']
                    query=insert_query("tblCosting",column_names,values)
                    # print(query)
                    costing_id = db.insert_data(query)
                    msg = 'successfully'
            elif args['method']=='update':

                costing_id = data['costing_id']                

                columns=" * "
                where_stetment="developer_id = '"+str(developer_id)+"' AND costing_id = '"+str(costing_id)+"'  AND verified = 0"               
                query=select_query("tblCosting",columns,where_stetment)                    
                costing = db.get_data_by_key(query)

                if costing !=None:
                    item_name = data['item_name']
                    item_count = data['item_count']
                    unit=data['unit']
                    cost = data['cost']
                    item_pic = data['item_pic']

                    column_names=['item_name',
                                    'item_count',
                                    'unit',
                                    'cost',
                                    'item_pic',
                                    'status']
                    values=[item_name,
                            item_count,
                            unit,
                            cost,
                            item_pic,
                            '1']
                    
                    where_stetment="costing_id = '"+str(costing_id)+"'"
                    query=update_query("tblCosting",column_names,values,where_stetment)
                    # print(query)
                    
                    res = db.update_data(query)
                    msg = 'successfully'
                
            
            columns=" * "
            where_stetment="costing_id = '"+str(costing_id)+"'"           
            query=select_query("tblCosting",columns,where_stetment)                    
            costing = db.get_data_by_key(query)
            code =200

                    

        return {'message': msg,'data': costing}, code

api.add_resource(CostingApi, '/costing_api')

@app.route("/costing_verifi", methods=['GET', 'POST'])
def costing_verifi():
    if authentication()==False:
        return redirect(url_for('login'))

    if session['login_user'][2]<2:
        return redirect(url_for('index'))

    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))
    
    return render_template('costing_verifi.html', title='স্বেচ্ছাসেবক যাচাইকরণ',hospital=hospital,key=key,login_user=session['login_user'])

class CostingVerifiApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hospital_id', required=True)
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        collections=None
        hospital_id = args['hospital_id']
        if user_key == key:
            db=Db()
            
            columns=" * "
            where_stetment="status = 1 AND hospital_id = '"+hospital_id+"' ORDER BY create_date DESC LIMIT 50  OFFSET "+offset
            
            query=select_query('tblCosting',columns,where_stetment)                    
            costings = db.get_data(query)

            code =200

        return {'costings': costings}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        costing=None
        costing_id=0
        if session['login_user'][2]<2:
            return {'message': msg, 'data': costing}, code
        if user_key == key:

            db=Db()
            
            if args['method']=='accept':
                costing_id = data['costing_id']

                column_names=['verified']
                values=['1']

                where_stetment="costing_id = '"+str(costing_id)+"'"
                query=update_query("tblCosting",column_names,values,where_stetment)
            
                res = db.update_data(query)

            elif args['method']=='cancel':
                costing_id = data['costing_id']

                column_names=['status']
                values=['0']

                where_stetment="costing_id = '"+str(costing_id)+"'"
                query=update_query("tblCosting",column_names,values,where_stetment)
            
                res = db.update_data(query)
                # print('cos:',costing_id)

            elif args['method']=='paid':
                costing_id = data['costing_id']

                column_names=[ 'paid', 'paid_date']
                values=['1',str(time.time())]

                where_stetment="costing_id = '"+str(costing_id)+"'"
                query=update_query("tblCosting",column_names,values,where_stetment)
            
                res = db.update_data(query)
                    
                
            
            columns="* "
                            
            where_stetment="costing_id = '"+str(costing_id)+"'"
            query=select_query('tblCosting',columns,where_stetment)                    
            costing = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': costing}, code

api.add_resource(CostingVerifiApi, '/costing_verifi_api')

@app.route("/costing_view", methods=['GET', 'POST'])
def costing_view():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
    # print("dddddddd:",district,town)
    columns=" hospital_id,hospital_name "
    where_stetment="district = '"+district+"' AND town = '"+town+"' AND accept_proposal = 1"    
    query=select_query("tblHospital",columns,where_stetment)                    
    hospital = db.get_data_by_key(query)
    if hospital == None:
        return redirect(url_for('index'))

    
    return render_template('costing_view.html', title='অর্থ সংগ্রহ',hospital=hospital,key=key,login_user=session['login_user'])

@app.route("/get_costing_view", methods=['GET'])
def get_costing_view():

    db = Db()
    offset = request.args.get('offset')
    district = session['user'][7]
    town = session['user'][8]
    columns=" tc.* "    
    where_stetment="th.district = '"+district+"' AND th.town = '"+town+"' ORDER BY tc.create_date DESC LIMIT 50  OFFSET "+offset    
    join_query="tblCosting as tc "
    join_query=join_query+"LEFT JOIN "
    join_query=join_query+"tblHospital as th ON tc.hospital_id = th.hospital_id "
    query=select_query(join_query,columns,where_stetment)                    
    costings = db.get_data(query)

    result={"costings":costings}
    # print(result)

    return jsonify(result)

@app.route("/get_developer_hospitals", methods=['GET'])
def get_developer_hospitals():

    db = Db()
    
    columns=" td.hospital_id,th.hospital_name "
    
    where_stetment="td.status = 1 AND td.user_id = '"+str(session['user'][0])+"'"
    
    
    join_query="tblDeveloper as td "
    join_query=join_query+"LEFT JOIN "
    join_query=join_query+"tblUser as tu ON td.user_id = tu.user_id "
    join_query=join_query+"LEFT JOIN "
    join_query=join_query+"tblHospital as th ON td.hospital_id = th.hospital_id "
    query=select_query(join_query,columns,where_stetment)                    
    hospitals = db.get_data(query)

    result={"hospitals":hospitals}
    # print(result)

    return jsonify(result)

@app.route("/total_summary", methods=['GET', 'POST'])
def total_summary():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key

    db=Db()
    district = session['user'][7]
    town = session['user'][8]
   
    columns="tts.*,th.hospital_name "
    
    where_stetment="th.district = '"+district+"' AND th.town = '"+town+"'"
    
    join_query="tblTotalSummary as tts "
    join_query=join_query+"LEFT JOIN "
    join_query=join_query+"tblHospital as th ON tts.hospital_id = th.hospital_id "
    query=select_query(join_query,columns,where_stetment)                    
    total_summary = db.get_data_by_key(query)
    
    
    return render_template('total_summary.html', title='total_summary',total_summary=total_summary,key=key,login_user=session['login_user'])

@app.route("/notification", methods=['GET', 'POST'])
def notification():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key
    
    return render_template('notification.html', title='নোটিফিকেশন',key=key,login_user=session['login_user'])

def send_notification(user_id,notification):

    column_names=['user_id',
                'notification',
                'create_date',
                'read',
                'status']
    values=[str(user_id),
            notification,
            str(time.time()),
            '0',
            '1']
    query=insert_query("tblNotification",column_names,values)
    # print(query)
    notification_id = db.insert_data(query)

    return notification_id

class NotificationApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        volunteers=None
        volunteer=None
        if user_key == key:
            db=Db()
            
            columns=" * "  
            where_stetment="user_id = '"+str(user_id)+"' ORDER BY create_date DESC LIMIT 50  OFFSET "+offset
           
            query=select_query('tblNotification',columns,where_stetment)                    
            notifications = db.get_data(query)
            code =200
            msg="successfully"

        return {'message': msg, 'notifications': notifications}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        notification=None
        notification_id=0
        if user_key == key:

            db=Db()
            
            if args['method']=='read':
                notification_id = data['notification_id']

                column_names=['read']
                values=['1']

                where_stetment="notification_id = '"+str(notification_id)+"'"
                query=update_query("tblNotification",column_names,values,where_stetment)
            
                res = db.update_data(query)
                
            
            columns="*"
                            
            where_stetment="notification_id = '"+str(notification_id)+"'"

            query=select_query('tblNotification',columns,where_stetment)                    
            notification = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': notification}, code

api.add_resource(NotificationApi, '/notification_api')


@app.route("/meeting", methods=['GET', 'POST'])
def meeting():
    if authentication()==False:
        return redirect(url_for('login'))
    key = str(uuid.uuid4())
    users[session['user'][0]] = key
    
    return render_template('meeting.html', title='নোটিফিকেশন',key=key,login_user=session['login_user'])

class MeetingApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('offset', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        offset = args['offset']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        volunteers=None
        volunteer=None
        if user_key == key:
            db=Db()
            
            columns=" * "  
            where_stetment="user_id = '"+str(user_id)+"' ORDER BY create_date DESC LIMIT 50  OFFSET "+offset
           
            query=select_query('tblMeeting',columns,where_stetment)                    
            notifications = db.get_data(query)
            code =200
            msg="successfully"

        return {'message': msg, 'notifications': notifications}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        notification=None
        notification_id=0
        if user_key == key:

            db=Db()
            
            if args['method']=='post':
                hospital_id = data['hospital_id']
                about_meeting = data['about_meeting']
                meeting_link = data['meeting_link']
                meeting_time = data['meeting_time']
                                    
                columns="meeting_id"
                where_stetment="user_id = '"+str(dev_user_id)+"' AND hospital_id = '"+hospital_id+"'"  
                query=select_query("tblMeeting",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    column_names=['hospital_id',
                                    'about_meeting',
                                    'meeting_link',
                                    'meeting_done',
                                    'meeting_time',
                                    'status']
                    values=[hospital_id,                           
                            about_meeting,
                            meeting_link,
                            '0',
                            meeting_time,
                            '1']
                    query=insert_query("tblMeeting",column_names,values)
                    # print(query)
                    meeting_id = db.insert_data(query)
            elif args['method']=='update':
                meeting_id = data['meeting_id']
                about_meeting = data['about_meeting']
                meeting_link = data['meeting_link']
                meeting_time = data['meeting_time']
                meeting_done = data['meeting_done']

                column_names=['about_meeting',
                                'meeting_link',
                                'meeting_done',
                                'meeting_time',
                                'status']
                values=[about_meeting,
                        meeting_link,
                        meeting_done,
                        meeting_time,
                        '1']

                where_stetment="meeting_id = '"+str(meeting_id)+"'"
                query=update_query("tblMeeting",column_names,values,where_stetment)
                
                res = db.update_data(query)

                
            
            columns="*"
                            
            where_stetment="notification_id = '"+str(notification_id)+"'"

            query=select_query('tblMeeting',columns,where_stetment)                    
            notification = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': notification}, code

api.add_resource(MeetingApi, '/meeting_api')

@app.route("/settings", methods=['GET', 'POST'])
def settings():

    if authentication()==False:
        return redirect(url_for('login'))

    if session['login_user'][2]<2:
        return redirect(url_for('index'))
    

    return render_template('settings.html', title='সেটিংস',
        login_user=session['login_user'])

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if authentication()==False:
        return redirect(url_for('login'))

    db=Db()

    # columns="user_id"
    # where_stetment="status = 1"
    # query=select_query("tblUser",columns,where_stetment)
    # users = db.get_data(query)
    # for user in users:
    #     create_account(user[0],db)

    columns="medical_staff_id, medical_staff_type"
    where_stetment="user_id = "+ str(session['user'][0])
    query=select_query("tblMedicalStaff",columns,where_stetment)                    
    medical_staff = db.get_data_by_key(query)
    if medical_staff == None:
        return redirect(url_for('patient_dashboard'))
    elif medical_staff[1]=='doctor':
        return redirect(url_for('doctor_dashboard'))
    else:
        return redirect(url_for('index'))


    return render_template('dashboard.html', title='মাই ড্যাশবোর্ড',
        login_user=session['login_user'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getImageList(persons):

    personLst=[]
    for person in persons:
        face_list=os.listdir("static/assets/img/")
        
        if 0<len(face_list):
            filename="static/assets/img/"+face_list[0]
            personLst.append((person[0],person[1],filename))
    return personLst


@app.route("/profile", methods=['GET', 'POST'])
def profile():
    
    if authentication()==False:
        return redirect(url_for('login'))

    
    columns="name,gender,nid,profile_pic,district,town,village"
    where_stetment="status = 1 AND user_id = '"+str(session['user'][0])+"'"
    query=select_query("tblUser",columns,where_stetment)
    # print(query)
    db=Db()
    user_info = db.get_data_by_key(query)
    

    return render_template('profile.html', title='প্রোফাইল',user_info=user_info,
        login_user=session['login_user'])

@app.route("/update_profile", methods=['GET', 'POST'])
def update_profile():
    
    if authentication()==False:
        return redirect(url_for('login'))
    db=Db()
    if request.method == 'POST':
        
        if request.form['action']=="submit":
                        
            column_names=['name','gender','nid','district','town','village']
            
            profile_pic=load_photo(request.files,'profile_pic')

            values=[request.form['first_name'],
                request.form['gender'],
                request.form['nid'],
                request.form['district'],
                request.form['town'],
                request.form['village']]
            if profile_pic!='':
                column_names.append('profile_pic')
                values.append(profile_pic)
            where_stetment="user_id = '"+str(session['user'][0])+"'"
            query=update_query("tblUser",column_names,values,where_stetment)
            # print(query)
            
            res = db.update_data(query)


        

    columns="name,gender,nid,profile_pic,district,town,village"
    where_stetment="status = 1 AND user_id = '"+str(session['user'][0])+"'"
    query=select_query("tblUser",columns,where_stetment)
    # print(query)
   
    user_info = db.get_data_by_key(query)
    districts = db.get_all_district()
    towns=[]
    if len(user_info[4])>0:
        pass
        towns = db.get_thanas_by_district_id(user_info[4])

    return render_template('update_profile.html', title='প্রোফাইল পরিবর্তন',user_info=user_info,districts=districts,towns=towns,
        login_user=session['login_user'])

@app.route("/admins", methods=['GET', 'POST'])
def admins():

    if authentication()==False:
        return redirect(url_for('login'))

    if session['login_user'][2]<2:
        return redirect(url_for('index'))

    isAdmin=False
    search_user=[]
    if request.method == 'POST':

        if request.form['action']=="set associate":

            if len(session['admin'])>0:
                
                column_names=['status']
                values=['1']

                where_stetment="admin_id = '"+str(session['admin'][0])+"'"
                query=update_query("tblAdmin",column_names,values,where_stetment)
                # print(query)
                
                res = db.update_data(query)
            else:
                user_id =request.form['search_user_id']
                db=Db()
                

                column_names=['user_id',
                            'admin_type',
                            'access_all',
                            'create_date',
                            'security_key',
                            'status']
                values=[str(user_id),
                            'associate admin',
                            '0',
                            str(time.time()),
                            'security_key',
                            '1']

                key = session['key']
                cipher_suite = Fernet(key)
                security_key =str(len(values[0])+len(values[1])+len(values[2])+len(values[3])+len(values[5]))
                ciphered_key = cipher_suite.encrypt(security_key.encode('ASCII'))   #required to be bytes
               
                values[4] = ciphered_key.decode('ASCII')

                query=insert_query("tblAdmin",column_names,values)
                # print(query)
                admin_id = db.insert_data(query)

                flash('Thanks for add.')
        elif request.form['action']=="remove admin":

            if session['admin'][2]!="root admin":             
                
                column_names=['status']
                values=['0']

                where_stetment="admin_id = '"+str(session['admin'][0])+"'"
                query=update_query("tblAdmin",column_names,values,where_stetment)
                # print(query)
                
                res = db.update_data(query)
            else:
                flash("Root Admin can not remove.")
        else:
            user_id = request.form['action']
            if user_id=="submit":
                phone_number = request.form['search_phone']
                where_stetment="phone_number = '"+phone_number+"'"
            else:
                where_stetment="user_id = '"+user_id+"'"

            session['key']=""
            session['admin']=[]
            

            db=Db()
            columns="user_id,phone_number,phone_number_verified,first_name,last_name,gender,user_type,about,nid,profile_pic,district,town,village,present_address,lat,lon,datetime(create_date,'unixepoch'),verified,key"
            
            query=select_query("tblUser",columns,where_stetment)                    
            search_user = db.get_data_by_key(query)
            if search_user == None:
                search_user=[]
                flash('Do not find.')
            else:
                session['key']=search_user[len(search_user)-1]

                columns="admin_id,user_id,admin_type,status"
                where_stetment="user_id = '"+str(search_user[0])+"'"
                query=select_query("tblAdmin",columns,where_stetment)                    
                res = db.get_data_by_key(query)
                if res == None:
                    isAdmin =False
                else:
                    isAdmin = res[3]
                    session['admin']=res

        
    db=Db()
    columns="ta.admin_id,ta.user_id,ta.admin_type,ta.access_all,datetime(ta.create_date,'unixepoch'), tu.first_name, tu.last_name , tu.user_type"
    where_stetment="ta.status = 1"
    query=select_query("tblAdmin as ta INNER JOIN tblUser as tu ON ta.user_id = tu.user_id",columns,where_stetment)                    
    admin_users = db.get_data(query)
    
    
    
    return render_template('admins.html', title='admins',search_user=search_user,admin_users=admin_users,isAdmin=isAdmin,
        login_user=session['login_user'])

def get_key(user_id,db):

    columns=" key "
    where_stetment="user_id = "+ user_id
    query=select_query("tblUser",columns,where_stetment)                    
    key = db.get_data_by_key(query)
    if key != None:
        return key[0]

    else:
        ''

def load_photo(request_files,url):
    photo_url=""
    if url not in request_files:
        flash('No file part')
    else:
        file = request_files[url]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            uniq_id=str(uuid.uuid4())
            photo_url="static/assets/img/tmp/"+url+uniq_id+".png"
            file.save(photo_url)
    return photo_url

def load_photos(request_files,url):
    photo_urls=[]
    if url not in request_files:
        flash('No file part')
    else:
        # file = request_files[url]
        files = request_files.getlist(url)
        
        for file in files:
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                uniq_id=str(uuid.uuid4())
                photo_url="static/assets/img/tmp/"+url+uniq_id+".png"
                file.save(photo_url)
                photo_urls.append(photo_url)
    return photo_urls

@app.route("/GetAllDistrict", methods=['GET', 'POST'])
def GetAllDistrict():

    db = Db()
    if request.method == 'POST':
        if request.form['action']=="submit":
            database = "district.db"
            try:
                conn = sqlite3.connect(database)
                print(sqlite3.version)
                
            except Error as e:
                pass

            cur = conn.cursor()
            cur.execute("SELECT * FROM tblDistrict where status = 1")
            
            districts = cur.fetchall()
            for district in districts:
                district_id=district[0]
                cur.execute("SELECT * FROM tblThana where status = 1 AND district_id = ? ",(district_id,))
            
                thanas = cur.fetchall()
                for than in thanas:
                    # print(than['Name'])
                    insert=(district[1],than[2])
                    db.insert_thana(insert)

            conn.close()

            # response = requests.get("http://www.amaarhero.com/amaarheroservice.asmx/GetAllDistrict")
            # print(response.status_code)
            # # print(response.json())
            # districts=response.json()
            
            # for dis in districts:                
            #     # print("District: ",dis['Name'])
            #     for than in dis['ThanaList']:
            #         # print(than['Name'])
            #         insert=(dis['Name'],than['Name'])
            #         db.insert_thana(insert)

            
    
    districts = db.get_district_details()

    return render_template('GetAllDistrict.html', title='GetAllDistrict',districts=districts,login_user=session['login_user'])


@app.route("/get_district", methods=['GET'])
def get_district():
    
    db = Db()
    
    districts = db.get_all_district()

    result={"districts":districts}
    # print(result)

    return jsonify(result)

@app.route("/get_thanas_by_district", methods=['GET'])
def get_thanas_by_district():

    district_id = request.args.get('id')

    db = Db()
    
    # print(flg,intent_id)
    thanas=db.get_thanas_by_district_id(district_id)
    # print("intent:",intent)

    result={"thanas":thanas}
    # print(result)

    return jsonify(result)

@app.route("/village", methods=['GET', 'POST'])
def village():
    db=Db()
    key = str(uuid.uuid4())
    users[session['user'][0]] = key
    districts = db.get_all_district()
    return render_template('village.html', title='village',key=key,districts=districts,login_user=session['login_user'])

@app.route("/get_villages_by_thana", methods=['GET'])
def get_villages_by_thana():

    thana_id = request.args.get('id')

    db = Db()
    
    columns=" village_id,village "
    where_stetment="thana_id = '"+thana_id+"'"
    query=select_query("tblVillage",columns,where_stetment)                    
    villages = db.get_data(query)

    result={"villages":villages}
    # print(result)

    return jsonify(result)

class VillageApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('thana_id', required=True)
        parser.add_argument('auth', required=True)
        args = parser.parse_args()

        thana_id = args['thana_id']
        auth = args['auth']
        auth = json.loads(auth)
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        villages=None
        if user_key == key:
            db=Db()
            
            columns="village_id,village "
            where_stetment="thana_id = '"+thana_id+"'"
            query=select_query("tblVillage",columns,where_stetment)                    
            villages = db.get_data(query)


            code =200
            msg="successfully"

        return {'message': msg, 'villages': villages}, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', required=True)
        parser.add_argument('auth', required=True)
        parser.add_argument('method', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        data = args['data']
        data = json.loads(data)
        auth = args['auth']
        auth = json.loads(auth)
        
        key=auth['key']      
        user_id = int(auth['u_id'])
        user_key=users[user_id]
        msg="unauthorized request"
        code =401
        village=None
        village_id=0
        if user_key == key:

            db=Db()

            if args['method']=='delete':
                village_id = data['village_id']
                query="DELETE FROM tblVillage WHERE village_id = '"+str(village_id)+"'" 
                msg = db.update_data(query)

            elif args['method']=='post':
                thana_id = data['thana_id']
                village = data['village']

                columns="village_id"
                where_stetment="thana_id = '"+str(thana_id)+"' AND village = '"+str(village)+"'"  
                query=select_query("tblVillage",columns,where_stetment)                    
                search = db.get_data_by_key(query)
                if search == None:

                    column_names=['thana_id',
                                    'village',
                                    'longitude',
                                    'latitude',
                                    'status']
                    values=[str(thana_id),
                            village,
                            '0',
                            '0',
                            '1']
                    query=insert_query("tblVillage",column_names,values)
                    # print(query)
                    village_id = db.insert_data(query)

            elif args['method']=='update':
                village_id = data['village_id']
                village = data['village']
                
                column_names=['village'
                                'status']
                values=[village,
                        '1']
                
                where_stetment="village_id = '"+str(village_id)+"'"
                query=update_query("tblVillage",column_names,values,where_stetment)
                # print(query)
                
                res = db.update_data(query)

                    
                
            
            columns=" village_id,village "
            where_stetment="village_id = '"+str(village_id)+"'"           
            query=select_query("tblVillage",columns,where_stetment)                    
            village = db.get_data_by_key(query)
            code =200               
                    

        return {'message': msg, 'data': village}, code

api.add_resource(VillageApi, '/village_api')

class ThanaUpdateApi(Resource):
    def get(self):
        data=[]

        return {'message': 'Success', 'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('thana_id', required=True)
        parser.add_argument('log', required=True)
        parser.add_argument('lat', required=True)
        parser.add_argument('covid19_center', required=True)
        parser.add_argument('method', required=True)
        parser.add_argument('key', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        print(args)
        msg = ""
        question_id=0
        db=Db()
        if args['method']=='update':

            thana_id=args['thana_id']

            update=(args['log'],args['lat'],args['covid19_center'],1,thana_id)
            db.update_thana_lon_lat(update)
            msg = "Thana update successfully."


        return {'message': msg, 'data': []}, 201

api.add_resource(ThanaUpdateApi, '/update_town')

@app.route('/file-upload', methods=['POST'])
def upload_file():
    # # load_photos(request.files,'file')
    # # check if the post request has the file part
    # if 'file' not in request.files:
    #     resp = jsonify({'message' : 'No file part in the request'})
    #     resp.status_code = 400
    #     return resp
    # file = request.files['file']
    # print(file)
    # if file.filename == '':
    #     resp = jsonify({'message' : 'No file selected for uploading'})
    #     resp.status_code = 400
    #     return resp
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     uniq_id=str(uuid.uuid4())
    #     photo_url="static/assets/img/tmp/"+uniq_id+".png"
    #     file.save(photo_url)
    #     resp = jsonify({'message' : 'File successfully uploaded'})
    #     resp.status_code = 201
    #     return resp
    # else:
    #     resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
    #     resp.status_code = 400
    #     return resp
    photo_urls=[]
    if 'file' not in request.files:
        flash('No file part')
    else:
        # file = request_files[url]
        files = request.files.getlist('file')
        
        for file in files:
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                
            elif file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                uniq_id=str(uuid.uuid4())
                photo_url="static/assets/img/tmp/"+uniq_id+".png"
                file.save(photo_url)
                photo_urls.append(photo_url)

    prescription_img_url = ','.join(photo_urls)
    # print(prescription_img_url)

    return jsonify({'url' : prescription_img_url})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    # socketio.run( app, debug = True,host='192.168.8.170' )
    # socketio.run( app, debug = True )
