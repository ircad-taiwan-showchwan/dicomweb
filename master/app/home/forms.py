from flask_wtf import FlaskForm,Form
from wtforms import StringField,SubmitField,ValidationError
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms.widgets import html_params,HTMLString
from flask_uploads import UploadSet,IMAGES
from flask_wtf.file import FileField,FileAllowed,FileRequired
from werkzeug.utils import secure_filename
from ..models import ImageDB
images=UploadSet("images",IMAGES)

class EditImageForm(FlaskForm):
	image_name=StringField("Image Name",validators=[DataRequired()])
	image_description=StringField("Image Description",validators=[DataRequired()])
	image_filename=FileField("Change Image",validators=[FileRequired(),FileAllowed(["bmp","jpg","png","dcm"],"can only upload spesific images format!")])
	submit=SubmitField("Change Image")
	'''	
	def validate_image_name(self,field):			
		if Image.query.filter_by(image_name=field.data).first():
			raise ValidationError("Image Name has been used")
	'''
class AddImageForm(FlaskForm):	

	image_name=StringField("Image Name",validators=[DataRequired()])
	image_description=StringField("Image Description",validators=[DataRequired()])
	image_filename=FileField("Upload Image",validators=[FileRequired(),FileAllowed(["bmp","jpg","png","dcm"],"can only upload specific images format!")])
		
	submit=SubmitField("Save Image")
	
	def validate_image_name(self,field):
		if ImageDB.query.filter_by(image_name=field.data).first():
			raise ValidationError("Image Name Has Been Used")


	
	
