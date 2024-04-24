from flask import jsonify, request

# from model.UserDetalies import *
# from model.EmployeDetalies import *
from model.EmployeeLetters import *
# from model.LetterTemplates import *
from datetime import datetime

from model.LetterTemplates import LetterTemplates





def add_employee_letter():
    try:
        data = request.json
        print('data', data)
        emp_id = data.get('EMP_ID')
        employee = EmployeeLetters.query.get(emp_id)
        if not employee:
            return jsonify({'error': 'Employee does not exist'}), 400
        
        template_id = data.get('TEMPLATE_ID')
        template = LetterTemplates.query.get(template_id)
        if not template:
            return jsonify({'error': 'Template does not exist'}), 400

        letter_data = EmployeeLetters(
            EMP_ID=emp_id,
            TEMPLATE_ID=template_id,
            LETTER_TYPE=data['LETTER_TYPE'],
            LETTER=data['LETTER'],  
            CREATED_BY="HR",
            LAST_UPDATED_BY="HR"
        )
        db.session.add(letter_data)
        db.session.commit()
        return jsonify({'message': 'Employee letter added successfully', 'data': letter_data.serialize()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

