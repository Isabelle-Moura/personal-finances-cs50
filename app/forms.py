from flask_wtf import FlaskForm
from wtforms import DateField, StringField, PasswordField, SubmitField, SelectField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Custom validation to ensure the username does not exist
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    # Custom validation to ensure the email does not exist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please login or use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Add SelectField, DecimalField, and TextAreaField to your wtforms imports at the top:

class TransactionForm(FlaskForm):
    amount = DecimalField('Amount ($)', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=200)])
    type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired()])
    category = SelectField('Category', choices=[('Salary', 'Salary'), ('Food', 'Food'), ('Rent', 'Rent'), ('Utilities', 'Utilities'), ('Other', 'Other')], validators=[DataRequired()])
    submit = SubmitField('Add Transaction')

class BudgetForm(FlaskForm):
    category = SelectField('Category', choices=[('Food', 'Food'), ('Rent', 'Rent'), ('Utilities', 'Utilities'), ('Other', 'Other')], validators=[DataRequired()])
    amount = DecimalField('Budget Limit ($)', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Set Budget')