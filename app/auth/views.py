from flask import flash,redirect,render_template,url_for,current_app
from flask_login import login_required,login_user,logout_user
from . import auth
from forms import LoginForm,RegistrationForm
from .. import db
from ..models import User
from datetime import datetime
from app import mail  # you can now import the Mail() object
from flask_mail import Message

@auth.route("/login",methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user)
			if user.is_admin:
				return redirect(url_for("home.admin_dashboard"))
			else:
				return redirect(url_for("home.dashboard"))
				#flash("Invalid email or password")
		else:
			flash("Invalid email or password")
	return render_template("auth/login.html",form=form,title="login")

@auth.route("/register",methods=["GET","POST"])
def register():
	form=RegistrationForm()
	if form.validate_on_submit():
		user=User(email=form.email.data,password=form.password.data,confirmed=1,registered_on=datetime.now(),is_admin=0)
		db.session.add(user)
		db.session.commit()
		#msg = Message('Hello', sender = 'gregoriusairlangga@gmail.com', recipients = ['gregorius.airlangga@atmajaya.ac.id'])
   		#msg.body = "This is the email body"
   		#mail.send(msg)
		#msg.add_recipient("somename@gmail.com")
		flash("You have successfully registered! You may now login")
		return redirect(url_for("auth.login"))

	return render_template("auth/register.html",form=form,title="Register")

@auth.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You have successfully been logged out.")
	return redirect(url_for("auth.login"))
