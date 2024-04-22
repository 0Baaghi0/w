
from enum import unique
from config import *
from sqlalchemy import Column,String,Integer,Float
from datetime import datetime
from flask import Flask, request, jsonify





class Emp_Detalies(db.Model):
    __tablename__='emp_detalies'


    EMPLOYEE_NUMBER =db.Column(db.Integer,primary_key=True)
    FIRST_NAME=db.Column(db.String(225),nullable=False)
    LAST_NAME=db.Column(db.String(225),nullable=False)
    DATE_OF_BIRTH=db.Column(db.Date)
    # DATE_OF_BIRTH=db.Column(db.Date)
    LOCATION=db.Column(db.String(225),nullable=False)
    EMAIL=db.Column(db.String(225),unique=True ,nullable=False)
    
    # CREATED_BY = db.Column(db.String(255), nullable=False)
    # LAST_UPDATED_BY = db.Column(db.String(255), nullable=False)
    CREATION_DATE = db.Column(db.DateTime, default=datetime.now, nullable=False)
    LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    





    def serialize(self):
        return {
            'EMPLOYEE_NUMBER': self.EMPLOYEE_NUMBER,
            'FIRST_NAME': self.FIRST_NAME,
            'DATE_OF_BIRTH': self.DATE_OF_BIRTH,
            'LAST_NAME':self.LAST_NAME,
            'EMAIL':self.EMAIL,    
            'LOCATION':self.LOCATION,
            'CREATION_DATE':self.CREATION_DATE.strftime('%Y-%m-%d %H:%M:%S'),
            'LAST_UPDATED_DATE': self.LAST_UPDATED_DATE.strftime('%Y-%m-%d %H:%M:%S')
            
            }

#=============================================================================================
def getemployee():
    data = Emp_Detalies.query.all()
    print(data)
    returnData= []
    for i in data:
        returnData.append(i.serialize())
    print('returnData',returnData)
    return returnData

def getemployeeId(CANDIDATE_ID):
    data = Emp_Detalies.query.get(CANDIDATE_ID)
    new={'CANDIDATE_ID': data.CANDIDATE_ID,
            'CANDIDATE_NAME': data.CANDIDATE_NAME,
            'DATE_OF_BIRTH': data.DATE_OF_BIRTH,
            'MOBILE_NO':data.MOBILE_NO,
            'EMAIL':data.EMAIL,
            'POSITION':data.POSITION,
            'COMPANY_NAME':data.COMPANY_NAME,
            'LOCATION':data.LOCATION,
            'SALARY':data.SALARY,
            'CREATED_BY': data.CREATED_BY,
            'LAST_UPDATED_BY': data.LAST_UPDATED_BY
         }
    return new

def deleteemployee(CANDIDATE_ID):
    try:
        employees=Emp_Detalies.query.get(CANDIDATE_ID)
        print("gghah",employees)
        if not employees:
            return jsonify({'message':'employees not found'}),404
        db.session.delete(employees)
        db.session.commit()
        return jsonify({'message':f'employee {id} deleted succesfully','data':employees.serialize()}),200
    except Exception as err:
        return jsonify({'err':str(err)}),500
    

