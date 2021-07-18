# machine learning library
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# predict texts
def predict(kategori, teks):
	#train dataset
	train = pd.read_csv('ml/train_'+ kategori +'.csv')
	
	#test dataset
	test = pd.read_csv('ml/test_'+ kategori +'.csv')
	
	#split train test 
	if (kategori == 'cb'):
		label_train = train['Bully'].values
		teks_train = train['Comment'].values
		label_test = test['Bully'].values
		teks_test = test['Comment'].values
	else:
		label_train = train['HS'].values
		teks_train = train['Tweet'].values
		label_test = test['HS'].values
		teks_test = test['Tweet'].values
	
	#tokenization dataset
	tokenizer = Tokenizer(num_words=800, oov_token='x')
	tokenizer.fit_on_texts(teks_train) 
	tokenizer.fit_on_texts(teks_test)
	sequences_train = tokenizer.texts_to_sequences(teks_train)
	sequences_test = tokenizer.texts_to_sequences(teks_test)
	padded_train = pad_sequences(sequences_train, maxlen=50, padding='post', truncating='post') 
	padded_test = pad_sequences(sequences_test, maxlen=50, padding='post', truncating='post')
	
	#pretrained model
	model = tf.keras.models.load_model('ml/model_'+ kategori +'.h5')
	
	#predict
	#tokenizer.fit_on_texts(teks)
	seq = tokenizer.texts_to_sequences(teks)
	pad = pad_sequences(seq, maxlen=50, padding='post', truncating='post')

	result = model.predict([pad])
	return result
