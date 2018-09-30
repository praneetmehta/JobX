import json
import os
from collections import OrderedDict
from werkzeug.security import generate_password_hash, check_password_hash

def loadJSON(filename):
	with open(filename, 'r') as file:
		data = json.load(file, object_pairs_hook=OrderedDict)
	return data

class Registration:
	def __init__(self):
		self.user_template = loadJSON('JobX/utils/templates/user.json')

	def generatePassword(self, pwd):
		return generate_password_hash(pwd)

	def validateUsername(self, username):
		self.registeredUsers = list(map(lambda x: x[:-5], os.listdir('JobX/user_profiles')))
		print(self.registeredUsers)
		if username in self.registeredUsers:
			return False
		return True

	def registerUser(self):
		if self.user_template['valid_reg'] == 1:
			with open('JobX/user_profiles/'+self.user_template['username']+'.json', 'w') as file:
				json.dump(self.user_template, file, indent=4)
			return True
		return False

	def createUser(self, fn, ln, un, pwd, con, email, dob):
		if self.validateUsername(un):
			self.user_template['id'] = len(self.registeredUsers)+1
			self.user_template['username'] = un
			self.user_template['password'] = self.generatePassword(pwd)
			self.user_template['first_name'] = fn
			self.user_template['last_name'] = ln
			self.user_template['dob'] = dob
			self.user_template['contact'] = con
			self.user_template['email'] = email
			self.user_template['valid_reg'] = 1
			return (self.registerUser(), "Successfuly signed up")
		else:
			return (False, "Username ALready Exists");

class LoginValidator:
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def validate(self):
		if self.username+'.json' in os.listdir('JobX/user_profiles/'):
			with open('JobX/user_profiles/'+self.username+'.json', 'r') as file:
				password_hash = json.load(file)['password']
			if(check_password_hash(password_hash, self.password)):
				return (True, "User validation successful")
			else:
				return (False, "Incorrect Password")
		else:
			return (False, "Username not found")

if __name__ == "__main__":
	education_template = loadJSON(url_for('static', 'templates/education.json'))
	# experience_template = loadJSON('templates/experience.json')
	project_template = loadJSON(url_for('static', 'templates/project.json'))
	user_template = loadJSON(url_for('static', 'templates/user.json'))
	validateUsername('praneet')