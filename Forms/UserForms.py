from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from re import match


class RegisterForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    password = StringField('Enter Password', validators=[DataRequired()])
    role = StringField('Enter Role', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class Login(FlaskForm):
    username = StringField('Login Username', validators=[DataRequired()])
    password = StringField('Login Password', validators=[DataRequired()])
    submit = SubmitField('Login User')