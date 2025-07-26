from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    stock = StringField('Stock', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    submit = SubmitField('Save')

class CheckoutForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    zip = StringField('ZIP Code', validators=[DataRequired(), Length(max=20)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Proceed')
