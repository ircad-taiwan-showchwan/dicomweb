from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

from app import db,login_manager

class User(UserMixin,db.Model):
	__tablename__="users"
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String(60),index=True,unique=True)
	password_hash=db.Column(db.String(128))
	registered_on = db.Column(db.DateTime, nullable=False)
	confirmed=db.Column(db.Integer)
	confirmed_on = db.Column(db.DateTime, nullable=True)
	is_admin=db.Column(db.Boolean,default=False)

	@property
	def password(self):
		raise AttributeError("Password is not readable attribute")
	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)
	def __repr__(self):
		return '<User:{}>'.format(self.email)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(int(user_id))

class ImageDB(db.Model):
	__tablename__="images"
	id=db.Column(db.Integer,primary_key=True)
	image_name=db.Column(db.String(60),unique=True)
	image_description=db.Column(db.String(200))
	image_filename=db.Column(db.String(250))
	image_frame_count=db.Column(db.Integer)
	user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
	users=db.relationship("SegmentedImage",backref="image",lazy="dynamic")
	image_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

	def load_image(image_id):
		return Image.query.get(int(image_id))
	def __repr__(self):
		return '<Image:{}>'.format(self.image_name)

class SegmentedImage(db.Model):
	__tablename__="segmentedimages"
	id=db.Column(db.Integer,primary_key=True)
	segmented_image_jpg_name=db.Column(db.String(200))
	segmented_image_dicom_name=db.Column(db.String(200))
	image_id=db.Column(db.Integer,db.ForeignKey("images.id"),nullable=False)
	images=db.relationship("SegmentedPoint",backref="segmentedimage",lazy="dynamic")
	segmented_image_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	segmented_image_comment=db.Column(db.Text)
	def __repr__(self):
		return '<SegmentedImage:{}>'.format(self.segmented_image_name)

class SegmentedPoint(db.Model):
	__tablename__="segmentedpoints"
	id=db.Column(db.Integer,primary_key=True)
	segmented_point_name=db.Column(db.String(200),unique=True)
	segmented_point_data=db.Column(db.String(250))
	segmented_image_id=db.Column(db.Integer,db.ForeignKey("segmentedimages.id"),nullable=False)
	segmented_point_date=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	def __repr__(self):
		return '<SegmentedPoint:{}>'.format(self.segmented_point_name)











