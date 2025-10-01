from flask import Blueprint, render_template, url_for, flash, redirect
from app.forms import RegistrationForm
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
    # Temporary route, will be changed to the dashboard after login is implemented
    return render_template('home.html', title='Home')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    # Checks if the form data is valid upon submission (POST method)
    if form.validate_on_submit():
        # 1. Password Hashing: Generate hash and decode to utf-8
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # 2. User Creation: Create a new User object
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        
        # 3. Save to Database: Add the user and commit the transaction
        db.session.add(user)
        db.session.commit()
        
        # 4. Success Message and Redirection
        # 'success' is a category for flashing messages
        flash('Your account has been created! You are now able to log in.', 'success')
        
        # Redirect to the login route (to be created next)
        return redirect(url_for('main.login')) 
    
    else:
        print("--- Form Validation Failed (Register): ---")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"  Field '{field}': {error}")
        print("---------------------------------------")

    # Render the registration template (for GET requests or invalid POST)
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        #1. Search for the user by email
        user = User.query.filter_by(email=form.email.data).first()
        
        #2. Verify that the user exists AND that the password is correct.
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            
            # 3. Logging in the user (Flask-Login)
            login_user(user, remember=form.remember.data) 
            
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            # Credential Failure (Incorrect User/Password)
            flash('Login failure. Please check your email and password.', 'danger')
            
    else:
        print("--- Form Validation Failed (Login): ---")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"  Field '{field}': {error}")
        print("---------------------------------------")
            
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user() 
    flash('You were disconnect.', 'info')
    return redirect(url_for('main.home'))
    form = LoginForm()