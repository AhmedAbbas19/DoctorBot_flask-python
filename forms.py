from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField,BooleanField,SelectField,IntegerField
from wtforms.validators import DataRequired, length, Email, EqualTo,NumberRange

class RegistrationForm(FlaskForm):
    firstName = StringField('First Name',
                            validators=[DataRequired(),length(min=2,max=12)])
    lastName = StringField('Last Name',
                            validators=[DataRequired(),length(min=2,max=12)])
    email = StringField('Email',
                                validators=[DataRequired(),Email()])
    age = IntegerField('Age',validators=[DataRequired(),NumberRange(min=18, max=100)])
    gender = SelectField('Gender',choices=[('','Gender (prefer not to say)'),('male','Male'),('female','Female')])
    acc_type = SelectField('Account Type',choices=[('patient','Account type (Default: Patient)'),('patient','Patient'),('doctor','Doctor')])
    specialization = StringField('Specialization')
    password = PasswordField('Password',validators=[DataRequired(),length(min=8,max=30)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                                validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')