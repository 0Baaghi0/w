from flask import Flask, request, jsonify
import mysql.connector
from model.LetterTemplate import *
from datetime import datetime
from flask import make_response
import io  
from sqlalchemy import text
# import comtypes.client
# import pdfkit
from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import SimpleDocTemplate, Paragraph
import os
import base64
import tempfile
from flask import send_file
import pythoncom
import win32com.client
import mimetypes
from mimetypes import guess_type

def addtemplate1():
    try:
        file = request.files['TEMPLATE']
        template_name = request.form['TEMPLATE_NAME']
        temp = file.read()
        template_type = file.mimetype
        existing_template = LetterTemplates.query.filter_by(TEMPLATE_NAME=template_name).first()
        if existing_template:
            # Update the existing template
            existing_template.TEMPLATE_TYPE = template_type
            existing_template.FILE_SIZE = len(temp)
            existing_template.TEMPLATE = temp
            existing_template.LAST_UPDATED_BY = 'HR'
        else:   
            max_id = db.session.query(db.func.max(LetterTemplates.TEMPLATE_ID)).scalar() or 0
            new_id = max_id + 1

            # Creating a new LetterTemplates instance with the determined ID and adding it to the database
            new_template = LetterTemplates(
                TEMPLATE_ID=new_id,
                TEMPLATE_NAME=template_name,
                TEMPLATE_TYPE=template_type,
                FILE_SIZE=len(temp),
                TEMPLATE=temp,
                CREATED_BY='HR',
                LAST_UPDATED_BY='HR'
            )
            db.session.add(new_template)

        db.session.commit()
        
        return jsonify({'message': 'Template uploaded successfully'}), 200
    except Exception as e:
        # Handling exceptions
        return jsonify({'error': str(e)}), 500



 
def getTemplateById(TEMPLATE_ID):
    try:
       
        data = LetterTemplates.query.get(TEMPLATE_ID)
        if data:
            print("data", data)
            file_data = data.TEMPLATE
            response = make_response(file_data)
            response.headers.set('Content-Disposition', 'inline',  TEMPLATE_NAME = 'filename.rtf')
            response.headers.set('Content-Type', 'application/rtf')
            return response
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error':str(e)}), 500



 
def convertrtf(TEMPLATE_ID):
    try:
        temp = LetterTemplates.query.filter(LetterTemplates.TEMPLATE_ID==TEMPLATE_ID).one()
        print("temp",temp)
        x = temp.TEMPLATE
        print("x",x)
       
 
        file_obj = BytesIO(x)
 
        rtf_file_name = 'rtffile.rtf'
        pdf_file_name = 'pdffile.pdf'
        rtf_file_path = os.path.join(os.getcwd(), rtf_file_name)
        print("rtf_file_path",rtf_file_path)
        with open(rtf_file_path, 'wb') as file:
                file.write(file_obj.read())
        pythoncom.CoInitialize()
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(rtf_file_path)
       
        pdfpath = os.path.join(os.getcwd(), pdf_file_name)
        doc.SaveAs(pdfpath, FileFormat=17)
        print("pdfpath",pdfpath)
        doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()
        os.remove(rtf_file_path)
 
        with open ('C:\\w\\frontend\\pdffile.pdf','rb') as file:
            a = file.read()
 
        file_obj = BytesIO(a)
        mimetype = mimetypes.MimeTypes().guess_type(pdf_file_name)[0]
        os.remove(pdfpath)
    # Return the file as a response
        return send_file(file_obj, mimetype=mimetype)    
    except Exception as e:
        return jsonify({'error':str(e)}),500