from sqlite3 import IntegrityError
from flask import Flask, request, jsonify
import mysql.connector
from sqlalchemy import Text, func
from model.EmpData import *
from config import *
from sqlalchemy.exc import IntegrityError
import pandas as pd


def addempdata():
    try:
        data = request.json
        print('data-->',data)
       
        emp_data=Emp_Detalies(
                            EMPLOYEE_NO=data['EMPLOYEE_NUMBER'],
                            FIRST_NAME=data['FIRST_NAME'],
                            LAST_NAME=data['LAST_NAME'],
                            # DATE_OF_JOINING=data['DATE_OF_JOINING'],
                            DATE_OF_BIRTH=data['DATE_OF_BIRTH'],
                            EMAIL=data['EMAIL'],
                            LOCATION=data['LOCATION'],
                            # CREATED_BY=data['CREATED_BY'],
                            # LAST_UPDATED_BY=data['LAST_UPDATED_BY']
                             )
        db.session.add(emp_data)
        db.session.commit()

        return jsonify({'message':'employee data added succesfully','data':emp_data.serialize()}),201
    except Exception as e:
        return jsonify({'error':str(e)}),500
    


def getemployee():
    data = Emp_Detalies.query.all()
    print(data)
    returnData= []
    for i in data:
        returnData.append(i.serialize())
    print('returnData',returnData)
    return returnData


def getemployeeId(EMPLOYEE_NUMBER):
    data = Emp_Detalies.query.get(EMPLOYEE_NUMBER)
    if data:
        new = {
            'EMPLOYEE_NO': data.EMPLOYEE_NUMBER,
            'FIRST_NAME': data.FIRST_NAME,
            'DATE_OF_BIRTH': data.DATE_OF_BIRTH,
            'LAST_NAME': data.LAST_NAME,
            'EMAIL': data.EMAIL,    
            'LOCATION': data.LOCATION,
        }
        return new
    else:
        return None

def deleteemployee(EMPLOYEE_NUMBER):
    try:
        employees=Emp_Detalies.query.get(EMPLOYEE_NUMBER)
        print("gghah",employees)
        if not employees:
            return jsonify({'message':'employees not found'}),404
        db.session.delete(employees)
        db.session.commit()
        return jsonify({'message':f'employee {id} deleted succesfully','data':employees.serialize()}),200
    except Exception as err:
        return jsonify({'err':str(err)}),500
   
 
def updateemployee(EMPLOYEE_NUMBER):
    try:
        data=request.json
        employees=Emp_Detalies.query.get(EMPLOYEE_NUMBER)
        for field in data.keys():
            new_value=data.get(field)
            if getattr(employees,field)!=new_value:
                setattr(employees,field,new_value)
        db.session.commit()
        return jsonify({'message':employees.serialize()})
    except Exception as e:
        return jsonify({'e':str(e)}),500
 
 
#FILTER THE COLUMNS IN CONDITION
def filter_employees(search_data):
    try:
        employee_list = []
        employees = Emp_Detalies.query.filter(
            (Emp_Detalies.EMPLOYEE_NUMBER == search_data) |
            (func.lower(Emp_Detalies.FIRST_NAME).startswith(search_data.lower()))|        #like(f'%{search_data.lower()}%')
            (func.lower(Emp_Detalies.LAST_NAME).startswith(search_data.lower()))|
            (func.lower(Emp_Detalies.EMAIL).startswith(search_data.lower()))
        ).all()
        if not employees:
            return jsonify({'message': 'No employees found for the given search criteria'}), 404
        for employee in employees:
            employee_dict = {
            'EMPLOYEE_NO': employee.EMPLOYEE_NUMBER,
            'FIRST_NAME': employee.FIRST_NAME,
            'DATE_OF_BIRTH': employee.DATE_OF_BIRTH,
            'LAST_NAME':employee.LAST_NAME,
            'EMAIL':employee.EMAIL,    
            'LOCATION':employee.LOCATION
            }
            employee_list.append(employee_dict)
        return jsonify(employee_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def upload_excel():
    try:
        file = request.files['hllo']
        if not file:
            return jsonify({'error': 'No file'}), 400
 
        df = pd.read_excel(file)
        count = 0  
        for index, row in df.iterrows():
            try:
                employee_number = row['EMPLOYEE_NUMBER']
               
                existing_employee = Emp_Detalies.query.filter_by(EMPLOYEE_NUMBER=employee_number).first()
                if existing_employee:
                    continue  
                employee = Emp_Detalies(
                    EMPLOYEE_NO=employee_number,
                    FIRST_NAME=row['FIRST_NAME'],
                    LAST_NAME=row['LAST_NAME'],
                    DATE_OF_BIRTH=row['DATE_OF_BIRTH'],
                    EMAIL=row['EMAIL'],
                    LOCATION=row['LOCATION']
                )
                db.session.add(employee)
                db.session.commit()
                count += 1  
            except Exception as e:
                db.session.rollback()
                raise e  
 
        if count > 0:
            return jsonify({'message': f'{count} new employee(s) added successfully'}), 201
        else:
            return jsonify({'message': 'All data already exists in the database'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    

