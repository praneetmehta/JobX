from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from JobX.utils.profiler import Registration, LoginValidator
import json
import sys

base = Blueprint('root', __name__)

#route handler for the root path
@base.route('/')
def index():
	if 'user' in session.keys():
		return render_template('index.html', loggedIn = True)
	else:
		return render_template('index.html', loggedIn = False)

#route handler for the login path
@base.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in session.keys():
		return redirect(url_for('.index'))
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		lv = LoginValidator(username, password)
		loginResponse = lv.validate()
		if(loginResponse[0]):
			session['user'] = username
			return redirect(url_for('.index'))
		else:
			flash(loginResponse[1])
			return render_template('login.html')
	else:
		return render_template('login.html')

#route handler for the user profile page
@base.route('/user')
def user():
	# form = ResumeForm()
	if('user' not in session.keys()):
		return redirect(url_for('.index'))
	return render_template('user_.html')

#route handler for the logout path
@base.route('/logout')
def logout():
	if 'user' in session.keys():
		session.pop('user')
	return redirect(url_for('.index'))

@base.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		firstname = request.form['first_name']
		lastname = request.form['last_name']
		username = request.form['username']
		password = request.form['password']
		contact = request.form['contact']
		email = request.form['email']
		dob = request.form['dob']
		reg = Registration()
		signupResponse = reg.createUser(firstname, lastname, username, password, contact, email, dob)
		if signupResponse[0]:
			flash("Successfuly Signed Up")
			return redirect(url_for('.login'))
		else:
			flash(signupResponse[1])
			return render_template('signup.html')
	return render_template('signup.html')
