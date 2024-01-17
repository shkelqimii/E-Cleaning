from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS  
from flask import session
import os
import stripe


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  # mysecretkey passwordi osht
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://shkelqim:mysecretkey@localhost/mydatabase'
app.config['SESSION_TYPE'] = 'filesystem'

# Stripe configuration
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51O5ONQLYq60Cyx2yr9iBiyNAV6eDKD69hQzu8O0M41J7Rg2Jc7sdIkZvMyUkJt2o0sSo6h1RHXQuUtKqBcSkC6lX00by2EyHMc'  

# Initialize Stripe with your secret key
stripe.api_key = 'sk_test_51O5ONQLYq60Cyx2yr9iBiyNAV6eDKD69hQzu8O0M41J7Rg2Jc7sdIkZvMyUkJt2o0sSo6h1RHXQuUtKqBcSkC6lX00by2EyHMc'
  # <-- Set the Stripe API key


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Set up CORS to handle the Authorization header
cors = CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

# Move this to the bottom
from app import views, models
