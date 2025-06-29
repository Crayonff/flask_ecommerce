from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError,Length
from app.models import User   
from flask_wtf.file import FileAllowed

# Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')
# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, message = "Password must be 8 characters")]) 
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Reset Password')  
class UpdateProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Update')
