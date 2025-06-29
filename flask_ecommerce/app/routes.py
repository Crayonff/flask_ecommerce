from flask import request, render_template, url_for, flash, redirect, request, Blueprint,current_app
from app import db,bcrypt
from datetime import datetime 
from app.forms import ForgotPasswordForm, RegistrationForm, LoginForm, UpdateProfileForm
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User,Product,Review
from PIL import Image
import secrets 
import os 


main = Blueprint('main', __name__)

# Home page
@main.route('/')
def home():
    return render_template('index.html', year=datetime.now().year) 

# Register page
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# Login page
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.login'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.products'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html', title = "Login",form=form)

@main.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user .password = hashed_password
            db.session.commit()
            flash("Your password has been reset successfully", 'success')
            return redirect(url_for('main.login'))
        else:
            flash("No account found with that email", 'danger')
    return render_template('forgot_password.html', form=form)

# Logout
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# Dashboard (protected route)
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html",title = "Profile", user = current_user)


@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data

        if form.pic.data:
            pass

        if form.password.data:
            current_user.set_password(form.password.data) 

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize the image
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@main.route("/products")
def products():
    all_products = Product.query.order_by(Product.id.desc()).all()  # Fetch latest products
    return render_template("products.html", products=all_products)

from flask import session

from flask import session, redirect, url_for, flash
from app.models import Product  # import your Product model

@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    # Check if product is in stock
    if product.stock <= 0:
        flash("This product is out of stock.", "danger")
        return redirect(url_for('main.products'))

    # Get cart from session, or create new one
    cart = session.get("cart", {})

    # Add product or increase quantity
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    # Save back to session
    session["cart"] = cart

    return redirect(url_for('main.products'))



@main.route("/cart")
@login_required
def view_cart():
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "subtotal": subtotal,
                "image": product.image  # assuming this is stored like 'static/img/whatever.jpg'
            })

    return render_template("cart.html",cart_items=cart_items, total=total)

@main.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session["cart"] = cart
    return redirect(url_for('main.products'))



@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('main.products'))

    cart_items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product = Product.query.get(int(product_id_str))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
                "subtotal": subtotal,
                "image": product.image
            })
    
        
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)

        if product and product.stock >= quantity:
            product.stock -= quantity  # 🔥 Reduce stock
        else:
            flash(f"Not enough stock for {product.name}", "danger")
            return redirect(url_for('main.view_cart'))

    db.session.commit()  # 🔥 Save changes
    session['cart'] = {}  # Clear cart after checkout

    if request.method == 'POST':
        # Here you would handle payment processing, order saving, etc.
        # For now, we'll just clear the cart and show success message

        session.pop('cart', None)
        flash("Thank you for your purchase! Your order has been placed.", "success")
        return redirect(url_for('main.products'))

    return render_template('checkout.html', cart_items=cart_items, total=total)


@main.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
def submit_review(product_id):
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment', '').strip()

    # You can get user_id from session or login manager if you have users
    user_id = current_user.id if current_user.is_authenticated else None # Implement accordingly or use None for anonymous

    if not (1 <= rating <= 5):
        flash("Invalid rating value.", "error")
        return redirect(url_for('main.products'))  # or product detail page

    review = Review(product_id=product_id, user_id=user_id, rating=rating, comment=comment)
    db.session.add(review)
    db.session.commit()
    flash("Review submitted successfully!", "success")
    return redirect(url_for('main.products')) 
