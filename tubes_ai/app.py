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


# Halaman awal
@app.route('/', methods = ['POST', 'GET'])
def index():
	text_in = ''
	label = ''
	if request.method == 'POST':
		text_in = request.form['text-in']
			
	if text_in:
		text_in = text_in.lower()
		text_in = [text_in]
		result_hs = predict('hs', text_in)
		result_cb = predict('cb', text_in)
		
		if (result_hs[0][0] > 0.5):
			label = "HATE SPEECH"
		elif (result_cb[0][0] > 0.51):
			label = "BULLYING"
		else:
			label = "BIASA"
		
	return render_template('index.html', text_in = text_in, label = label, judul='Home')
    
    
@app.route('/wa-analysis', methods = ['POST', 'GET'])
def wa_analysis():
	hs = []
	cb = []
	hasil=[]
	# file upload
	berkas = ''
	if request.method == 'POST':
		berkas = request.files['file']
				
	if berkas and allowed_file(berkas.filename):
		filename = secure_filename(berkas.filename)
		berkas.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	
	df = clean(berkas.filename)
	r_hs = predict('hs', df['Message'])
	r_cb = predict('cb', df['Message'])
		
	for i in range(len(df)):
		if r_hs[i][0] > 0.5:
			hs.append(df['Author'][i])
		if r_cb[i][0] > 0.51:
			cb.append(df['Author'][i])
			
	people = set(hs+cb)
	tot_data = len(df)
	for i in people:
		x = (hs.count(i)+cb.count(i))/2
		bb = ((tot_data - x)/tot_data)*100
		r = {'nama': i, 'hs': (hs.count(i)/tot_data)*100, 'cb': (cb.count(i)/tot_data)*100, 'bb': bb}
		hasil.append(r)
	
	return render_template('wa-analysis.html',  hasil=hasil, judul='Home')

if __name__ == '__main__':
	app.run(debug=True)
