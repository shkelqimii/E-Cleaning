from argparse import Action
from crypt import methods
from email import message
from http import client
import ntpath
from tkinter.tix import Tree
from MySQLdb import Timestamp
from flask import jsonify, request, url_for
from app import app, db
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from .models import *
import stripe
from flask import session
from flask_login import current_user
from .models import CartItem
from flask_login import login_required, current_user
from .models import Cart, CartItem, Product
from .decorators import *









# _________________________________________________________________________________________________________________________________________________________
#                                                            METODA PER REGJISTRIM TE USERIT
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/register', methods=['POST'])
@login_required
@admin_or_worker_required
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(success=False, message="Username already taken."), 400

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(success=True, message="Registration successful!")

# ____________________________________________________________________________________________________________________________________________________________________________________________
#                                                                   METODA PER LOGIN TE USERIT
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        if user.status == 'deactive':
            return jsonify(success=False, message="This account is deactivated."), 403
        login_user(user)
        return jsonify(success=True, message="Login successful!")
    else:
        return jsonify(success=False, message="Invalid username or password."), 401



# ____________________________________________________________________________________________________________________________________________________________________________________________
#                                                                           HOMEPAGE
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/index')
@login_required
def index():
    return jsonify(message="Hello World!")

# logout metoda
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(success=True, message="Logged out successfully!")

# ____________________________________________________________________________________________________________________________________________________________________________________________
#                                                                     PROFILI I USERIT
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# metoda e shikimit te informatave  te veta te userit

@app.route('/user_details', methods=['GET'])
@login_required
def get_user_details():
    print("Is authenticated:", current_user.is_authenticated)
    print("Current user:", current_user.username)
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'role': current_user.role
    }
    return jsonify(user_data)

# metoda qe useri me ndryshu vet passwordin e vet

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify(success=False, message="Both old and new passwords are required."), 400

    # Check if the old password is correct
    if current_user.check_password(old_password):
        # Set the new password
        current_user.set_password(new_password)
        db.session.commit()
        return jsonify(success=True, message="Password successfully updated!")
    else:
        return jsonify(success=False, message="Incorrect old password."), 401
    
# ______________________________________________________________________________________________________________________________________________________________________________________________
#                                                              METODA PER PAMJEN E PUNTORVE
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/api/workers', methods=['GET'])
@login_required
@admin_required
def get_workers():
    workers = User.query.filter_by(role='worker').all()

    # Convert the workers to a format that can be returned as JSON.
    worker_list = [{'id': worker.id, 'username': worker.username} for worker in workers]
    
    return jsonify(worker_list)


# 
# editimi i emrit te puntorve

from werkzeug.security import generate_password_hash

@app.route('/api/workers/<int:worker_id>', methods=['PUT'])
@login_required
@admin_required
def edit_worker(worker_id):
    worker = User.query.get(worker_id)
    if not worker:
        return jsonify({"success": False, "message": "Worker not found"}), 404

    data = request.get_json()
    new_username = data.get('username')
    new_password = data.get('password')

    if not new_username:
        return jsonify({"success": False, "message": "Username is required"}), 400

    # Validate the password if provided
    if new_password:
        # Here you can include any password validation you require
        if len(new_password) < 6:  # Example validation: password length
            return jsonify({"success": False, "message": "Password must be at least 6 characters long"}), 400
        # Hash the new password
        hashed_password = generate_password_hash(new_password)
        worker.password = hashed_password

    worker.username = new_username
    db.session.commit()

    return jsonify({"success": True, "message": "Worker updated successfully"}), 200



# 
# fshirja e  nje puntori

