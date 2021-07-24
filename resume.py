
from __future__ import print_function
import os,io
from flask import Flask,render_template,request, redirect,abort, url_for
from werkzeug.utils import secure_filename
from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(os.getcwd()+'\\key.json')

ocr = Flask(__name__)

ocr.config['UPLOAD_EXTENSION'] = ['.jpg', '.png', '.jpeg']
ocr.config['UPLOAD_PATH'] = 'files'

@ocr.route('/data')
def data():
    
    
    
    path = os.path.join(os.getcwd()+"\\files\\test.png")  #TODO: Change it 
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    result=[text.description+'\n' for text in response.text_annotations]


    for text in response.text_annotations:
        print('=' * 30)
        print(text.description)
        vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
        print('bounds:', ",".join(vertices))

    return render_template('data.html',result=result)
    
@ocr.route('/', methods=['GET','POST'])
def upload_file():
    if request.method=='GET':
        return render_template('index.html')
    print('post method called')
    for uploadedImage in request.files.getlist('file'):
        filename = secure_filename(uploadedImage.filename)

        try:
        
            if(filename!=''):
                extension = os.path.splitext(filename)[1]
                if extension not in ocr.config['UPLOAD_EXTENSION']:
                    abort(404)
                    
                uploadedImage.save(os.path.join(ocr.config['UPLOAD_PATH'],'test'+extension))

        except Exception as e:
            print(e)
            print("A exception occured")
    
    return redirect(url_for('data'))


if __name__ == "__main__":
    ocr.run(debug=True)