from flask import Blueprint, render_template, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm, TransactionForm
from app import db 
from app.models import Category, Transaction, User
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



# [PAREI] - Tela de login não funciona. Ver o pq!!!



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


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TransactionForm()
    
    # 1. Handle form submission to add a new transaction
    if form.validate_on_submit():
        # First, find or create the category in the database for this user
        category_name = form.category.data
        category = Category.query.filter_by(name=category_name, user_id=current_user.id).first()
        
        if not category:
            category = Category(name=category_name, type=form.type.data, user_id=current_user.id)
            db.session.add(category)
            db.session.commit()

        # Create the transaction object
        # Convert amount to float for the database structure
        transaction = Transaction(
            amount=float(form.amount.data),
            description=form.description.data,
            user_id=current_user.id,
            category_id=category.id
        )
        
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    # 2. Query all transactions belonging to the current user
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    # 3. Calculate metrics (Incomes, Expenses, Balance)
    total_income = 0.0
    total_expense = 0.0
    
    for t in user_transactions:
        if t.category and t.category.type == 'income':
            total_income += t.amount
        else:
            total_expense += t.amount
            
    total_balance = total_income - total_expense

    return render_template('dashboard.html', 
                           title='Dashboard', 
                           user=current_user, 
                           form=form, 
                           transactions=user_transactions,
                           income=total_income,
                           expense=total_expense,
                           balance=total_balance)