@app.route('/api/workers/<int:worker_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_worker(worker_id):
    worker = User.query.get(worker_id)
    if not worker:
        return jsonify({"success": False, "message": "Worker not found"}), 404

    db.session.delete(worker)
    db.session.commit()

    return jsonify({"success": True, "message": "Worker deleted successfully"}), 200


#______________________________________________________________________________________________________________________________________________________________________________________________
#                                                               METODA PER PAMJEN E KLIENTAVE
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



@app.route('/api/clients', methods=['GET'])
@login_required
@admin_or_worker_required
def get_clients():
    clients = User.query.filter_by(role='client').all()
    client_list = [{'id': client.id, 'username': client.username, 'status': client.status} for client in clients]
    return jsonify(client_list)



# 
# editimi i emrit te klientit
@app.route('/api/clients/<int:client_id>', methods=['PUT'])
@login_required
@admin_or_worker_required
def edit_client(client_id):
    client = User.query.get(client_id)
    if not client:
        return jsonify({"success": False, "message": "Client not found"}), 404

    data = request.get_json()
    new_username = data.get('username')
    new_password = data.get('password')

    if new_username:
        client.username = new_username
    
    if new_password:
        # Hash the new password before storing it
        client.password_hash = generate_password_hash(new_password)

    db.session.commit()

    return jsonify({"success": True, "message": "Client updated successfully"}), 200


# 
# metoda per fshirjen e nje kilenti


@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
@login_required
@admin_or_worker_required
def delete_client(client_id):
    client = User.query.get(client_id)
    if not client:
        return jsonify({"success": False, "message": "Client not found"}), 404

    db.session.delete(client)
    db.session.commit()

    return jsonify({"success": True, "message": "Client deleted successfully"}), 200



@app.route('/api/clients/<int:client_id>/activate', methods=['PUT'])
@login_required
@admin_or_worker_required
def activate_client(client_id):
    client = User.query.get(client_id)
    if not client:
        return jsonify({"success": False, "message": "Client not found"}), 404

    client.status = 'active'
    db.session.commit()

    return jsonify({"success": True, "message": "Client activated successfully"}), 200

@app.route('/api/clients/<int:client_id>/deactivate', methods=['PUT'])
@login_required
@admin_or_worker_required
def deactivate_client(client_id):
    client = User.query.get(client_id)
    if not client:
        return jsonify({"success": False, "message": "Client not found"}), 404

    client.status = 'deactive'
    db.session.commit()

    return jsonify({"success": True, "message": "Client deactivated successfully"}), 200



# _____________________________________________________________________________________________________________________________________________________________________________________________
                                                            # PRODUCTS
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from werkzeug.utils import secure_filename
import os
from app.models import Product , ProductImage
from PIL import Image



BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This gets the directory of the current file (which is "app")
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads')  # This goes one level up from "app" and then into "uploads"
ALLOWED_EXTENSIONS = {'jpg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compress_image(filename):
    img = Image.open(filename)
    img = img.convert('RGB')  # Convert to RGB if it's not
    img.save(filename, optimize=True, quality=85)  # Adjust quality as needed

@app.route('/add_product', methods=['POST'])
@login_required
@admin_or_worker_required
def add_product():
    data = request.form
    name = data.get('name')
    price = float(data.get('price'))
    description = data.get('description')
    quantity = int(data.get('quantity',0))
    images = request.files.getlist('images')

    # Save product data
    product = Product(name=name, price=price, description=description, quantity=quantity)
    db.session.add(product)
    db.session.commit()

    # Save images
    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            compress_image(filepath)  # Compress the image
            product_image = ProductImage(image_file=filename, product_id=product.id)
            db.session.add(product_image)

# Create and save notification
    notification = Notification(
        user_id=current_user.get_id(),  # Assuming current_user is the user adding the product
        product_id=product.id,
        action='added',  # The action being logged
        timestamp=datetime.utcnow()  # The time of the action
    )
    
    db.session.add(notification)
    db.session.commit()

    return jsonify(success=True, message="Product added successfully!")


@app.route('/products', methods=['GET'])
def get_products():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=30, type=int)

    products = Product.query.offset(start).limit(limit).all()
    product_list = [
        {
            'id': product.id, 
            'name': product.name, 
            'original_price': product.original_price,  # Add this line
            'price': product.price, 
            'description': product.description,
            'quantity': product.quantity,
            'images': [img.image_file for img in product.images]
        } for product in products
    ]
    return jsonify(product_list)





@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404
    product_data = {
        'id': product.id,
        'name': product.name,
        'original_price': product.original_price,  # Ensure this is included
        'price': product.price,
        'description': product.description,
        'quantity': product.quantity,
        'images': [img.image_file for img in product.images]
    }
    return jsonify(product_data)

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




@app.route('/product/<int:product_id>', methods=['PUT'])
@login_required
@admin_or_worker_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    data = request.json
    new_price = float(data.get('price', product.price))
    new_quantity = int(data.get('quantity', product.quantity))

    # Set original_price if it's not already set
    if product.original_price is None:
        product.original_price = product.price

    # Calculate the discount percentage
    discount_percentage = 0
    if product.original_price > 0:
        discount_percentage = round((1 - (new_price / product.original_price)) * 100, 2)

    # Update the product details
    product.name = data.get('name', product.name)
    product.price = new_price
    product.description = data.get('description', product.description)
    product.quantity = new_quantity

    db.session.commit()

    # Create a notification for the edit action
    create_edit_notification(product_id, current_user.id)

    # Return the response with discount percentage
    return jsonify(success=True, message="Product updated successfully!", discount_percentage=discount_percentage)


def create_edit_notification(product_id, user_id):
    try:
        notification = Notification(
            product_id=product_id,
            user_id=user_id,
            action='edited',
            timestamp=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Database error on create_edit_notification: {str(e)}")



# -----------------------------------------------------------------------------------------------------


@app.route('/product/<int:product_id>', methods=['DELETE'])
@login_required
@admin_or_worker_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    # Set the product_id to None for related notifications before deleting the product
    notifications = Notification.query.filter_by(product_id=product_id).all()
    for notification in notifications:
        notification.product_id = None
    db.session.flush()  # Flush the changes to the database

    # Call the notification function here before deleting the product
    notify_product_deleted(product_id, current_user.id)

    db.session.delete(product)
    db.session.commit()

    return jsonify(success=True, message="Product deleted successfully!")





# ______________________________________________________________________________________________________________________________________________________________________________________________
#                                                                 CART
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from sqlalchemy.exc import SQLAlchemyError


@app.route('/cart', methods=['POST'])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        if product.quantity < quantity:
            return jsonify({"message": "Not enough stock available!"}), 400

        # Decrease the product quantity when added to the cart
        product.quantity -= quantity
        db.session.add(product)

        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)

        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)

        # Check if product quantity has reached zero and notify
        if product.quantity == 0:
            notify_product_stock_empty(product.id, current_user.id)

        db.session.commit()
        return jsonify({"message": "Product added to cart successfully!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"SQLAlchemyError: {e}")
        return jsonify({"message": "An error occurred while adding to cart"}), 500
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Exception: {e}")
        return jsonify({"message": "An error occurred while adding to cart"}), 500

def notify_product_stock_empty(product_id, user_id):
    try:
        notification = Notification(
            product_id=product_id,
            user_id=user_id,
            action='product out of stock',
            timestamp=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Database error on notify_product_stock_empty: {str(e)}")




# ---------------------------------------------------------------------------

@app.route('/cart', methods=['GET'])
@login_required
def get_cart():
    try:
        # Fetch the cart for the currently logged-in user
        cart = Cart.query.filter_by(user_id=current_user.id).first()

        # Return an empty cart if none exists
        if not cart:
            return jsonify({"message": "Cart is empty", "cart_items": []}), 200

        # Construct the list of cart items
        cart_items = []
        for item in cart.items:
            product = item.product
            if product:  # Ensure the product exists
                cart_items.append({
                    'product_id': item.product_id,
                    'product_name': product.name,
                    'quantity': item.quantity,
                    'price': product.price,
                    'total': item.quantity * product.price,
                    'image': product.images[0].image_file if product.images else None
                })

        return jsonify({"message": "Cart fetched successfully", "cart_items": cart_items}), 200

    except Exception as e:
        # Handle any unexpected exceptions
        print(str(e))
        return jsonify({"message": "An error occurred while fetching the cart"}), 500
    
    

# -----------------------------------------------------------------------------------------


@app.route('/cart/update', methods=['PUT'])
@login_required
def update_cart_item():
    data = request.json
    product_id = data.get('product_id')
    new_quantity = data.get('quantity', 1)
    
    try:
        cart_item = CartItem.query.join(Cart).filter(Cart.user_id == current_user.id, CartItem.product_id == product_id).first()
        if not cart_item:
            return jsonify(success=False, message="Product not found in cart"), 404

        product = Product.query.get(product_id)

        # Calculate the quantity difference
        quantity_difference = new_quantity - cart_item.quantity
        if quantity_difference > 0 and product.quantity >= quantity_difference:
            product.quantity -= quantity_difference
        elif quantity_difference < 0:
            product.quantity -= quantity_difference  # This increases the quantity
        else:
            return jsonify(success=False, message="Not enough stock to update the cart"), 400

        db.session.add(product)

        cart_item.quantity = new_quantity
        db.session.add(cart_item)
        db.session.commit()
        return jsonify(success=True, message="Cart item updated successfully!")

    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"SQLAlchemyError: {e}")
        return jsonify(success=False, message="An error occurred while updating cart item"), 500
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Exception: {e}")
        return jsonify(success=False, message="An error occurred while updating cart item"), 500



# ----------------------------------------------------------------------------------------

@app.route('/cart/remove', methods=['DELETE'])
@login_required
def remove_from_cart():
    data = request.json
    product_id = data.get('product_id')
    
    try:
        cart_item = CartItem.query.join(Cart).filter(Cart.user_id == current_user.id, CartItem.product_id == product_id).first()
        if not cart_item:
            return jsonify(success=False, message="Product not found in cart"), 404

        # Increase the product quantity when removed from the cart
        product = Product.query.get(product_id)
        product.quantity += cart_item.quantity
        db.session.add(product)

        db.session.delete(cart_item)
        db.session.commit()
        return jsonify(success=True, message="Product removed from cart successfully!")

    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"SQLAlchemyError: {e}")
        return jsonify(success=False, message="An error occurred while removing item from cart"), 500



# -----------------------------------------------------------------------------

@app.route('/cart/clear', methods=['DELETE'])
@login_required
def clear_cart():
    try:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            for item in cart.items:
                db.session.delete(item)
            db.session.commit()
        return jsonify(success=True, message="Cart cleared successfully!")

    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"SQLAlchemyError: {e}")
        return jsonify(success=False, message="An error occurred while clearing the cart"), 500



