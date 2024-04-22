from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app
from flask_bcrypt import Bcrypt
from flask_mail import Mail

cors = CORS(app)
 

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:rajeev@localhost/end'#4-2-2024'
db = SQLAlchemy(app)
migrate=Migrate(app, db)



# bcrypt = Bcrypt()
# #config
# app.secret_key = 'os.urandom(24)'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sql12@localhost/offletter'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'sample11nhr5@gmail.com'
# app.config['MAIL_PASSWORD'] = 'dzvo yxnb iftp sgaq'
 
# mail = Mail(app)
# bcrypt = Bcrypt(app)