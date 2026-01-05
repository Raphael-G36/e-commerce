from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from models import db, Product, User, Order, OrderItem
from functools import wraps
from chatbot import chatbot_service
import os
import random
import string
from datetime import datetime

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "ecommerce.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# Custom Jinja2 filter for currency formatting
@app.template_filter('currency')
def currency_filter(value):
    """Format number as NGN currency with commas"""
    try:
        num = float(value)
        return f"₦{num:,.2f}"
    except (ValueError, TypeError):
        return f"₦0.00"


@app.route("/")
def index():
    """Homepage with featured products"""
    featured_products = Product.query.filter_by(featured=True).limit(6).all()
    # If no featured products, show all products
    if not featured_products:
        featured_products = Product.query.limit(6).all()
    return render_template('index.html', featured_products=featured_products)


@app.route("/products")
def products():
    """Products listing page with optional category filter"""
    category = request.args.get('category', None)
    
    if category:
        # Case-insensitive category matching
        products_list = Product.query.filter(
            Product.category.ilike(f'%{category}%')
        ).all()
    else:
        products_list = Product.query.all()
    
    return render_template('products.html', products=products_list)


@app.route("/product/<int:id>")
def product_detail(id):
    """Product detail page"""
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)


@app.route("/cart")
def cart():
    """Shopping cart page"""
    return render_template('cart.html')


def generate_order_number():
    """Generate unique order number"""
    return 'ORD' + ''.join(random.choices(string.digits, k=8))


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    if request.method == 'POST':
        try:
            # Get cart from session or localStorage (we'll use session for server-side)
            cart_data = request.form.get('cart_data')
            if not cart_data:
                flash('Your cart is empty', 'error')
                return redirect(url_for('cart'))
            
            import json
            cart_items = json.loads(cart_data)
            
            if not cart_items:
                flash('Your cart is empty', 'error')
                return redirect(url_for('cart'))
            
            # Get customer information
            customer_name = request.form.get('customer_name')
            customer_email = request.form.get('customer_email')
            customer_phone = request.form.get('customer_phone')
            shipping_address = request.form.get('shipping_address')
            city = request.form.get('city')
            state = request.form.get('state')
            postal_code = request.form.get('postal_code')
            payment_method = request.form.get('payment_method')
            
            # Validate required fields
            if not all([customer_name, customer_email, customer_phone, shipping_address, city, state, postal_code, payment_method]):
                flash('Please fill in all required fields', 'error')
                return redirect(url_for('checkout'))
            
            # Calculate total
            total_amount = 0
            order_items_data = []
            
            for item in cart_items:
                product = Product.query.get(item['id'])
                if product:
                    quantity = item['quantity']
                    price = float(product.price)
                    subtotal = price * quantity
                    total_amount += subtotal
                    
                    order_items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price': price,
                        'subtotal': subtotal
                    })
            
            # Create order
            order = Order(
                order_number=generate_order_number(),
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                shipping_address=shipping_address,
                city=city,
                state=state,
                postal_code=postal_code,
                total_amount=total_amount,
                payment_method=payment_method,
                payment_status='pending',
                status='pending'
            )
            
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create order items
            for item_data in order_items_data:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data['product'].id,
                    product_name=item_data['product'].name,
                    quantity=item_data['quantity'],
                    price=item_data['price'],
                    subtotal=item_data['subtotal']
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            # Process payment (sample logic)
            payment_result = process_payment(order.id, payment_method, total_amount)
            
            if payment_result['success']:
                order.payment_status = 'completed'
                order.status = 'processing'
                db.session.commit()
                
                # Clear cart
                session['cart'] = []
                
                flash('Order placed successfully!', 'success')
                return redirect(url_for('order_confirmation', order_number=order.order_number))
            else:
                order.payment_status = 'failed'
                db.session.commit()
                flash(f'Payment failed: {payment_result["message"]}', 'error')
                return redirect(url_for('checkout'))
                
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('checkout'))
    
    return render_template('checkout.html')


def process_payment(order_id, payment_method, amount):
    """
    Sample payment processing logic
    In a real application, this would integrate with payment gateways like Paystack, Flutterwave, etc.
    """
    # Simulate payment processing
    # For demo purposes, we'll simulate success for certain conditions
    
    if payment_method == 'card':
        # Simulate card payment - always succeeds for demo
        return {'success': True, 'message': 'Payment processed successfully', 'transaction_id': f'TXN{random.randint(100000, 999999)}'}
    elif payment_method == 'bank_transfer':
        # Simulate bank transfer - always succeeds for demo
        return {'success': True, 'message': 'Bank transfer initiated', 'transaction_id': f'BT{random.randint(100000, 999999)}'}
    elif payment_method == 'pay_on_delivery':
        # Pay on delivery - always succeeds
        return {'success': True, 'message': 'Order confirmed. Pay on delivery.', 'transaction_id': None}
    else:
        return {'success': False, 'message': 'Invalid payment method'}


