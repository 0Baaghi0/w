from app import app
from Controller.EmpDataController import *
from Controller.userdetaliescontroller import *
from Controller.LetterTemplateController import *


#ADD NEW EMPDATA STORE IN DATABASE
@app.route('/adddata',methods=['POST'])
def new_project():
    return addempdata()


@app.route('/uplodeexcel',methods=['POST'])
def project():
    return upload_excel()

#register get method
@app.route('/getemployees',methods=['GET'])
def getregister():
    return getemployee()
 
#register id get  method
@app.route('/getemployee/getById/<EMPLOYEE_NUMBER>',methods=['GET'])
def getById(EMPLOYEE_NUMBER):
    print(type(EMPLOYEE_NUMBER))    
    return getemployeeId(EMPLOYEE_NUMBER)
 
#register delete method
@app.route('/getdeleteid/<EMPLOYEE_NUMBER>',methods=['DELETE'])
def getdeleteById(EMPLOYEE_NUMBER):
    return deleteemployee(EMPLOYEE_NUMBER)
 
#register update method
@app.route('/updateid/<EMPLOYEE_NUMBER>',methods=['PUT'])
def updateid(EMPLOYEE_NUMBER):
    return updateemployee(EMPLOYEE_NUMBER)
 
 
#FILTER THE COLUMNS IN CONDITION
@app.route('/getemployee/filterEmployees/<search_data>',methods=['GET'])
def fillters(search_data):
    return filter_employees(search_data)







#=========================================================================

#REGISTER DETAILS
@app.route('/register',methods=['POST'])
def regi():
    return register_user_data()
 
#LOGIN DETAILS
@app.route('/login',methods=['POST'])
def logi():
    return login()


 
#register get method
@app.route('/getregister',methods=['GET'])
def getregisters():
    return getemployees()
 
# #register id get  method
# @app.route('/getbyId/<USER_ID>',methods=['GET'])
# def getById(USER_ID):
#     print(type(USER_ID))
#     return getemployeeId(USER_ID)
 
# #register delete method
# @app.route('/getdeleteid/<USER_ID>',methods=['DELETE'])
# def getdeleteById(USER_ID):
#     return deleteemployee(USER_ID)
 
#register update method
# @app.route('/updateid/<USER_ID>',methods=['PUT'])
# def updateid(USER_ID):
#     return updateemployee(USER_ID)
 
 
# #Forgetting Password
# @app.route('/forgetpassword', methods=['POST'])
# def forget_password():
#     return forgetpassword()
 
 
# #verify otp
# @app.route('/verifyotp', methods=['POST'])
# def verify_otp():
#     return verifyotp()
 
 
# ##newpassword
# @app.route('/newpassword', methods = ['PUT'])
# def new_password():
#     return newpassword()
 
@app.route('/uploadTemplate', methods=['POST'])
def upload_Template():
    return addtemplate1()



@app.route('/getTemplateNames', methods=['GET'])
def get_all_template():
    return get_all_template_names()



@app.route('/getTemplateById/<TEMPLATE_ID>',methods=['GET'])
def get_Template_By_Id(TEMPLATE_ID):
    print(type(TEMPLATE_ID))
    return getTemplateById(TEMPLATE_ID)
@app.route('/convert_rtf/<string:Id>', methods=['GET'])
def convert_rtf(Id):
    print("sdfghjgvyvb")
    return convertrtf(Id)