def updateemployee(CANDIDATE_ID):
    try:
        data=request.json
        employees=Emp_Detalies.query.get(CANDIDATE_ID)
        for field in data.keys():
            new_value=data.get(field)
            if getattr(employees,field)!=new_value:
                setattr(employees,field,new_value)
        db.session.commit()
        return jsonify({'message':employees.serialize()})
    except Exception as e:
        return jsonify({'e':str(e)}),500









































    # Employee_Reference_Number=db.Column(db.String(225),nullable=False)
    # Gender=db.Column(db.String(225),nullable=False)
    # confirmdate=db.Column(db.Date,nullable=False)
    # Nick_Name=db.Column(db.String(225),nullable=False)
    # Extension_Number=db.Column(db.Integer,nullable=False)
    # First_Name=db.Column(db.String(225),nullable=False)
    # Middle_Name=db.Column(db.String(225),nullable=False)
    # Last_Name=db.Column(db.String(225),nullable=False)
    # Email_Address=db.Column(db.String(225),nullable=False)
    # Personal_Email_Address=db.Column(db.String(225),nullable=False)
    # PAN_Number=db.Column(db.String(225),nullable=False)
    # Marital_Status=db.Column(db.String(225),nullable=False)

    # Marriage_Date=db.Column(db.Date,nullable=False)
    # Blood_Group=db.Column(db.String(225),nullable=False)
    # WORKINManagers_Employee_No=db.Column(db.String(225),nullable=False)
    # Fathers_Name=db.Column(db.String(225),nullable=False)
    # spousename=db.Column(db.String(225),nullable=False)
    # ipaddress=db.Column(db.String(225),nullable=False)
    # Login_User_Name = db.Column(db.String(255), nullable=False)
    # Probation_Period = db.Column(db.String(255), nullable=False)

    # Notice_Period=db.Column(db.String(225),nullable=False)
    # Is_Physical_Challanged=db.Column(db.Integer,nullable=False)
    # Is_International_Employee=db.Column(db.Integer,nullable=False)
    # Background_Check_Status=db.Column(db.String(255),nullable=False)
    # Background_Verification_Completed_On=db.Column(db.Date,nullable=False)
    # Agency_Name=db.Column(db.String(225),nullable=False)
    # Background_Check_Remarks = db.Column(db.String(255), nullable=False)
    # Emergency_Contact_Name = db.Column(db.String(255), nullable=False)

    # Emergency_Contact_Number=db.Column(db.Integer,nullable=False)
    # Bank_Account_Number=db.Column(db.Integer,nullable=False)
    # IFSC_Code=db.Column(db.String(225),nullable=False)
    # Bank_Account_Type=db.Column(db.String(225),nullable=False)
    # Bank_Name=db.Column(db.String(225),nullable=False)
    # Bank_Branch=db.Column(db.String(225),nullable=False)

    # Salary_Payment_Mode=db.Column(db.String(225),)
    # DD_Payable_At =db.Column(db.String(225))
    # Name_As_Per_Bank_Records=db.Column(db.String(225))
    # IBAN=db.Column(db.Float(8,2))
    # Is_employee_eligible_for_PF=db.Column(db.String(225))
    # PF_Number=db.Column(db.String(225))

    # PF_Scheme=db.Column(db.String(225),primary_key=True)
    # PF_Joining_Date=db.Column(db.String(225))
    # Is_employee_eligible_for_excess_EPF_contribution=db.Column(db.String(225))
    # Is_employee_eligible_for_excess_EPS_contribution=db.Column(db.Float(8,2))
    # Is_existing_member_of_PF=db.Column(db.String(225))
    # Is_employee_eligible_for_ESI=db.Column(db.String(225))


    # ESI_Number=db.Column(db.String(225),primary_key=True)
    # Is_employee_covered_under_LWF=db.Column(db.String(225))
    # Aadhaar_Card_Enrolment_No=db.Column(db.String(225))
    # Name_As_on_Aadhaar_Card=db.Column(db.Float(8,2))
    # Aadhaar_Card_Number =db.Column(db.String(225))
    # Universal_Account_Number=db.Column(db.String(225))
    # Mobile_Number = db.Column(db.String(255), nullable=False)


    # Country_Of_Origin=db.Column(db.String(225),primary_key=True)
    # Designation=db.Column(db.String(225))
    # Department=db.Column(db.String(225))
    # Location=db.Column(db.Float(8,2))

    # CREATED_BY = db.Column(db.String(255), nullable=False)
    # LAST_UPDATED_BY = db.Column(db.String(255), nullable=False)
    # CREATION_DATE = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # LAST_UPDATED_DATE = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    


    # def serialize(self):
    #     return {
    #         'AGENT_CODE': self.AGENT_CODE,
    #         'AGENT_NAME': self.AGENT_NAME,
    #         'WORKING_AREA': self.WORKING_AREA,
    #         'COMMISSION':self.COMMISSION,
    #         'PHONE_NO':self.PHONE_NO,
    #         'COUNTRY':self.COUNTRY,
    #         'CREATED_BY': self.CREATED_BY,
    #         'LAST_UPDATED_BY': self.LAST_UPDATED_BY,
    #         'CREATION_DATE':self.CREATION_DATE.strftime('%Y-%m-%d %H:%M:%S'),
    #         'LAST_UPDATED_DATE': self.LAST_UPDATED_DATE.strftime('%Y-%m-%d %H:%M:%S')
            
    #         }


