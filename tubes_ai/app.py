import os
from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

UPLOAD_FOLDER = 'file_up/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def predict(teks):
	#train dataset
	train = pd.read_csv('ml/train.csv')
	label_train = train['HS'].values
	tweet_train = train['Tweet'].values
	
	#test dataset
	test = pd.read_csv('ml/test.csv')
	label_test = test['HS'].values
	tweet_test = test['Tweet'].values
	
	#tokenization dataset
	tokenizer = Tokenizer(num_words=800, oov_token='x')
	tokenizer.fit_on_texts(tweet_train) 
	tokenizer.fit_on_texts(tweet_test)
	sequences_train = tokenizer.texts_to_sequences(tweet_train)
	sequences_test = tokenizer.texts_to_sequences(tweet_test)
	padded_train = pad_sequences(sequences_train, maxlen=50, padding='post', truncating='post') 
	padded_test = pad_sequences(sequences_test, maxlen=50, padding='post', truncating='post')
	
	#pretrained model
	model = tf.keras.models.load_model('ml/my_model.h5')
	
	#predict
	tokenizer.fit_on_texts(teks)
	seq = tokenizer.texts_to_sequences(teks)
	pad = pad_sequences(seq, maxlen=50, padding='post', truncating='post')
	#print(pad)
	result = model.predict([pad])
	return result

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Halaman awal
@app.route('/', methods = ['POST', 'GET'])
def index():
	text_in = ''
	berkas = ''
	label = "AMAN"
	if request.method == 'POST':
		try:
			text_in = request.form['text-in']
		except:
			pass
		
		try:
			berkas = request.files['file']
		except:
			pass
		
	if berkas and allowed_file(berkas.filename):
			filename = secure_filename(berkas.filename)
			berkas.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			
	if text_in:
		text_in = text_in.lower()
		text_in = [text_in]
		result = predict(text_in)
		
		if (result[0][0] > 0.5):
			label = "HATE SPEECH"
	
	return render_template('index.html', text_in = text_in[0], label = label, berkas = berkas, judul='Home')
    

if __name__ == '__main__':
	app.run(debug=True)