# __________________________________________________________________________________________________________________________________________________________
#                                                               CHECKOUT STRIPE
# ---------------------------------------------------------------------------------------------------------------------------------------------------------

from sqlalchemy.exc import SQLAlchemyError
import stripe.error

@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    try:
        print("Creating checkout session...")  # Logging

        cart_items = get_cart_items_for_user(current_user.id)
        
        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                    'images': [f"http://localhost:5000/uploads/{image.image_file}" for image in item.product.images]
                },
                'unit_amount': int(item.product.price * 100)  # Convert to cents
            },
            'quantity': item.quantity
        } for item in cart_items]
        
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            payment_method_types=['card'],
            mode='payment',
            success_url='http://localhost:5173/success',
            cancel_url='http://localhost:5173/cancel',
        )

        return jsonify({
            'session_id': checkout_session.id,
            'success': True
        })

    except stripe.error.StripeError as e:
        app.logger.error(f"StripeError: {e}")
        return jsonify({'message': 'Stripe error occurred', 'success': False}), 500
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.error(f"SQLAlchemyError: {e}")
        return jsonify({'message': 'Database error occurred', 'success': False}), 500
    except Exception as e:
        app.logger.error(f"Exception: {e}")
        return jsonify({'message': 'An error occurred', 'success': False}), 500






