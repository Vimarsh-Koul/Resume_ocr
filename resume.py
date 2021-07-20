import os
from flask import Flask,render_template,request, redirect,abort, url_for
from werkzeug.utils import secure_filename

ocr = Flask(__name__)

ocr.config['UPLOAD_EXTENSION'] = ['.jpg', '.png', '.jpeg']
ocr.config['UPLOAD_PATH'] = 'files'

@ocr.route('/')
def index():
    return render_template('index.html')

@ocr.route('/', methods=['POST'])
def upload_file():
    for uploadedImage in request.files.getlist('file'):
        filename = secure_filename(uploadedImage.filename)

        # try:
        print("entered try")
        if(filename!=''):
            extension = os.path.splitext(filename)[1]
            if extension not in ocr.config['UPLOAD_EXTENSION']:
                abort(404)
                
            uploadedImage.save(os.path.join(ocr.config['UPLOAD_PATH'],filename))

        # except:
        #     print("A exception occured")
    
    return redirect(url_for('index'))


if __name__ == "__main__":
    ocr.run(debug=True)