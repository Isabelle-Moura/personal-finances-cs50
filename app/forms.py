from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    # Field for Username
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    # Field for Email
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    # Field for Password
    password = PasswordField('Password', validators=[DataRequired()])
    
    # Field for Password Confirmation
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    
    # Submission Button
    submit = SubmitField('Register')

    # Custom validation to ensure the username does not exist
    def validate_username(self, username):
        # Queries the database for the username
        user = User.query.filter_by(username=username.data).first()
        if user:
            # Raises a validation error if a user is found
            raise ValidationError('That username is taken. Please choose a different one.')

    # Custom validation to ensure the email does not exist
    def validate_email(self, email):
        # Queries the database for the email
        user = User.query.filter_by(email=email.data).first()
        if user:
            # Raises a validation error if an email is found
            raise ValidationError('That email is already registered. Please login or use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')