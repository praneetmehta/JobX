import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error as msq
from sklearn.ensemble import RandomForestClassifier
import reader
import os
import re
import numpy as np
import pickle

def preprocess(cell):
	# cell = re.sub('[^A-Za-z]', ' ', text)
	cell = re.sub(r'\b\w{1,2}\b','', cell)
	cell = (' ').join(cell.split())
	cell = cell.lower()
	return cell.strip()


if __name__ == "__main__":
	folders = ['Manager/', 'Accounts/', 'Audit/', 'Analyst/', 'Data_Science/']
	results = {1: 'Manager', 2: 'Accounts', 3:'Audit', 4:'Analyst', 5:'Data Science'}
	dataroot = 'resumeLabeled/'
	resume = list()
	label = list()
	if not os.path.isfile('datasetLabeled.csv'):
		for i, folder in enumerate(folders):
			for file in os.listdir(dataroot+folder):
				try:
					text = reader.readFile(dataroot+folder+file)
					if text is not None:
						resume.append(reader.readFile(dataroot+folder+file))
						label.append(i+1)
				except:
					pass

		data = pd.DataFrame({'Resume':resume, 'category':label})
		data.to_csv('datasetLabeled.csv', sep=',')
	if not os.path.isfile('datasetLabeledProcessed.csv'):
		df = pd.read_csv('datasetLabeled.csv', sep=',')
		df = df.dropna()
		# df.category = df.category.astype(int)
		print(df.head())
		df.Resume = df.Resume.apply(preprocess)
		df = df[df['Resume'].map(len) > 100]
		df.to_csv('datasetLabeledProcessed.csv', sep=',')
	df = pd.read_csv('datasetLabeledProcessed.csv', sep=',')
	X = df['Resume']
	Y = df['category']

	X_train , X_test, Y_train, Y_test = train_test_split(X,Y, stratify=Y)

	vectorizer = TfidfVectorizer(stop_words = 'english', max_df=0.25, ngram_range=(1,2),use_idf = True)
	X_train = vectorizer.fit_transform(X_train)
	X_test = vectorizer.transform(X_test)
	# X_vec = vectorizer.transform(X)

	regressor = LogisticRegression(C=10, warm_start=True)
	regressor.fit(X_train, Y_train)

	y_pred = regressor.predict(X_test)
	print(accuracy_score(Y_test, y_pred))
	print(classification_report(Y_test, y_pred))

	file = open('savedModel.pkl', 'wb')
	pickle.dump((regressor, vectorizer, results), file)
	file.close()
# print(reader.readFile(dataroot+folders[1]+'JTB_Chung Yon Jie_Accountant.pdf'))