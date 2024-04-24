import io
from flask import Flask, make_response, render_template, request, jsonify, send_file
import mysql.connector
from sqlalchemy import Text
from config import db
from model.EmpAddrDetaliess import *
from model.EmployeDetalies import EmployeeDetails


def add_employee_address():
    try:
        data = request.json
        print('data-->', data)
        emp_id = data.get('EMP_ID')
        employee = EmployeeDetails.query.get(emp_id)
        if not employee:
            return jsonify({'error': 'Employee does not exist'}), 400
        address_id = data.get('ADDRESS_ID')
        address = EmployeeAddressDetails.query.filter_by(ADDRESS_ID=address_id).first()
        if address:
            return jsonify({'error': 'Address ID already exists'}), 400
        address_data = EmployeeAddressDetails(
            EMP_ID=emp_id,
            ADDRESS_ID=address_id,
            ADDRESS_TYPE=data['ADDRESS_TYPE'],
            ADDRESS=data['ADDRESS'],
            CITY=data['CITY'],
            STATE=data['STATE'],
            COUNTRY=data['COUNTRY'],
            PIN_CODE=data['PIN_CODE'],
            DATE_FROM=data['DATE_FROM'],
            DATE_TO=data['DATE_TO'],
            PHONE_1=data['PHONE_1'],
            PHONE_2=data['PHONE_2'],
            CREATED_BY="HR",
            LAST_UPDATED_BY="HR"
        )
        db.session.add(address_data)
        db.session.commit()
        return jsonify({'message': 'Employee address data added successfully', 'data': address_data.serialize()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
