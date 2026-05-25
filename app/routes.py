from flask import Blueprint, render_template, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm
from app import db 
from app.models import User
from flask_bcrypt import Bcrypt 
from flask_login import login_user, logout_user, current_user, login_required

# Initialize Bcrypt outside the route function
bcrypt = Bcrypt() 

# Create the Blueprint for main application routes
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # 1. Password Hashing: Generate hash and decode to utf-8
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # 2. User Creation: Create a new User object
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        
        # 3. Save to Database: Add the user and commit the transaction
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('main.login')) 
        
    else:
        # Debugging: Print validation errors to the Linux terminal
        print("--- Form Validation Failed (Register): ---")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"  Field '{field}': {error}")
        print("------------------------------------------")
        
    return render_template('register.html', title='Register', form=form)



# [PAREI] - Tela de login não funciona. Ver o pq.



@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        # 1. Query user by the provided email
        user = User.query.filter_by(email=form.email.data).first()
        
        # 2. Check if user exists and password hash matches
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            
            # 3. Log the user in via Flask-Login
            login_user(user) 
            
            flash('Login successful!', 'success')
            
            # 4. Redirect directly to the protected Dashboard
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            
    else:
        # Debugging: Print validation errors to the Linux terminal
        print("--- Form Validation Failed (Login): ---")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"  Field '{field}': {error}")
        print("---------------------------------------")
            
    return render_template('login.html', title='Login', form=form)


@main.route("/logout")
def logout():
    logout_user() 
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard', user=current_user)