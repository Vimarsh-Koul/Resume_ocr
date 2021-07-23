import os
from flask import Flask,render_template,request, redirect,abort, url_for
from werkzeug.utils import secure_filename
from google.cloud import storage,vision


ocr = Flask(__name__)

def upload_blob(source_file_name, destination_blob_name,bucket_name="resumeocr"):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def retrive_data(filename):
    image_uri = 'gs://resumeocr/' + filename

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)

    for text in response.text_annotations:
        print('=' * 30)
        print(text.description)
        vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
        print('bounds:', ",".join(vertices))


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
            upload_blob('files/'+filename, filename)
            retrive_data(filename)

        # except:
        #     print("A exception occured")
    
    return redirect(url_for('index'))




if __name__ == "__main__":
    ocr.run(debug=True)