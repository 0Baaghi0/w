from app import app

from Controller.UserDetaliesController import *
from Controller.employeController import *
from Controller.EmployementDetaliesController import *
from Controller.empAddrController import *
from Controller.LetterTemplateController import *
from Controller.EmployeeLettersController import *

#REGISTER DETAILS
@app.route('/register',methods=['POST'])
def register():
    return register_data()

#LOGIN DETAILS
@app.route('/login',methods=['POST'])
def login():
    return login_user()

#register get method
@app.route('/getregister',methods=['GET'])
def getregister():
    return getemployee()

#register id get  method
@app.route('/getbyId/<USER_ID>',methods=['GET'])
def getById(USER_ID):
    print(type(USER_ID))
    return getemployeeId(USER_ID)

#register delete method
@app.route('/getdeleteid/<USER_ID>',methods=['DELETE'])
def getdeleteById(USER_ID):
    return deleteemployee(USER_ID)

#register update method
@app.route('/updateid/<USER_ID>',methods=['PUT'])
def updateid(USER_ID):
    return updateemployee(USER_ID)


#Forgetting Password
@app.route('/forgetpassword', methods=['POST'])
def forget_password():
    return forgetpassword()
 
 
#verify otp
@app.route('/verifyotp', methods=['POST'])
def verify_otp():
    return verifyotp()
 
 
##newpassword
@app.route('/newpassword', methods = ['PUT'])
def new_password():
    return newpassword()


###register add employees
@app.route('/registeremployee', methods=['POST'])
def register_employee():
    return register_employee_data()


##upload excel sheet
@app.route('/uploadexcel', methods=['POST'])
def upload():
    return upload_excel()

##filterData
@app.route('/filterEmployees/<search_data>',methods=['GET'])
def fillters(search_data):
    return filter_employees(search_data)


############ LetterTemplate
### upload rtf file
@app.route('/uploadTemplate', methods=['POST'])
def upload_Template():
    return uploadTemplate()


#### update template
@app.route('/update_template/<int:id>', methods = ['PUT'])
def update_Template(id):
    return updatetemplate(id)


@app.route('/retrieve_template/<string:Id>', methods=['GET'])
def retrieve_template(Id):
    print("data")
    return temp(Id)


# convertpdf
@app.route('/convert_rtf/<string:Id>', methods=['GET'])
def convert_rtf(Id):
    print("sdfghjgvyvb")
    return convertrtf(Id)
 
 
 

@app.route('/add_employment_details', methods=['POST'])
def add_employment_detailss():
    return add_employment_details()



@app.route('/filess',methods=['POST'])
def filess():
    return file_convert()