from flask import Blueprint, render_template, request, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm, TransactionForm, BudgetForm
from app import db 
from app.models import Category, Transaction, User, Budget
from flask_bcrypt import Bcrypt 
from flask_login import login_user, logout_user, current_user, login_required

bcrypt = Bcrypt() 

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Home')



@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('main.login')) 
        
    else:
        print("--- Form Validation Failed (Register): ---")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"  Field '{field}': {error}")
        print("------------------------------------------")
        
    return render_template('register.html', title='Register', form=form)



@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user) 
            
            flash('Login successful!', 'success')
            
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            
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
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))



@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
                                           .order_by(Transaction.date.desc())\
                                           .limit(5).all()
    
    all_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    total_income = 0.0
    total_expense = 0.0
    
    for t in all_transactions:
        if t.category and t.category.type == 'income':
            total_income += t.amount
        else:
            total_expense += t.amount
            
    total_balance = total_income - total_expense

    user_budgets = Budget.query.filter_by(user_id=current_user.id).all()
    critical_budgets = []
    
    for b in user_budgets:
        current_category = Category.query.get(b.category_id)
        category_name = current_category.name if current_category else "Unknown"
        
        total_spent = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.category_id == b.category_id,
            Transaction.date >= b.start_date,
            Transaction.date <= b.end_date
        ).scalar() or 0.0
        
        percentage = (total_spent / b.amount) * 100 if b.amount > 0 else 0
        
        if percentage >= 80:
            critical_budgets.append({
                'category_name': category_name,
                'percentage': min(percentage, 100),
                'remaining': b.amount - total_spent
            })

    return render_template('dashboard.html', 
                           title='Dashboard', 
                           user=current_user, 
                           transactions=recent_transactions, 
                           income=total_income,
                           expense=total_expense,
                           balance=total_balance,
                           alerts=critical_budgets) 



@main.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    form = BudgetForm()
    
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.category.data, user_id=current_user.id).first()
        
        if not category:
            category = Category(name=form.category.data, type='expense', user_id=current_user.id)
            db.session.add(category)
            db.session.commit()
            
        budget = Budget(
            amount=float(form.amount.data),
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            user_id=current_user.id,
            category_id=category.id
        )
        db.session.add(budget)
        db.session.commit()
        flash('Budget limit configured successfully!', 'success')
        return redirect(url_for('main.budgets'))

    user_budgets = Budget.query.filter_by(user_id=current_user.id).all()
    
    budget_reports = []
    for b in user_budgets:
        current_category = Category.query.get(b.category_id)
        category_name = current_category.name if current_category else "Unknown"
        
        total_spent = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.category_id == b.category_id,
            Transaction.date >= b.start_date,
            Transaction.date <= b.end_date
        ).scalar() or 0.0
        
        percentage = (total_spent / b.amount) * 100 if b.amount > 0 else 0
        
        budget_reports.append({
            'budget': b,
            'category_name': category_name,
            'spent': total_spent,
            'remaining': b.amount - total_spent,
            'percentage': min(percentage, 100) 
        })

    return render_template('budgets.html', title='Budgets', form=form, budget_reports=budget_reports)



@main.route('/budget/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    
    if budget.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.budgets'))
        
    db.session.delete(budget)
    db.session.commit()
    flash('Budget limit deleted successfully!', 'success')
    return redirect(url_for('main.budgets'))



@main.route('/budget/edit/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    
    if budget.user_id != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.budgets'))
        
    form = BudgetForm()
    
    if request.method == 'GET':
        current_category = Category.query.get(budget.category_id)
        if current_category:
            form.category.data = current_category.name
        form.amount.data = budget.amount
        form.start_date.data = budget.start_date
        form.end_date.data = budget.end_date
    
    if form.validate_on_submit():
        category_name = form.category.data
        category = Category.query.filter_by(name=category_name, user_id=current_user.id).first()
        
        if not category:
            category = Category(name=category_name, type='expense', user_id=current_user.id)
            db.session.add(category)
            db.session.commit()
            
        budget.category_id = category.id
        budget.amount = float(form.amount.data)
        budget.start_date = form.start_date.data
        budget.end_date = form.end_date.data
        
        db.session.commit()
        flash('Budget limit updated successfully!', 'success')
        return redirect(url_for('main.budgets'))



@main.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    form = TransactionForm()
    
    if form.validate_on_submit():
        if float(form.amount.data) > 1000000:
            flash('Transaction blocked! Value exceeds the maximum fraud prevention limit.', 'danger')
            return redirect(url_for('main.transactions'))
        
        category_name = form.category.data

        category = Category.query.filter_by(
            name=category_name, 
            type=form.type.data, 
            user_id=current_user.id
        ).first()
        
        if not category:
            category = Category(name=category_name, type=form.type.data, user_id=current_user.id)
            db.session.add(category)
            db.session.commit()

        transaction = Transaction(
            amount=float(form.amount.data),
            description=form.description.data,
            user_id=current_user.id,
            category_id=category.id
        )
        
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.transactions'))

    transaction_filter = request.args.get('filter', 'all')
    
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    if transaction_filter == 'income':
        user_transactions = query.join(Category).filter(Category.type == 'income').order_by(Transaction.date.desc()).all()
    elif transaction_filter == 'expense':
        user_transactions = query.join(Category).filter(Category.type == 'expense').order_by(Transaction.date.desc()).all()
    else:
        user_transactions = query.order_by(Transaction.date.desc()).all()
    
    return render_template('transactions.html', 
                           title='Transactions', 
                           form=form, 
                           transactions=user_transactions, 
                           current_filter=transaction_filter)



@main.route('/transaction/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction.', 'danger')
        return redirect(url_for('main.transactions')) 
        
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('main.transactions')) 