from flask import Flask, render_template, request, redirect, url_for, session
from JobX.user.router import user
from JobX.base.router import base
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.register_blueprint(base, url_prefix='/')
app.register_blueprint(user, url_prefix='/user')

app.add_url_rule('/classificationModel', endpoint='cm',
                 view_func=app.send_static_file)

app.add_url_rule('/uploads', endpoint='uploads',
                 view_func=app.send_static_file)

UPLOAD_FOLDER = 'JobX/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

app.config['SECRET_KEY'] = 'SDFEWhad70235C@#34e21'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

#override url_for to add a timestamp behind the file paths
@app.context_processor
def override_url_for():
	return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
	if endpoint == 'static':
		filename = values.get('filename', None)
		if filename:
			file_path = os.path.join(app.root_path, endpoint, filename)
		values['q'] = int(os.stat(file_path).st_mtime)
	return url_for(endpoint, **values)
