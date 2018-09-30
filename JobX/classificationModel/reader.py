import PyPDF2
import docx
import re

def getText(filename):
	with open(filename, 'r') as file:
		data = file.read()
	return data
	
def getTextPDF(filename):
	pdfFileObj = open(filename, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	num_pages = pdfReader.numPages
	count = 0
	text = ""
	#The while loop will read each page
	while count < num_pages:
		pageObj = pdfReader.getPage(count)
		count +=1
		text += pageObj.extractText()
	return text

def getTextDOCX(filename):
	doc = docx.Document(filename)
	fullText = []
	for para in doc.paragraphs:
		fullText.append(para.text)
	return ' '.join(fullText)

def preprocess(text):
	text = re.sub('[^A-Za-z]', ' ', text)
	text = ' '.join(text.split())
	return text

def textChunks(text, chunkSize = 40):
	words = text.split(' ')
	chunks = []
	i = 0
	while(i < len(words)):
		chunks.append((' ').join(words[i:i+chunkSize]))
		i+=chunkSize
	return chunks

def readFile(filename):
	print(filename)
	if filename.endswith('.pdf'):
		text = getTextPDF(filename)
	elif filename.endswith('.docx') or filename.endswith('.doc'):
		text = getTextDOCX(filename)
	elif filename.endswith('.txt'):
		text = getText(filename)
	else:
		return False
	text = preprocess(text)
	return text

if __name__ == "__main__":
	filename = '2Ben.pdf'
	if filename.endswith('.pdf'):
		text = getTextPDF(filename)
	elif filename.endswith('.docx'):
		text = getTextDOCX(filename)
	text = preprocess(text)
	print(textChunks(text))