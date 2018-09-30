from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
from JobX.utils.profiler import Registration, LoginValidator
import json
import sys, os
from werkzeug.utils import secure_filename
import JobX.classificationModel.openModel as cmodel
import JobX.gensim.gensim_model as gen

user = Blueprint('user', __name__)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf', 'txt', 'doc', 'docx']

@user.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('JobX/uploads',
                               filename)

@user.route('/employeeTools')
def employeeTools():
	if 'user' not in session.keys():
		return redirect('/')
	return render_template('employeeTools.html')

@user.route('/employeeTools/jd')
def jd():
	if 'user' not in session.keys():
		return redirect('/')
	session['userClass'] = cmodel.Model().makePredictionforCV(session['filename'])
	return redirect('/user/employeeTools/submitJD')

@user.route('/employeeTools/submitJD', methods=['POST', 'GET'])
def submitJD():
	if 'user' not in session.keys():
		return redirect('/')
	if request.method == 'POST':
		session['userJD'] = request.form['JD']
		employeeSummary, employeeSkills, jdSkills, finalScore =  gen.generateSummary(session['filename'], session['userJD'], thresh=0.7)
		return render_template('employeeReport.html', data=[employeeSummary, employeeSkills, jdSkills, finalScore])
	else:
		flash("Your CV Matches "+session['userClass']+" profile")
		return render_template('employeejd.html', userClass = session['userClass'])

@user.route('/employerTools', methods=['POST', 'GET'])
def employerTools():
	if 'user' not in session.keys():
		return redirect('/')
	if request.method == 'POST':
		session['userJD'] = request.form['JD']
		session['JD'] = cmodel.Model().makePredictionforJD(session['userJD'])
		return redirect('/user/employerTools/resumeSuggestion')
	return render_template('employerTools.html')

@user.route('/employerTools/resumeSuggestion', methods=['POST', 'GET'])
def matchResumes():
	if 'user' not in session.keys():
		return redirect('/')
	cat = session['JD']
	top10Resume = cmodel.Model().getTop10(session['JD'], 15)
	top10 = list()
	total = 0
	for resume in top10Resume[:]:
		try:
			employeeSummary, employeeSkills, jdSkills, finalScore =  gen.generateSummary('JobX/classificationModel/resumeLabeled/'+('_').join(session['JD'].split(' '))+'/'+resume, session['userJD'], thresh=0.7, addfilePath=False)
			top10.append([resume, [employeeSummary, employeeSkills, jdSkills, finalScore]])
			total += 1
		except:
			pass		
		if(total == 10):
			break
	top10.sort(key=lambda x: x[1][3], reverse=True)
	return render_template('matchingResume.html', JDcat = cat, top10=top10)

@user.route('/upload_file', methods=['POST', 'GET'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return redirect('/user/employeeTools')
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join('JobX/uploads', filename))
			session['filename'] = filename
			return redirect('/user/employeeTools/jd')
	else:
		return redirect('/user/employeeTools')

