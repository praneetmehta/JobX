import os, errno
import html2text

htmls = os.listdir('FinanceManager/')
# try:
# 	os.makedirs('resumeLabeled/IT')
# except OSError as e:
# 	if e.errno != errno.EEXIST:
# 		raise
count = 0
for html in htmls[:]:
	with open('FinanceManager/'+html, 'r', encoding='utf-8') as htmlfile:
		htmlcontent = htmlfile.read()
	htmltext = html2text.html2text(htmlcontent)
	htmltext = (htmltext.rsplit('--|--', 1)[1]).split('[Email')[0]
	with open('FinanceManager/'+html[:-5]+'.txt', 'w', encoding='utf-8') as file:
		file.write(htmltext)
	count += 1
	print(count)