from flask_wtf import FlaskForm
from wtforms import SubmitField,PasswordField,StringField,ValidationError
from wtforms.validators import Email,EqualTo,DataRequired

from ..models import User

class RegistrationForm(FlaskForm):
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired(),EqualTo("confirm_password")])
	confirm_password=PasswordField("Confirm Password",validators=[DataRequired()])
	submit=SubmitField("Submit")
	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError("Email have been used")	
	

class LoginForm(FlaskForm):
	email=StringField("Email",validators=[DataRequired(),Email()])	
	password=PasswordField("Password",validators=[DataRequired()])
	submit=SubmitField("Login")

	
