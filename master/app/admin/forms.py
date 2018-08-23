from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

from ..models import User

class UserForm(FlaskForm):
	email=StringField("Email",validators=[DataRequired()])
	password=PasswordField("Password",validators=[DataRequired()])
	submit=SubmitField("Submit")


