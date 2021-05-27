import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#train dataset
train = pd.read_csv('ml/train_cb.csv')
label_train = train['Bully'].values
tweet_train = train['Comment'].values

#test dataset
test = pd.read_csv('ml/test_cb.csv')
label_test = test['Bully'].values
tweet_test = test['Comment'].values

#tokenization dataset
tokenizer = Tokenizer(num_words=800, oov_token='x')
tokenizer.fit_on_texts(tweet_train) 
tokenizer.fit_on_texts(tweet_test)
sequences_train = tokenizer.texts_to_sequences(tweet_train)
sequences_test = tokenizer.texts_to_sequences(tweet_test)
padded_train = pad_sequences(sequences_train, maxlen=50, padding='post', truncating='post') 
padded_test = pad_sequences(sequences_test, maxlen=50, padding='post', truncating='post')

#pretrained model
model = tf.keras.models.load_model('ml/model_cb.h5')

#predict
_, train_acc = model.evaluate(padded_train, label_train)
_, test_acc = model.evaluate(padded_test, label_test)

print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))
