from config import *
from sqlalchemy import Column, LargeBinary,String,Integer
from datetime import datetime
from flask import Flask, make_response, render_template, request, jsonify, send_file
from sqlalchemy.orm import relationship

#===========================================================================================



class EmployeeAddressDetails(db.Model):
    __tablename__ = 'employee_address_details'

    ADDRESS_ID = db.Column(db.Integer, primary_key=True)
    EMP_ID = db.Column(db.Integer, db.ForeignKey('employee_details.EMP_ID'))
    ADDRESS_TYPE = db.Column(db.String(225), nullable=False)
    ADDRESS = db.Column(db.String(225), nullable=False)
    CITY = db.Column(db.String(225), nullable=False)
    STATE = db.Column(db.String(225), nullable=False)
    COUNTRY = db.Column(db.String(225), nullable=False)
    PIN_CODE = db.Column(db.Integer, nullable=False)
    DATE_FROM = db.Column(db.TIMESTAMP)
    DATE_TO = db.Column(db.TIMESTAMP)
    PHONE_1 = db.Column(db.String(225))
    PHONE_2 = db.Column(db.String(225))
    CREATED_BY = db.Column(db.String(225), nullable=False)
    LAST_UPDATED_BY = db.Column(db.String(225), nullable=False)
    CREATED_AT = db.Column(db.DateTime, default=datetime.now, nullable=False)
    LAST_UPDATED_AT = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    

    # employee = relationship("EmployeeDetails", back_populates="address_details")

    def serialize(self):
        serialized_data = {
            "ADDRESS_ID": self.ADDRESS_ID,
            "EMP_ID": self.EMP_ID,
            "ADDRESS_TYPE": self.ADDRESS_TYPE,
            "ADDRESS": self.ADDRESS,
            "CITY": self.CITY,
            "STATE": self.STATE,
            "COUNTRY": self.COUNTRY,
            "PIN_CODE": self.PIN_CODE,
            "DATE_FROM": str(self.DATE_FROM),
            "DATE_TO": str(self.DATE_TO),
            "PHONE_1": self.PHONE_1,
            "PHONE_2": self.PHONE_2,
            "CREATED_BY": self.CREATED_BY,
            "LAST_UPDATED_BY": self.LAST_UPDATED_BY
            
        }
        return serialized_data