@app.route('/payment-success')
def payment_success():
    try:
        # Fetch the cart items for the user
        cart_items = get_cart_items_for_user(current_user.id)

        # Deduct product quantities for each item in the cart
        for item in cart_items:
            product = Product.query.get(item.product_id)
            if product:
                # Ensure there's stock left and reduce the quantity by 1
                if product.quantity > 0:
                    product.quantity -= 1
                else:
                    # Handle the case where there's no stock left
                    return jsonify({"success": False, "message": f"No stock left for product {product.name}!"}), 400

        # Commit the changes to the database
        db.session.commit()

        # Clear the user's cart after successful payment
        clear_cart_for_user(current_user.id)

        return jsonify({"success": True, "message": "Payment was successful and product quantities updated!"})

    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500


    
    # Clear the cart
def clear_cart_for_user(user_id):
    cart = Cart.query.filter_by(user_id=user_id).filter()
    if cart:
        for item in cart.items:
            db.session.delete(item)
        db.session.commit()


def update_product_quantities(cart_items):
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            print(f"Before: Product ID {product.id} has quantity {product.quantity}")
            product.quantity -= item.quantity
            print(f"After: Product ID {product.id} now has quantity {product.quantity}")
    db.session.commit()



@app.route('/payment-cancelled')
def payment_cancelled():
    return jsonify({"success": False, "message": "Payment was cancelled."})



