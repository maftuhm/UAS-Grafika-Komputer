from flask import Flask, request, render_template, redirect
from os.path import join, dirname, realpath
import ImageClassificationAPI as clf

app = Flask(__name__)

UPLOADS_PATH = join(dirname(realpath(__file__)), '..', 'data', 'data-predict')
ALLOWED_EXTENSION = set(['png', 'jpeg', 'jpg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':

		if 'image' not in request.files:
			return redirect(request.url)

		file = request.files['image']

		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			filename = join(UPLOADS_PATH, file.filename)
			file.save(filename)
			return redirect('/result/'+file.filename)
	return render_template('upload.html')