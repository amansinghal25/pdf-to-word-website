from flask import Flask, request, send_file, render_template
import os, tempfile, subprocess
from pdf2docx import Converter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    file = request.files['pdf_file']
    if not file:
        return "No file uploaded", 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        file.save(temp_pdf.name)
        ocr_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        docx_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name

        try:
            subprocess.run(["ocrmypdf", "--skip-text", temp_pdf.name, ocr_pdf], check=True)
            cv = Converter(ocr_pdf)
            cv.convert(docx_file)
            cv.close()
            return send_file(docx_file, as_attachment=True, download_name="converted.docx")
        finally:
            for f in [temp_pdf.name, ocr_pdf, docx_file]:
                if os.path.exists(f):
                    os.remove(f)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
