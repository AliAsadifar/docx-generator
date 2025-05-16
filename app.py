from flask import Flask, request, jsonify, send_from_directory
from docx import Document
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/generate-docx', methods=['POST'])
def generate_docx():
    data = request.get_json()
    report_text = data.get('report_text', '')

    doc = Document()
    doc.add_paragraph(report_text)

    filename = f"report-{uuid.uuid4()}.docx"
    path = os.path.join(UPLOAD_FOLDER, filename)
    doc.save(path)

    return jsonify({
        "file_url": f"{request.host_url}static/{filename}"
    })

@app.route('/static/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
