from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from email_validator import validate_email, EmailNotValidError


class RegistrationForm(FlaskForm):
    orgname = StringField('Orgname',
                           validators=[DataRequired(), Length(max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    website = StringField('Website',
                                validators=[DataRequired(),
                                            Length(max=100)])
    acronym = StringField('Acronym', validators=[DataRequired(),
                                             Length(max=10)])
    puv_monthly = StringField('PUV_Per_Month', validators=[DataRequired(),
                                             Length(max=10)])
    address = StringField('Address',
                                validators=[DataRequired(),
                                            Length(max=80)])
    city = StringField('City',
                                validators=[DataRequired(),
                                            Length(max=20)])
    state = StringField('State',
                                validators=[DataRequired(),
                                            Length(max=20)])
    zip = StringField('Zip',
                                validators=[DataRequired(),
                                            Length(max=10)])
    submit = SubmitField('Sign Up')

class ConfirmationForm(FlaskForm):
    acronym = StringField('Acronym')
    submit = SubmitField('Start Extract')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
