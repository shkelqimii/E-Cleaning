from email.policy import default
from itertools import product
from tarfile import data_filter
from sqlalchemy import Nullable
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active')  # 'active', 'deactive', 'none'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    original_price = db.Column(db.Float, nullable=True)  # new field to store the original price
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    quantity = db.Column(db.Integer, nullable=False, default=0)




class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='SET NULL'), nullable=True)  # Add ondelete='SET NULL'
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_user_created = db.Column(db.Boolean, default=False, nullable=False)
    description = db.Column(db.Text)



    def __repr__(self):
        return f'<Notification {self.action} by User {self.user_id} on Product {self.product_id}>'
    

class SimpleNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<SimpleNotification {self.creator} on {self.date}>'


class WashproductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    washproduct_id = db.Column(db.Integer, db.ForeignKey('washproducts.id'), nullable=False)

class Washproducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    images = db.relationship('WashproductImage', backref='washproduct', lazy=True, cascade='all, delete-orphan')



class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(120), unique=True, nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    valid_duration = db.Column(db.Integer, default=30)  # Duration in minutes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to User model

    user = db.relationship('User', backref='qrcodes')  # Relationship with User

    def is_valid(self):
        return datetime.utcnow() < self.creation_time + timedelta(minutes=self.valid_duration)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
