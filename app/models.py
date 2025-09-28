from app import db 
from flask_login import UserMixin
from datetime import datetime

# ==============================================================================
# 1. User
# Represents the user table (required for login and registration)
# ==============================================================================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Relationships
    # user.transactions will give you all of the user's transactions
    transactions = db.relationship('Transaction', backref='owner', lazy=True)
    categories = db.relationship('Category', backref='owner', lazy=True)
    budgets = db.relationship('Budget', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# ==============================================================================
# 2. Categories
# Represents the categories of expenses/income (Food, Salary, etc.)
# ==============================================================================
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'income' or 'expense'

    # Foreign Key: Links the category to its user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Category('{self.name}', '{self.type}')"

# ==============================================================================
# 3. Transactions
# Represents each user entry (expense or income)
# ==============================================================================
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign Keys:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    def __repr__(self):
        return f"Transaction('{self.amount}', '{self.date}')"

# ==============================================================================
# 4. Budgets
# Displays the spending limits set by the user.
# ==============================================================================
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    # Foreign Keys:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"Budget('{self.amount}', '{self.start_date.date()}')"