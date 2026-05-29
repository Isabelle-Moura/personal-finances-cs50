from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from app.models import User


CATEGORY_CHOICES = [
    ('Salary', 'Salary 💼'),
    ('Investments', 'Investments 📈'),
    ('Freelance', 'Freelance 💻'),
    ('Food', 'Food 🍔'),
    ('Rent', 'Rent 🏠'),
    ('Utilities', 'Utilities ⚡'),
    ('Transport', 'Transport 🚗'),
    ('Entertainment', 'Entertainment 🍿'),
    ('Shopping', 'Shopping 🛍️'),
    ('Health', 'Health 🏥'),
    ('Education', 'Education 📚'),
    ('Other', 'Other ❓')
]


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please login or use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class TransactionForm(FlaskForm):
    amount = DecimalField('Amount ($)', validators=[
        DataRequired(message="This field is required."), 
        NumberRange(min=0.01, message="The amount must be greater than zero.")
    ])
    description = StringField('Description', validators=[Length(max=200)])
    type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
    
    category = SelectField('Category', choices=CATEGORY_CHOICES, validators=[DataRequired()])
    
    submit = SubmitField('Add Transaction')


class BudgetForm(FlaskForm):
    category = SelectField('Category', choices=CATEGORY_CHOICES, validators=[DataRequired()])
    
    amount = DecimalField('Budget Limit ($)', validators=[
        DataRequired(message="This field is required."), 
        NumberRange(min=0.01, message="The budget limit must be greater than zero.")
    ])
    start_date = DateField('Start Date', validators=[DataRequired(message="Please select a start date.")])
    end_date = DateField('End Date', validators=[DataRequired(message="Please select an end date.")])
    submit = SubmitField('Set Budget')