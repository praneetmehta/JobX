import pickle
import JobX.classificationModel.reader as reader
from flask import url_for
import os, sys

class Model:
	def __init__(self):
		picklePath = 'JobX/classificationModel/savedModel.pkl'
		file = open(picklePath, 'rb')
		tup = pickle.load(file)
		self.model = tup[0]
		self.vectorizer = tup[1]
		self.results = tup[2]
		
	def makePredictionforJD(self, text):
		return self.results[self.model.predict(self.vectorizer.transform([text]))[0]]

	def makePredictionforCV(self, filename):
		path = "JobX/uploads/"+filename
		text = reader.readFile(path)
		return self.results[self.model.predict(self.vectorizer.transform([text]))[0]]

	def getTop10(self, type, num=10):
		folder = ('_').join(type.split(' '))
		folderPath = "JobX/classificationModel/resumeLabeled/"+folder+'/'
		resumes = os.listdir(folderPath)
		return resumes[:num] 
