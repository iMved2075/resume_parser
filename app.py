# app.py
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from extraction import extract_pdf_text, preprocess_text, extract_sections

app = Flask(__name__)

# Use an absolute path for the uploads folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the file is part of the request
        if 'file' not in request.files:
            return "No file part in the request.", 400
        file = request.files.get('file')
        if file.filename == '':
            return "No file selected.", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
                print("File saved to:", filepath)
            except Exception as e:
                print("Error saving file:", e)
                return f"Error saving file: {e}", 500

            # Process the PDF file using extraction functions
            raw_text = extract_pdf_text(filepath)
            clean_text = preprocess_text(raw_text)
            sections = extract_sections(clean_text)
            try:
                os.remove(filepath)
                print(f"Deleted file: {filepath}")
            except Exception as e:
                print(f"Error deleting file: {e}")
            # Option 1: Directly render the result page here
            return render_template("result.html", sections=sections)
    return render_template("upload.html")



if __name__ == '__main__':
    app.run(debug=True)
