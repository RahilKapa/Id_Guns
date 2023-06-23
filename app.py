import os
import subprocess
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename

app = Flask("Find Weapons")
app.secret_key = 'my_secret_key'

# Set the path for uploaded images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def show_predict_stock_form():
    return render_template('predictorform.html')

@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Prepare the command
            cmd = f'python3 recognize-anything/inference_ram.py --image {os.path.join(app.config["UPLOAD_FOLDER"], filename)} --pretrained recognize-anything/pretrained/ram_swin_large_14m.pth'

            # Call your model for inference
            result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

            # Get the output
            predicted_object = result.stdout.decode()

            return render_template('resultsform.html', predicted_object=predicted_object)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)