@app.route("/order-confirmation/<order_number>")
def order_confirmation(order_number):
    """Order confirmation page"""
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template('order_confirmation.html', order=order)


@app.route("/track-order", methods=['GET', 'POST'])
def track_order():
    """Order tracking page - search for specific order"""
    order = None
    error = None
    
    if request.method == 'POST':
        order_number = request.form.get('order_number', '').strip()
        email = request.form.get('email', '').strip()
        
        if order_number and email:
            order = Order.query.filter_by(
                order_number=order_number.upper(),
                customer_email=email
            ).first()
            
            if not order:
                error = 'Order not found. Please check your order number and email address.'
        else:
            error = 'Please provide both order number and email address.'
    elif request.method == 'GET' and request.args.get('order_number') and request.args.get('email'):
        # Handle direct links from My Orders page
        order_number = request.args.get('order_number', '').strip()
        email = request.args.get('email', '').strip()
        
        if order_number and email:
            order = Order.query.filter_by(
                order_number=order_number.upper(),
                customer_email=email
            ).first()
            
            if not order:
                error = 'Order not found. Please check your order number and email address.'
    
    return render_template('track_order.html', order=order, error=error)


@app.route("/my-orders", methods=['GET', 'POST'])
def my_orders():
    """View all orders for a customer by email"""
    orders = []
    email = None
    error = None
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if email:
            orders = Order.query.filter_by(
                customer_email=email
            ).order_by(Order.created_at.desc()).all()
            
            if not orders:
                error = 'No orders found for this email address.'
        else:
            error = 'Please provide your email address.'
    elif request.method == 'GET' and request.args.get('email'):
        # Allow viewing orders via query parameter
        email = request.args.get('email', '').strip()
        if email:
            orders = Order.query.filter_by(
                customer_email=email
            ).order_by(Order.created_at.desc()).all()
    
    return render_template('my_orders.html', orders=orders, email=email, error=error)


@app.route("/order/<order_number>")
def view_order(order_number):
    """View order details by order number (public access with email verification)"""
    order = Order.query.filter_by(order_number=order_number.upper()).first_or_404()
    return render_template('view_order.html', order=order)


@app.route("/contact")
def contact():
    """Contact page"""
    return render_template('contact.html')


@app.route("/api/cart-products")
def cart_products():
    """API endpoint to get product details for cart items"""
    ids_param = request.args.get('ids', '')
    if not ids_param:
        return jsonify([])
    
    try:
        product_ids = [int(id) for id in ids_param.split(',') if id.strip()]
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        return jsonify([product.to_dict() for product in products])
    except (ValueError, Exception) as e:
        return jsonify({'error': str(e)}), 400


@app.route("/api/chat", methods=['POST'])
def chat():
    """API endpoint for chatbot"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate response using chatbot service
        response = chatbot_service.generate_response(user_message, conversation_history)
        
        return jsonify({
            'response': response,
            'success': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


# Authentication routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            
            # Redirect to admin if admin, otherwise to home
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route("/logout")
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('You need to be an admin to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Admin routes
@app.route("/admin")
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_products = Product.query.count()
    total_stock = db.session.query(db.func.sum(Product.stock)).scalar() or 0
    low_stock = Product.query.filter(Product.stock < 10).count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html', 
                         total_products=total_products,
                         total_stock=total_stock,
                         low_stock=low_stock,
                         total_orders=total_orders,
                         pending_orders=pending_orders)


@app.route("/admin/products")
@admin_required
def admin_products():
    """Admin products list"""
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)


@app.route("/admin/products/add", methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            price=float(request.form.get('price')),
            image=request.form.get('image'),
            stock=int(request.form.get('stock', 0)),
            featured=bool(request.form.get('featured'))
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = ['Electronics', 'Fashion', 'Sports', 'Home & Living']
    return render_template('admin/product_form.html', product=None, categories=categories)


@app.route("/admin/products/edit/<int:id>", methods=['GET', 'POST'])
@admin_required
def admin_edit_product(id):
    """Edit product"""
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.category = request.form.get('category')
        product.price = float(request.form.get('price'))
        product.image = request.form.get('image')
        product.stock = int(request.form.get('stock', 0))
        product.featured = bool(request.form.get('featured'))
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = ['Electronics', 'Fashion', 'Sports', 'Home & Living']
    return render_template('admin/product_form.html', product=product, categories=categories)


@app.route("/admin/products/delete/<int:id>", methods=['POST'])
@admin_required
def admin_delete_product(id):
    """Delete product"""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin_products'))


@app.route("/admin/orders")
@admin_required
def admin_orders():
    """Admin orders list"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@app.route("/admin/orders/<int:id>")
@admin_required
def admin_order_detail(id):
    """Admin order detail"""
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)


@app.route("/admin/orders/<int:id>/update-status", methods=['POST'])
@admin_required
def admin_update_order_status(id):
    """Update order status"""
    order = Order.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash('Order status updated successfully!', 'success')
    return redirect(url_for('admin_order_detail', id=id))


if __name__ == "__main__":
    app.run(debug=True)
