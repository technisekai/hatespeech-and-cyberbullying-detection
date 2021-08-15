#Import library
import re
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#split date
def startsWithDateTime(s):
    patterns = ['([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -', '([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}) ([0-9][0-9]).([0-9][0-9]) -']
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False
    
#split author wurh regex
def startsWithAuthor(s):
    patterns = [
        '([\w]+):',                                # First Name
        '([\w]+[\s]+[\w]+):',                      # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',            # First Name + Middle Name + Last Name
        '([\w\W]+[\s\W]+[\w\W]+[\s\W]+[\w\W]+):',  # First Name + Middle Name + Last Name that maybe have non-character
        '\+?([ -]?\d+)+|\(\d+\)([ -]\d+)'          # Mobile Number (indonesia)
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False
    
#split time, message, and author
def getDataPoint(line):
	#split time
    splitLine = line.split(' - ')
    dateTime = splitLine[0]
    date, time = dateTime.split(' ')
    #split message
    message = ' '.join(splitLine[1:])
    
    if startsWithAuthor(message):
        splitMessage = message.split(': ')
        author = splitMessage[0] #author
        message = ' '.join(splitMessage[1:]) #message
    else:
        author = None
    return date, time, author, message

#preparing data
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#lowercase
def lowercase(text):
    return text.lower()

#remove unnecessary char
def remove_unnecessary_char(text):
    text = re.sub('\n',' ',text) # Remove every '\n'
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) # Remove every URL
    text = re.sub('  +', ' ', text) # Remove extra spaces
    return text
 
#remove non-alphanumeruic   
def remove_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text) 
    return text

#stemming
def stemming(text):
    return stemmer.stem(text)

#process
def preprocess(text):
    text = lowercase(text) # 1
    text = remove_nonaplhanumeric(text) # 2
    text = remove_unnecessary_char(text) # 2
    text = stemming(text) # 4
    return text

#clean
def clean(path_file):
	parsedData = []
	conversationPath = "file_up/"+path_file    #path ke file
	with open(conversationPath, encoding="latin1") as fp:
		fp.readline()
			
		messageBuffer = []
		date, time, author = None, None, None
		
		while True:
			line = fp.readline() 
			if not line:
				break
			line = line.strip()
			if startsWithDateTime(line):
				if len(messageBuffer) > 0:
					parsedData.append([date, time, author, ' '.join(messageBuffer)])
     
				messageBuffer.clear()
				date, time, author, message = getDataPoint(line)
				messageBuffer.append(message)
			else:
				messageBuffer.append(line)
				
	#to pandas
	df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
	
	#apply next step preprocess
	df['Message'] = df['Message'].apply(preprocess)
	
	#remove value with None
	for i in range(len(df["Message"])):
		if '' == df["Message"][i]:
			df["Message"][i] = None
		if 'media omitted' == df["Message"][i]:
			df["Message"][i] = None
		 
	#drop None
	df.dropna(inplace=True)
	df.reset_index(drop=True, inplace=True)
	
	#take column author and message
	df = df.drop(columns=['Date','Time'])
	
	return df
