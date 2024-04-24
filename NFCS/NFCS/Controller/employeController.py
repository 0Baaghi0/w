from ctypes import pythonapi
from io import BytesIO
from flask import Flask, request, jsonify, send_file
import mysql.connector
from sqlalchemy import Text, func
import win32com
from model.EmployeDetalies import *
from flask import jsonify, request
import bcrypt
import re
import pandas as pd 
from model.EmploymentDetaliess import EmploymentDetails
from model.LetterTemplates import LetterTemplates
from model.UserDetalies import UserDetails
import pandas as pd
from sqlalchemy.exc import IntegrityError
import re
import pythoncom

def register_employee_data():
    try:
        userEmail = 'prasad1@gmail.com'
        data = request.json
        print('data', data)
        user = UserDetails.query.filter_by(EMAIL = userEmail).one()
        print('user',user)
           
        required_fields = ['EMP_NO', 'FIRST_NAME', 'LAST_NAME', 'EMAIL_ADDRESS',
                           'DATE_OF_JOINING', 'DATE_OF_BIRTH','USER_ID']
        missing =[]
        for i in required_fields:
            if i not in data:
                missing.append(f'{i} is required')
                print("missing",missing)
        if missing:
            return jsonify ({'message':missing}),400
 
        EMP_NO = data.get('EMP_NO')
        EMAIL_ADDRESS = data.get('EMAIL_ADDRESS')
 
       
        # if EMP_NO and EmployeeDetails.query.filter_by(EMP_NO=EMP_NO).first():
            # return jsonify({'error': 'EMP_NO already exists'}), 400        
        # if EMAIL_ADDRESS and EmployeeDetails.query.filter_by(EMAIL_ADDRESS=EMAIL_ADDRESS).first():
        #     return jsonify({'error': 'Email already exists'}), 400
           # If EMAIL_ADDRESS exists, update EMP_NO with a predefined value
        if EMP_NO:
            dbdata = EmployeeDetails.query.filter_by(EMP_NO=EMP_NO).first()
            if EMAIL_ADDRESS and EmployeeDetails.query.filter_by(EMAIL_ADDRESS=EMAIL_ADDRESS).first():
                return jsonify({'error': 'Email already exists'}), 400
            if dbdata:
                dbdata.EMP_ID = data['EMP_ID']
                dbdata.EMP_NO = data['EMP_NO']
                dbdata.FIRST_NAME = data['FIRST_NAME']
                dbdata.LAST_NAME = data['LAST_NAME']
                dbdata.DATE_OF_JOINING = data['DATE_OF_JOINING']
                dbdata.DATE_OF_BIRTH = data['DATE_OF_BIRTH']
                dbdata.WORK_LOCATION = data.get('WORK_LOCATION')
                dbdata.WORKER_TYPE = data['WORKER_TYPE']

                dbdata.USER_ID = user.USER_ID
                dbdata.EFFECTIVE_END_DATE = "4712-12-31"
                dbdata.CREATED_BY = "HR"
                dbdata.LAST_UPDATED_BY = "HR"
                db.session.commit()
                return jsonify(f'{dbdata.EMAIL_ADDRESS}  updated Successfully'), 200
            # If EMAIL_ADDRESS doesn't exist, create a new record
        employee_data = EmployeeDetails(
            EMP_ID = data['EMP_ID'],
            EMP_NO=data['EMP_NO'],
            FIRST_NAME=data['FIRST_NAME'],
            LAST_NAME=data['LAST_NAME'],
            EMAIL_ADDRESS=EMAIL_ADDRESS,
            DATE_OF_JOINING=data['DATE_OF_JOINING'],
            DATE_OF_BIRTH=data['DATE_OF_BIRTH'],
            WORKER_TYPE=data['WORKER_TYPE'],

            WORK_LOCATION=data.get('WORK_LOCATION'),
            USER_ID=user.USER_ID,
        	EFFECTIVE_END_DATE = "4712-12-31",
            
            CREATED_BY="HR",
            LAST_UPDATED_BY="HR"
        )
             
        if 'MIDDLE_NAME' in data:
            employee_data.MIDDLE_NAME = data['MIDDLE_NAME']
       
        db.session.add(employee_data)
        db.session.commit()
       
        return jsonify({'message': 'Employee data added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

# def updateemployee
# def getemployee():
#     data = EmployeeDetails.query.all()
#     print(data)
#     returnData= []
#     for i in data:
#         returnData.append(i.serialize())
#     print('returnData',returnData)
#     return returnData


#bulk employees added excel sheet
def upload_excel():
    try:
        file = request.files['Excel']
        if not file:
            return jsonify({'error': 'No file'}), 400
 
        df = pd.read_excel(file)
        count = 0  
        required_fields = ['EMP_NO', 'FIRST_NAME', 'LAST_NAME', 'EMAIL_ADDRESS',
                           'DATE_OF_JOINING', 'DATE_OF_BIRTH']
        missing =[]
        for i in required_fields:
            if i not in df:
                missing.append(f'{i} is required')
                print("missing",missing)
        if missing:
            return jsonify({'message':missing}), 400
        details = []
        for index, row in df.iterrows():
            try:
                emp_no = row['EMP_NO']
                createdBy = 'HR'
                lastUpdatedBy = 'HR'
                existing_employee = EmployeeDetails.query.filter_by(EMP_NO=emp_no).first()
                
                if existing_employee:
                    # Skip to the next iteration if employee already exists
                    continue
                print(type(row.get('MIDDLE_NAME')))
                if row.get('MIDDLE_NAME') == 'str':
                    middleName = row['MIDDLE_NAME']
                else :
                    middleName = None
                employee = EmployeeDetails(
                    EMP_ID=row['EMP_ID'],
                    EMP_NO=emp_no,
                    FIRST_NAME=row['FIRST_NAME'],
                    MIDDLE_NAME=middleName,
                    LAST_NAME=row['LAST_NAME'],
                    EMAIL_ADDRESS=row['EMAIL_ADDRESS'],
                    DATE_OF_JOINING=row['DATE_OF_JOINING'],
                    DATE_OF_BIRTH=row['DATE_OF_BIRTH'],
                    LOCATION=row['LOCATION'],
                    USER_ID=row['USER_ID'],
                    EFFECTIVE_END_DATE='4712-12-31',
                    CREATED_BY=createdBy,
                    LAST_UPDATED_BY=lastUpdatedBy
                )
                db.session.add(employee)
                db.session.commit()
                count += 1  
                details.append(employee.serialize())
            except Exception as e:
                db.session.rollback()
                raise e  
 
        if count > 0:
            return jsonify({'message': f'{count}new employee(s) added successfully','data':details}), 200
        else:
            return jsonify({'message': 'All data already exists in the database'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

###filterDAta
def filter_employees(search_data):
    try:
        employee_list = []
        data = EmployeeDetails.query.filter(
            (EmployeeDetails.EMP_NO == search_data)|
            (func.lower(EmployeeDetails.FIRST_NAME).startswith(search_data.lower()))|      
            (func.lower(EmployeeDetails.LAST_NAME).startswith(search_data.lower()))|
            (func.lower(EmployeeDetails.EMAIL_ADDRESS).startswith(search_data.lower()))
        ).all()
        print("data",data)
        if not data:
            return jsonify({'message': 'No employees found for the given search criteria'}), 404
        for employee in data:
            employee_dict = {
            'EMP_NO': employee.EMP_NO,
            'FIRST_NAME': employee.FIRST_NAME,
            'LAST_NAME': employee.LAST_NAME,
            'EMAIL_ADDRESS':employee.EMAIL_ADDRESS,
            'DATE_OF_JOINING':employee.DATE_OF_JOINING,
            'DATE_OF_BIRTH':employee.DATE_OF_BIRTH,    
            'USER_ID':employee.USER_ID,
            'EFFECTIVE_END_DATE':employee.EFFECTIVE_END_DATE
            }
            employee_list.append(employee_dict)
        return jsonify(employee_list), 200 
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def file_convert():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400           
        ASSIGNMENT_ID, TEMPLATE_ID, ANNUAL_SALARY = data.get('ASSIGNMENT_ID'), data.get('TEMPLATE_ID'), data.get('ANNUAL_SALARY')      
        if not all([ASSIGNMENT_ID, TEMPLATE_ID, ANNUAL_SALARY]):
            return jsonify({'error': 'Missing required fields in JSON data'}), 400       
        employment_details = EmploymentDetails.query.get(ASSIGNMENT_ID)
        employee_details = EmployeeDetails.query.filter_by(EMP_ID=employment_details.EMP_ID).first()
        if employee_details:
            required_employee_fields = ['EMP_NO', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'EMAIL_ADDRESS',
            'DATE_OF_JOINING', 'DATE_OF_BIRTH', 'LOCATION', 'EFFECTIVE_START_DATE','EFFECTIVE_END_DATE']
            filee_info = {field: getattr(employee_details, field) for field in required_employee_fields}
            required_fields = ['ORGANIZATION_NAME', 'POSITION', 'DEPARTMENT', 'ANNUAL_SALARY','PREVIOUS_ANNUAL_SALARY', 
            'PROBATION_PERIOD', 'NOTICE_PERIOD','EMAIL', 'WORK_LOCATION', 'MOBILE_NO', 'EFFECTIVE_START_DATE', 'EFFECTIVE_END_DATE']
            file_info = {field: getattr(employment_details, field) for field in required_fields}
            dictt = {}
            Basic_Salary_year = ANNUAL_SALARY * 0.5
            dictt['Basic_Salary_year'] = f'{Basic_Salary_year:,.0f}'
            Basic_Salary_month = Basic_Salary_year // 12
            dictt['Basic_Salary_month'] = int(Basic_Salary_month)
            House_Rent_Allowance_year = Basic_Salary_year * 0.4
            dictt['House_Rent_Allowance_year'] = int(House_Rent_Allowance_year)
            House_Rent_Allowance_month = Basic_Salary_month * 0.4
            dictt['House_Rent_Allowance_month'] = int(House_Rent_Allowance_month)
            Special_Allowance_year = ANNUAL_SALARY - Basic_Salary_year - House_Rent_Allowance_year
            dictt['Special_Allowance_year'] = int(Special_Allowance_year)
            Special_Allowance_month = ANNUAL_SALARY // 12 - Basic_Salary_month - House_Rent_Allowance_month
            dictt['Special_Allowance_month'] = int(Special_Allowance_month)
            Gross_Compensation_year = Basic_Salary_year + House_Rent_Allowance_year + Special_Allowance_year
            dictt['Gross_Compensation_year'] = int(Gross_Compensation_year)
            Gross_Compensation_month = Basic_Salary_month + House_Rent_Allowance_month + Special_Allowance_month
            dictt['Gross_Compensation_month'] = int(Gross_Compensation_month)
            PF_month = 0 if Basic_Salary_month < 15000 else 1800
            dictt['PF_month'] = int(PF_month)
            PF_year = 0 if Basic_Salary_year < 180000 else 1800
            dictt['PF_year'] = int(PF_year)
            Total_Base_Compensation_year = Gross_Compensation_year + PF_year
            dictt['Total_Base_Compensation_year'] = int(Total_Base_Compensation_year)
            Total_Base_Compensation_month = Gross_Compensation_month + PF_month
            dictt['Total_Base_Compensation_month'] = int(Total_Base_Compensation_month)
            Gratuity_month = Basic_Salary_month * 4.81 / 100 
            dictt['Gratuity_month'] = int(Gratuity_month)
            Gratuity_year = Basic_Salary_year * 4.81 / 100
            dictt['Gratuity_year'] = int(Gratuity_year)
            Total_Cost_to_Company_year = Total_Base_Compensation_year + Gratuity_year
            dictt['Total_Cost_to_Company_year'] = f'{Total_Cost_to_Company_year:,.0f}'
            Total_Cost_to_Company_month = Total_Base_Compensation_month + Gratuity_month
            dictt['Total_Cost_to_Company_month'] = int(Total_Cost_to_Company_month)

            output_pdf = 'F:\\new\\n90.pdf'

            template = LetterTemplates.query.get(TEMPLATE_ID)
            if not template:
                return jsonify({'error': 'Template not found'}), 404
            rtf_content = template.TEMPLATE.decode('utf-8')
            file3 = rtf_content
            for key, value in file_info.items():
                file3 = re.sub(fr'\b{re.escape(key)}\b', str(value), file3)
            for key, value in filee_info.items():
                file3 = re.sub(fr'\b{re.escape(key)}\b', str(value), file3)
            for key, value in dictt.items():
                file3 = re.sub(fr'\b{re.escape(key)}\b', str(value), file3)
            file_name = f'F:\\file\\EMOLOYEE_{ASSIGNMENT_ID}.rtf'
            with open(file_name, 'wb') as file2:
                file2.write(file3.encode('utf-8'))         
            pythoncom.CoInitialize()
            word = win32com.client.Dispatch("Word.Application")
            doc = word.Documents.Open(os.path.abspath(file_name))
            doc.SaveAs(output_pdf, FileFormat=17)
            doc.Close()
            word.Quit()
            with open(output_pdf, 'rb') as file:
                file_contents = file.read()

        return send_file(BytesIO(file_contents), as_attachment=True, mimetype='application/pdf', download_name='n90.pdf')    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
