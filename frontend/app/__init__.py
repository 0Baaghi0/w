

from flask  import Flask
from flask_cors import CORS 

app=Flask(__name__)

from app import view

CORS(app)




import config
