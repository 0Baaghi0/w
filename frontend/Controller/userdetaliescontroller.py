
import email
import bcrypt
from flask import Flask, request, jsonify, config ,session
import mysql.connector
from sqlalchemy import Text, func
from config import *
from model.userdetalies import *
from bcrypt import hashpw, gensalt
import pandas as pd
import re
import smtplib
import random
import string
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker
from datetime import datetime,timedelta
from werkzeug.security import generate_password_hash
from bcrypt import hashpw, gensalt
import bcrypt
bcrypt = Bcrypt()
 
def register_user_data():
    try:
        data = request.json
        print('data-->', data)
        required_fields = ['USER_NAME', 'PASSWORD', 'FIRST_NAME', 'LAST_NAME', 'EMAIL',
                           'USER_TYPE','MOBILE_NO','USER_ID']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400        
        PASSWORD = data.get('PASSWORD')
        user_id = data.get('USER_ID')
        user_name = data.get('USER_NAME')
        email = data.get('EMAIL')
        mobile_no = data.get('MOBILE_NO')
        middlename=data.get('MIDDLE_NAME')
        if user_id and UserDetails.query.filter_by(USER_ID=user_id).first():
            return jsonify({'error': 'USER_ID already exists'}), 400
        if email and UserDetails.query.filter_by(EMAIL=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        if mobile_no and UserDetails.query.filter_by(MOBILE_NO=mobile_no).first():
            return jsonify({'error': 'Mobile number already exists'}), 400
        if mobile_no and (not re.match(r'^\d{10}$', str(mobile_no))):
            return jsonify({'error': 'Mobile number should be exactly 10 digits long'}), 400
     
        password_hash = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_data = UserDetails(
            USER_ID=user_id,
            USER_NAME=user_name,
            PASSWORD=password_hash,
            FIRST_NAME=data['FIRST_NAME'],
            MIDDLE_NAME=middlename,
            LAST_NAME=data['LAST_NAME'],
            EMAIL=email,
            MOBILE_NO=mobile_no,
            USER_TYPE=data['USER_TYPE'],
            CREATED_BY="HR",
            LAST_UPDATED_BY="HR"
        )
       
        db.session.add(user_data)
        db.session.commit()
       
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
 
import bcrypt
import jwt
 
SECRET_KEY = 'secret_key'
 
def login():
    try:
        data = request.json
        username_or_email = data.get('username_or_email')
        password = data.get('password')      
        user = UserDetails.query.filter((UserDetails.USER_NAME == username_or_email) | (UserDetails.EMAIL == username_or_email)).first()      
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.PASSWORD.encode('utf-8')):                
                payload = {'USER_NAME': user.USER_NAME,
                           'password':user.PASSWORD}
                emailerjson=email.json
                token = jwt.encode(payload, SECRET_KEY)
                return jsonify({'message': 'Login successful', 'token': token}), 200
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as err:
        return jsonify({'err': str(err)}), 500
#============================================================================================
def getemployees():
    data = UserDetails.query.all()
    print(data)
    returnData= []
    for i in data:
        returnData.append(i.serialize())
    print('returnData',returnData)
    return returnData
 
def getemployeeId(USER_ID):
    try:
        data = UserDetails.query.get(USER_ID)
        if not data:
                return jsonify({'message':'employees not found'}),404
        return jsonify({'message':f'employee {USER_ID}','data':data.serialize()}),200
    except Exception as err:
        return jsonify({'err':str(err)}),500
   
   
 
def deleteemployee(USER_ID):
    try:
        employees=UserDetails.query.get(USER_ID)
        print("gghah",employees)
        if not employees:
            return jsonify({'message':'employees not found'}),404
        db.session.delete(employees)
        db.session.commit()
        return jsonify({'message':f'employee {USER_ID} deleted succesfully','data':employees.serialize()}),200
    except Exception as err:
        return jsonify({'err':str(err)}),500
   
 
def updateemployee(USER_ID):
    try:
        data = request.json
        employees = UserDetails.query.get(USER_ID)
        for field in data.keys():
            new_value = data.get(field)
            if field == 'PASSWORD':
                new_value_hash = bcrypt.hashpw(new_value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                if employees.PASSWORD != new_value_hash:
                    setattr(employees, field, new_value_hash)
            else:
                if getattr(employees, field) != new_value:
                    setattr(employees, field, new_value)
        db.session.commit()
        return jsonify({'message': employees.serialize()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
###Forgetting Mail
   #Generate OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=5))
 
    #send OTP via Email
def send_otp_email(app, email, otp):
    try:
        # data = request.json
        # email = data.get('EMAIL')
        # print(email)
        msg = Message('Password Reset OTP', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Your oTP for Password Reset is: {otp}'
        mail.send(msg)
        print("Email Sent Successfully")
        return True
    except Exception as e:
        print(f"Error Sending Email: {e}")
        return False
 
        ##api for forgetting Password
def forgetpassword():
    data = request.get_json()
    email = data.get('EMAIL')
 
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'message':'Invalid Email address Format'}), 400
 
        #generate otp and send otp via Email
    otp = generate_otp()
    if send_otp_email(app, email, otp):
        expiry_time = datetime.now() + timedelta(minutes=5)
        session[email] = {
            'otp': otp,
            'otp_expiry': expiry_time,
            'email': email
        }
 
        print("session", session)
   
        return jsonify({'message': f'OTP Sent Successfully - {otp}'}), 200
    else:
        return jsonify({'error': 'Failed to send OTP'}), 500
 
 
 
 
 
### verify otp
def verifyotp():
    data = request.json
    email = data.get('EMAIL')
    user_otp = data.get('otp')
    print("session")
    if session:
        user_data = session.get(email)
        print("user_data", user_data)
        if user_data:
            stored_otp = user_data['otp']
            otp_expiry = user_data.get('otp_expiry').replace(tzinfo=None)   #remove timezone information
            current_time = datetime.now()
            print("otp_expiry",otp_expiry, "current_time",current_time)
            if stored_otp == user_otp:
                #check otp is expired
                if otp_expiry and current_time < otp_expiry:
                    return jsonify({"message": "OTP verified Successfully"}), 200
                else:
                    return jsonify({'message': "OTP has Expired"}), 500
            else:
                return jsonify({'message': "Invalid OTP. Please try again."}), 500
    else:
        return jsonify({'message': "No OTP found in the Session"}), 404
 
 
### New Password
def newpassword():
    data = request.json
    email = data.get('Email')
    PASSWORD = data.get('New_password')
    print("session", session)
 
    #update the user password in the database
    user = UserDetails.query.filter_by(EMAIL=email).first()
    if user:
        password_hash = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.PASSWORD = password_hash
        db.session.commit()
        return jsonify({'message': 'Password Reset Successfully'}), 200
    else:
        return jsonify({'error': 'user not found'}), 404
 