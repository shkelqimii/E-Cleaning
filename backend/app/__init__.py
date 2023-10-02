from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS  
from flask import session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  # mysecretkey passwordi
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://shkelqim:mysecretkey@localhost/mydatabase'
app.config['SESSION_TYPE'] = 'filesystem'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Set up CORS to handle the Authorization header
from flask_cors import CORS

cors = CORS(app, origins=["http://localhost:5173"], supports_credentials=True)




from app import views, models