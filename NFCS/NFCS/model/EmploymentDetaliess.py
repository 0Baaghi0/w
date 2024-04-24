
from config import *
from sqlalchemy import Column,String,Integer
from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy.orm import relationship



class EmploymentDetails(db.Model):
    __tablename__ = 'employment_details'

    ASSIGNMENT_ID = db.Column(db.Integer, primary_key=True)
    ORGANIZATION_NAME = db.Column(db.String(225), nullable=False)
    POSITION = db.Column(db.String(225), nullable=False)
    DEPARTMENT = db.Column(db.String(225), nullable=False)
    ANNUAL_SALARY = db.Column(db.Float)
    PREVIOUS_ANNUAL_SALARY = db.Column(db.Float)
    EMAIL = db.Column(db.String(225), unique=True)
    WORK_LOCATION = db.Column(db.String(225), nullable=False)
    MOBILE_NO = db.Column(db.BigInteger, nullable=False)
    PROBATION_PERIOD = db.Column(db.Integer)
    NOTICE_PERIOD = db.Column(db.Integer)
    CONFIRMATION_DATE =db.Column(db.Date)
    EFFECTIVE_START_DATE = db.Column(db.TIMESTAMP)
    EFFECTIVE_END_DATE = db.Column(db.DateTime)
    EMP_ID = db.Column(db.Integer, db.ForeignKey('employee_details.EMP_ID'))
    CREATED_BY = db.Column(db.String(225), nullable=False)
    LAST_UPDATED_BY = db.Column(db.String(225), nullable=False)
    CREATED_AT = db.Column(db.DateTime, default=datetime.now, nullable=False)
    LAST_UPDATED_AT = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    

    # employee = relationship("EmployeeDetails", back_populates="employment_details")

    def serialize(self):
        serialized_data = {
            "ASSIGNMENT_ID": self.ASSIGNMENT_ID,
            "ORGANIZATION_NAME": self.ORGANIZATION_NAME,
            "POSITION": self.POSITION,
            "DEPARTMENT": self.DEPARTMENT,
            "ANNUAL_SALARY": self.ANNUAL_SALARY,
            "PREVIOUS_ANNUAL_SALARY": self.PREVIOUS_ANNUAL_SALARY,
            "EMAIL": self.EMAIL,
            "WORK_LOCATION": self.WORK_LOCATION,
            "MOBILE_NO": self.MOBILE_NO,
            "PROBATION_PERIOD": self.PROBATION_PERIOD,
            "NOTICE_PERIOD": self.NOTICE_PERIOD,
            "EFFECTIVE_START_DATE": str(self.EFFECTIVE_START_DATE),
            "EFFECTIVE_END_DATE": str(self.EFFECTIVE_END_DATE),
            "EMP_ID": self.EMP_ID,
            "CREATED_BY": self.CREATED_BY,
            "LAST_UPDATED_BY": self.LAST_UPDATED_BY
        }
        return serialized_data