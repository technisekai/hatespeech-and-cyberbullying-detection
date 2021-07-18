# web flask library
import os
from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from prediction import *
from clean_wa import *


# file upload
UPLOAD_FOLDER = 'file_up/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# validation file upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def kebalikan(text):
  fungsi3 = pd.read_csv('ml/fungsi3.csv', header=None)
  fungsi3_map = dict(zip(fungsi3[0], fungsi3[1]))
  
  return ' '.join([fungsi3_map[kata] if kata in fungsi3_map else kata for kata in text.split(' ')])

# Halaman awal
@app.route('/', methods = ['POST', 'GET'])
def index():
	text_in, label, balik = None, None, None
	if request.method == 'POST':
		text_in = request.form['text-in']
			
	if text_in:
		text_in = text_in.lower()
		text_in = [text_in]
		result_hs = predict('hs', text_in)
		result_cb = predict('cb', text_in)
		
		if (result_hs[0][0] > 0.5):
			label = "HATE SPEECH"
			balik = kebalikan(text_in[0])
		elif (result_cb[0][0] > 0.51):
			label = "BULLYING"
			balik = kebalikan(text_in[0])
		else:
			label = "BIASA"
		
	return render_template('index.html', text_in = text_in, balik = balik, label = label, title='Home')
	
@app.route('/fungsi_1', methods = ['POST', 'GET'])
def fungsi_1():
	text_in, label, balik = None, None, None
	if request.method == 'POST':
		text_in = request.form['text-in']
			
	if text_in:
		text_in = text_in.lower()
		text_in = [text_in]
		result_hs = predict('hs', text_in)
		result_cb = predict('cb', text_in)
		
		if (result_hs[0][0] > 0.5):
			label = "HATE SPEECH"
			balik = kebalikan(text_in[0])
		elif (result_cb[0][0] > 0.51):
			label = "BULLYING"
			balik = kebalikan(text_in[0])
		else:
			label = "BIASA"
		
	return render_template('fungsi1.html', text_in = text_in, label = label, title='Fungsi 1')
    
    
@app.route('/fungsi_2', methods = ['POST', 'GET'])
def fungsi_2():
	berkas, hasil = None, None
	hs = []
	cb = []
	bb = []
	hasil=[]
	
	if request.method == 'POST':
		berkas = request.files['file']
				
	if berkas and allowed_file(berkas.filename):
		filename = secure_filename(berkas.filename)
		berkas.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		df = clean(berkas.filename)
		r_hs = predict('hs', df['Message'])
		r_cb = predict('cb', df['Message'])
	
		
		for i in range(len(df)):
			isRun = False
			if r_hs[i][0] > 0.5:
				hs.append(df['Author'][i])
				isRun = True
			if r_cb[i][0] > 0.51:
				cb.append(df['Author'][i])
				isRun = True
			if not isRun:
				bb.append(df['Author'][i])
				
		people = set(hs+cb+bb)
		tot_data = len(df)
		for i in people:
			r = {'nama': i, 'hs': (hs.count(i)/tot_data)*100, 'cb': (cb.count(i)/tot_data)*100, 'bb': (bb.count(i)/tot_data)*100}
			hasil.append(r)
	
	return render_template('fungsi2.html',  hasil=hasil, title='Fungsi 2')
	
@app.route('/fungsi_3', methods = ['POST', 'GET'])
def fungsi_3():
	text_in, label, balik = None, None, None
	if request.method == 'POST':
		text_in = request.form['text-in']
			
	if text_in:
		text_in = text_in.lower()
		text_in = [text_in]
		result_hs = predict('hs', text_in)
		result_cb = predict('cb', text_in)
		
		if (result_hs[0][0] > 0.5):
			label = "HATE SPEECH"
			balik = kebalikan(text_in[0])
		elif (result_cb[0][0] > 0.51):
			label = "BULLYING"
			balik = kebalikan(text_in[0])
		else:
			label = "BIASA"
		
	return render_template('fungsi3.html', text_in = text_in, balik = balik, label = label, title='Fungsi 3')

@app.route('/tentang')
def tentang():
	return render_template('tentang.html',  title='Tentang')

if __name__ == '__main__':
	app.run(debug=True)
