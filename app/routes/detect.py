import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

detect = Blueprint('detect', __name__)
# Fix this in detect.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'static', 'uploads')
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@detect.route('/detect', methods=['GET', 'POST'])
def detect_disease():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        print("POST request received")

        if 'crop_image' not in request.files:
            print("No file in request")
            return redirect(request.url)

        file = request.files['crop_image']
        if file.filename == '':
            print("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print(f"File uploaded: {file.filename}")
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            simulated_result = {
                "disease": "Early Blight",
                "description": "A fungal disease affecting tomatoes and potatoes.",
                "treatment": "Use fungicides like mancozeb."
            }

            return render_template("detect.html", image_url=filepath.replace('app/', ''), result=simulated_result)

        print("File not allowed or error occurred")

    return render_template("detect.html")
