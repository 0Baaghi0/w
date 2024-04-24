from flask import Flask, request, jsonify
import mysql.connector
from sqlalchemy import Text, func
from config import *
from model.EmployeDetalies import *
from model.EmploymentDetaliess import *

def add_employment_details():
    try:
        data = request.json
        print('data-->', data)
        emp_id = data.get('EMP_ID')
        employee = EmployeeDetails.query.get(emp_id)
        if not employee:
            return jsonify({'error': 'Employee does not exist'}), 400
        email = data.get('EMAIL')
        existing_employment = EmploymentDetails.query.filter_by(EMAIL=email).first()
        if existing_employment:
            return jsonify({'error': 'Email already exists'}), 400
        employment_data = EmploymentDetails(
            ASSIGNMENT_ID=data['ASSIGNMENT_ID'],
            ORGANIZATION_NAME=data['ORGANIZATION_NAME'],
            POSITION=data['POSITION'],
            DEPARTMENT=data['DEPARTMENT'],
            ANNUAL_SALARY=data['ANNUAL_SALARY'],
            PREVIOUS_ANNUAL_SALARY=data['PREVIOUS_ANNUAL_SALARY'],
            EMAIL=email,
            WORK_LOCATION=data['WORK_LOCATION'],
            MOBILE_NO=data['MOBILE_NO'],
            PROBATION_PERIOD=data['PROBATION_PERIOD'],
            NOTICE_PERIOD=data['NOTICE_PERIOD'],
            EFFECTIVE_START_DATE=data['EFFECTIVE_START_DATE'],
            EFFECTIVE_END_DATE="4712-12-31",
            EMP_ID=emp_id,
            CREATED_BY="HR",
            LAST_UPDATED_BY="HR"
        )
        db.session.add(employment_data)
        db.session.commit()
        return jsonify({'message': 'Employment details added successfully', 'data': employment_data.serialize()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
