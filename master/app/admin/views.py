#app/admin/views.py
from flask import abort,flash,redirect,render_template,url_for
from flask_login import current_user,login_required

from . import admin
from forms import UserForm
from .. import db
from ..models import User

def check_admin():
	if not current_user.is_admin:
		abort(403)

@admin.route("/users")
@login_required
def list_users():
	check_admin()
	users=User.query.all()
	return render_template("admin/users/users.html",users=users,title="Users")

@admin.route("/users/add",methods=["GET","POST"])
@login_required
def add_user():
	check_admin()
	add_user=True
	form=UserForm()
	if form.validate_on_submit():
		user=User(email=form.email.data,password=form.password.data)
		try:
			db.session.add(user)
			db.session.commit()
			flash("You have successfully added a new uer")
		except:
			flash("Error: User alredy exists")
		return redirect(url_for("admin.list_users"))
	return render_template("admin/users/user.html",action="Add",add_user=add_user,form=form,title="Add User")

@admin.route("/users/edit/<int:id>",methods=["GET","POST"])
@login_required
def edit_user(id):
	check_admin()
	add_user=False
	user=User.query.get_or_404(id)
	form=UserForm(obj=user)
	if form.validate_on_submit():
		user.email=form.email.data
		user.password=form.password.data
		db.session.commit()
		flash("You have successfully edited the department")
		return redirect(url_for("admin.list_users"))

	form.email.data=user.email
	#form.password.data=user.password
	return render_template("admin/users/user.html",action="Edit",add_user=add_user,form=form,user=user,title="Edit User")

@admin.route("/users/delete/<int:id>",methods=["GET","POST"])
@login_required
def delete_user(id):
	check_admin()
	user=User.query.get_or_404(id)
	db.session.delete(user)
	db.session.commit()
	flash("You have successfully deleted the user")
	return redirect(url_for("admin.list_users"))
	return render_template(title="Delete User")
