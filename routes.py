from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from models import User, Product
from forms import SignupForm, LoginForm, ProductForm
from extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    username = None
    if session.get('user_id'):
        from models import User
        user = User.query.get(session['user_id'])
        if user:
            username = user.username
    return render_template('index.html', username=username)

@main.route('/products')
def products():
    return render_template('products.html')

@main.route('/products/<int:product_id>')
def product_detail(product_id):
    return render_template('product_detail.html', product_id=product_id)

@main.route('/cart')
def cart():
    if not session.get('user_id'):
        flash('Please log in to access your cart.', 'warning')
        return redirect(url_for('main.login'))
    return render_template('cart.html')

from forms import CheckoutForm

@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not session.get('user_id'):
        flash('Please log in to proceed to checkout.', 'warning')
        return redirect(url_for('main.login'))
    form = CheckoutForm()
    cart_items = []
    total = 0
    from models import CartItem
    if session.get('user_id'):
        cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    from models import Order, OrderItem, CartItem, db
    print('POST:', request.method == 'POST')
    print('form.errors:', form.errors)
    if form.validate_on_submit():
        print('Form validated! Proceeding to save order.')
        # Create order
        order = Order(
            user_id=session['user_id'],
            name=form.name.data,
            address=form.address.data,
            city=form.city.data,
            zip=form.zip.data,
            phone=form.phone.data
        )
        db.session.add(order)
        db.session.flush()  # get order.id
        # Add order items
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                subtotal=item.product.price * item.quantity
            )
            db.session.add(order_item)
        # Clear cart
        CartItem.query.filter_by(user_id=session['user_id']).delete()
        db.session.commit()
        return redirect(url_for('main.order_success', order_id=order.id))
    return render_template('checkout.html', form=form, cart_items=cart_items, total=total)

@main.route('/order-success/<int:order_id>')
def order_success(order_id):
    from models import Order
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    redirect_home = False
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            redirect_home = True
        else:
            flash('Invalid username or password', 'danger')
    if redirect_home:
        return render_template('login.html', form=form, redirect_home=True)
    return render_template('login.html', form=form)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.login'))
