from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms import ValidationError
from wtforms.validators import (InputRequired, Email, Length, EqualTo, 
        DataRequired)
from ..models import User

class RegistrationForm(FlaskForm):
    user_name = StringField("Username", validators = [InputRequired(), 
        Length(3, 64)])
    email_address = StringField("Email Address", validators = [InputRequired(), 
        Email(), Length(10, 128)])
    password = PasswordField("Password", validators = [InputRequired(), 
        Length(8, 32)])
    confirm_password = PasswordField("Confirm Password", validators = [
        InputRequired(), Length(8, 32), EqualTo("password", 
        message = "Passwords must match")])


    def validate_email_address(self, field):
        if User.query.filter_by(emailAddress = field.data).first():
            raise ValidationError("Email already registered")
   

    def validate_user_name(self, field):
        if User.query.filter_by(userName = field.data).first():
            raise ValidationError("Username already in use")


class EditUserProfileForm(FlaskForm):
    firstName = StringField('First Name', validators=[Length(1, 50)])
    middleName = StringField('Middle Name', validators=[Length(1, 50)])
    lastName = StringField('Last Name', validators=[Length(1, 50)])
    
    phoneNumber = StringField('Phone Number', validators=[Length(1, 50)])
    gender = SelectField('Gender')

    locationAddress = StringField('Residential Address', 
            validators=[DataRequired(), Length(1, 128)])
    about_me = TextAreaField('About Me', validators=[Length(1, 192)])