def get_cart_items_for_user(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if cart:
        return cart.items
    return []

# _____________________________________________________________________________________________________________________________________________________________
#                                                          Notifications
# -------------------------------------------------------------------------------------------------------------------------------------------------------------
from flask import jsonify
from datetime import datetime
from .models import db, Notification, Product, User
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemy exceptions

from sqlalchemy.orm.exc import NoResultFound

@app.route('/notifications')
def get_notifications():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)  # Set a default limit

    try:
        notifications_query = db.session.query(Notification, Product.name, User.username) \
            .join(Product, Product.id == Notification.product_id) \
            .join(User, User.id == Notification.user_id) \
            .order_by(Notification.timestamp.desc()) \
            .offset(start) \
            .limit(limit) \
            .all()
        notifications = [
            {
                'id': notification.Notification.id,
                'product_id': notification.Notification.product_id,
                'product_name': notification.name,
                'added_by': notification.username,
                'action': notification.Notification.action,
                'timestamp': notification.Notification.timestamp.isoformat()
            } for notification in notifications_query
        ]

        return jsonify(notifications)
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred"}), 500






def notify_product_edited(product_id, user_id):
    try:
        notification = Notification(
            product_id=product_id,
            user_id=user_id,
            action='updated',
            timestamp=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Database error on notify_product_edited: {str(e)}")

def notify_product_deleted(product_id, user_id):
    try:
        notification = Notification(
            product_id=None,  # Set this to None since the product is being deleted
            user_id=user_id,
            action='deleted',
            timestamp=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
    except SQLAlchemyError as e:
        print(f"Database error on notify_product_deleted: {str(e)}")



def notify_product_back_in_stock(product_id, user_id):
    """
    Notify when a product is back in stock.
    """
    try:
        # Create a new notification instance
        notification = Notification(
            user_id=user_id,
            product_id=product_id,
            action='back in stock',
            timestamp=datetime.utcnow()
        )
        # Add the notification to the database session and commit
        db.session.add(notification)
        db.session.commit()
    except Exception as e:
        # Log an error message if an exception occurs
        app.logger.error(f'Failed to notify product back in stock: {e}')
        # You might want to handle the exception further, such as notifying an admin or sending an alert.



# ----------------------------------------------------------------------------------------------------------------

def create_custom_notification(description, user_id, target_group):
    try:
        # Assuming there is a 'target_group' field in the Notification model
        # which can be 'clients', 'workers', or 'both'
        notification = Notification(
            user_id=user_id,
            product_id=None,  # This is a custom notification without a product
            action=description,
            target_group=target_group,
            timestamp=datetime.utcnow()
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        app.logger.error(f'Failed to create custom notification: {e}')
        return None
    
@app.route('/notifications/create', methods=['POST'])
@login_required
@admin_or_worker_required
def add_custom_notification():
    data = request.get_json()
    description = data.get('description')
    target_group = data.get('target_group')  # 'clients', 'workers', or 'both'
    user_id = current_user.get_id()

    notification = create_custom_notification(description, user_id, target_group)
    if notification:
        return jsonify({
            "success": True,
            "message": "Notification created successfully",
            "notification": {
                'id': notification.id,
                'action': notification.action,
                'target_group': notification.target_group,
                'timestamp': notification.timestamp.isoformat()
            }
        }), 201
    else:
        return jsonify({"success": False, "message": "Failed to create notification"}), 500
    



@app.route('/api/simple-notifications', methods=['GET'])
def get_simple_notifications():
    start = request.args.get('start', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    notifications = SimpleNotification.query \
        .order_by(SimpleNotification.date.desc()) \
        .offset(start) \
        .limit(limit) \
        .all()

    return jsonify([{
        'id': notification.id,
        'creator': notification.creator,
        'date': notification.date.strftime('%d-%m-%Y %H:%M:%S'),
        'description': notification.description
    } for notification in notifications]), 200


@app.route('/api/simple-notifications', methods=['POST'])
@admin_or_worker_required
def create_simple_notification():
    data = request.get_json()
    notification = SimpleNotification(
        creator=current_user.username,  # Use the current logged-in user's username
        description=data['description']
    )
    db.session.add(notification)
    db.session.commit()
    return jsonify({
        'id': notification.id,
        'creator': notification.creator,  # Send back the creator's username
        'date': notification.date.strftime('%Y-%m-%d %H:%M:%S'),
        'description': notification.description
    }), 201


@app.route('/api/notifications/<int:id>', methods=['DELETE'])
@admin_or_worker_required
def delte_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted'}),200

@app.route('/api/simple-notifications/<int:id>', methods=['DELETE'])
@admin_or_worker_required
def delete_simple_notification(id):
    notification = SimpleNotification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': "Simple notification deleted"}), 200

# ____________________________________________________________________________________________________________________________________________________________________________________________
#                                                              Autolarja (Washproducts)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image

@app.route('/washproducts/add', methods=['POST'])
def add_washproduct():
    data = request.form
    new_washproduct = Washproducts(
        name=data['name'],
        price=float(data['price']),
        description=data.get('description', '')
    )
    db.session.add(new_washproduct)
    db.session.commit()

    images = request.files.getlist('images')
    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            compress_image(filepath)
            washproduct_image = WashproductImage(image_file=filename, washproduct_id=new_washproduct.id)
            db.session.add(washproduct_image)

    db.session.commit()
    return jsonify({'message': 'New washproduct added', 'id': new_washproduct.id}), 201

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'webp'}

def compress_image(filename):
    img = Image.open(filename)
    img = img.convert('RGB')  # Convert to RGB if it's not
    img.save(filename, optimize=True, quality=85)  # Adjust quality as needed


# editimi i washproducts


@app.route('/washproducts/edit/<int:id>', methods=['PUT'])
def edit_washproduct(id):
    washproduct = Washproducts.query.get_or_404(id)

    # Using request.form and request.files for multipart/form-data
    name = request.form.get('name', washproduct.name)
    price = request.form.get('price', washproduct.price)
    description = request.form.get('description', washproduct.description)

    washproduct.name = name
    washproduct.price = price
    washproduct.description = description

    # Handle file uploads
    if 'images' in request.files:
        # Clear existing images
        WashproductImage.query.filter_by(washproduct_id=id).delete()
        db.session.commit()

        # Save new images
        for image in request.files.getlist('images'):
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)
                # Assuming you have a function to compress the image
                compress_image(filepath)
                new_image = WashproductImage(image_file=filename, washproduct_id=id)
                db.session.add(new_image)

    db.session.commit()
    return jsonify({'message': 'Washproduct updated', 'id': washproduct.id}), 200

def allowed_file(filename):
    # Check if the file has one of the allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'webp'}

def compress_image(filename):
    # Implement your image compression logic here
    pass



# get products 
@app.route('/washproducts', methods=['GET'])
def get_washproducts():
    washproducts = Washproducts.query.all()
    washproducts_data = [
        {
            'id': washproduct.id,
            'name': washproduct.name,
            'price': washproduct.price,
            'description': washproduct.description,
            'images': [image.image_file for image in washproduct.images]
        } for washproduct in washproducts
    ]
    return jsonify(washproducts_data), 200

# WashProduct detail

@app.route('/washproducts/<int:id>', methods=['GET'])
def get_washproduct(id):
    washproduct = Washproducts.query.get_or_404(id)
    washproduct_data = {
        'id': washproduct.id,
        'name': washproduct.name,
        'price': washproduct.price,
        'description': washproduct.description,
        'images': [image.image_file for image in washproduct.images]
    }
    return jsonify(washproduct_data), 200

@app.route('/washproducts/delete/<int:id>', methods=['DELETE'])
def delete_washproduct(id):
    washproduct = Washproducts.query.get_or_404(id)

    # Delete associated images if necessary
    # for image in washproduct.images:
    #     os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.image_file))

    db.session.delete(washproduct)
    db.session.commit()

    return jsonify({'message': 'Washproduct deleted', 'id': id}), 200


# ________________________________________________________________________________________________________________________________________________________________________________
#                                                                    Stripe Checkout per Autolarje
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import uuid
from flask import jsonify, request


@app.route('/create-washproduct-checkout-session', methods=['POST'])
def create_washproduct_checkout_session():
    try:
        data = request.get_json()
        washproduct = Washproducts.query.get(data['productId'])

        if not washproduct:
            return jsonify({'error': 'Washproduct not found'}), 404

        # Generate a unique payment_id
        payment_id = str(uuid.uuid4())

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(washproduct.price * 100),  # Convert price to cents
                    'product_data': {
                        'name': washproduct.name,
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'http://localhost:5173/Success-Page?paymentId={payment_id}',  # Append payment_id to the URL
            cancel_url='http://localhost:5173/cancel',
        )

        return jsonify({'sessionId': checkout_session['id'], 'paymentId': payment_id})
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

# ____________________________________________________________________________________________________________________________________________________________________________________________
#                                                                     Gjenerimi i QR CODE 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import qrcode
from io import BytesIO
from flask import Flask, request, send_file
import base64




@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    data = request.json
    payment_id = data.get('payment_id')
    if not payment_id:
        return jsonify({'error': 'Payment ID is required'}), 400

    # Generate and save QR code in the database
    user_id = current_user.id  # Assuming Flask-Login for user session
    new_qr_code = QRCode(payment_id=payment_id, user_id=user_id)
    db.session.add(new_qr_code)
    db.session.commit()

    # Generate QR image
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(payment_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return jsonify({'qr_image': img_base64})





@app.route('/check-qr-validity/<payment_id>', methods=['GET'])
def check_qr_validity(payment_id):
    qr_code = QRCode.query.filter_by(payment_id=payment_id).first()
    if qr_code and qr_code.is_valid():
        return jsonify({'is_valid': True})
    else:
        return jsonify({'is_valid': False})
    

@app.route('/user-qrcodes', methods=['GET'])
def get_user_qrcodes():
    user_id = current_user.id  # Using Flask-Login
    # Fetch only valid QR codes
    valid_qrcodes = QRCode.query.filter(QRCode.user_id == user_id, QRCode.creation_time > datetime.utcnow() - timedelta(minutes=30)).all()

    qrcode_data = []
    for qr in valid_qrcodes:
        # Generate QR image
        qr_code = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr_code.add_data(qr.payment_id)
        qr_code.make(fit=True)
        img = qr_code.make_image(fill_color="black", back_color="white")
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        qr_image = base64.b64encode(img_bytes.read()).decode('utf-8')

        qrcode_data.append({'id': qr.id, 'payment_id': qr.payment_id, 'is_valid': qr.is_valid(), 'qr_image': qr_image})

    return jsonify(qrcode_data)
