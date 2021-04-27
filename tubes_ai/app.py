import os
from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'file_up/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Halaman awal
@app.route('/', methods = ['POST', 'GET'])
def index():
	text_in = ''
	berkas = ''
	if request.method == 'POST':
		#text_in = request.form['text-in']
		berkas = request.files['file']
		
	if berkas and allowed_file(berkas.filename):
			filename = secure_filename(berkas.filename)
			berkas.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		
	return render_template('index.html', text_in = text_in, judul='Home')
    

if __name__ == '__main__':
	app.run(debug=True)
