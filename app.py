import os
from flask import Flask, render_template, request, send_file
from pdf2docx import Converter
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400

    file = request.files['pdf_file']

    # Save uploaded file to Render's temporary directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        file.save(temp_pdf.name)
        output_path = temp_pdf.name.replace(".pdf", ".docx")

    try:
        cv = Converter(temp_pdf.name)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 500
    finally:
        # Clean up temporary files
        if os.path.exists(temp_pdf.name):
            os.remove(temp_pdf.name)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
